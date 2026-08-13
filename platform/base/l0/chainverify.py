"""Chain verifier v1 (PA-006, L0-012, DEC-0001 R1).

One implementation of the §9 caveat grammar (ENT-091–095) plus chain walk and
lease-TTL checking (ENT-072), consuming the act-token wire format of ES-020–023.
PA-006 requires this be the *only* implementation: the base carries no second
verifier, and the bus auth callout and gate library embed this same module.

Laws encoded here, each traceable:
  ENT-091  a caveat is a conjunction of guard predicates — no disjunction, no else
  ENT-092  predicates draw only on the fixed fact vocabulary
  ENT-093  composition is union; attenuation is algebraic, not policed
  ENT-094  verification is fail-closed: unknown fact, unknown op, or any error denies
  ENT-095  no exception-grammar construct may appear inside a credential
  ES-020   caveats are lists of lists of [fact, op, literal] — no objects on the wire
  ES-021   effective caveat set is the union along chain_ref to root
  ES-022   the verifier supplies operation facts; a predicate over anything else denies
  ENT-072  lease TTL is checked at every hop, not once
"""
import datetime
import operator

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from canon import CanonicalizationError, signing_form
from keys import b64d

# ENT-092 — the fact vocabulary is fixed by DOC-0005 and supplied by the verifier.
FACTS = frozenset({"now", "mint_time", "lease_age", "subject", "action",
                   "resource", "audience", "use_count", "depth", "parent_id", "lease_id"})

OPS = {
    "=": operator.eq, "!=": operator.ne, "<": operator.lt, "<=": operator.le,
    ">": operator.gt, ">=": operator.ge,
    "in": lambda a, b: isinstance(b, (list, tuple, str)) and a in b,
    "prefix-of": lambda a, b: str(b).startswith(str(a)),
}

# ENT-095 / ONT-057 — rule-layer constructs are not expressible in a credential.
EXCEPTION_TOKENS = frozenset({"given", "when", "meets", "then", "for"})


class VerificationError(Exception):
    """Any denial. There is no partial grant and no fallback branch (ENT-094)."""


def check_predicate(pred, facts):
    """One guard predicate. Anything unexpected denies rather than raises through."""
    if not isinstance(pred, (list, tuple)) or len(pred) != 3:
        return False
    fact, op, literal = pred
    if fact not in FACTS or op not in OPS or fact not in facts:
        return False  # ENT-094: unknown fact or op denies
    try:
        return bool(OPS[op](facts[fact], literal))
    except Exception:  # noqa: BLE001 — an unevaluable predicate denies
        return False


def well_formed_caveats(caveats):
    """ES-020/ENT-095: lists of lists of triples. An object anywhere is a smuggling
    attempt and is refused before evaluation — the ONT-032 pattern on the wire."""
    if not isinstance(caveats, list):
        return False
    for block in caveats:
        if isinstance(block, dict):
            return False
        if not isinstance(block, list):
            return False
        for pred in block:
            if isinstance(pred, dict):
                return False
            if not isinstance(pred, (list, tuple)) or len(pred) != 3:
                return False
            fact = pred[0]
            if isinstance(fact, str) and fact.lower() in EXCEPTION_TOKENS:
                return False
    return True


def verify_caveats(caveats, facts):
    """ENT-091/093/094: every predicate of every block must hold."""
    if not well_formed_caveats(caveats):
        raise VerificationError("malformed caveats (ES-020/ENT-095)")
    for block in caveats:
        for pred in block:
            if not check_predicate(pred, facts):
                raise VerificationError(f"caveat denied: {pred}")


def verify_detached(pubkey_b64, obj, sig_field):
    """Ed25519 over the JCS signing form (ES-011)."""
    sig = obj.get(sig_field)
    if not isinstance(sig, str):
        raise VerificationError(f"missing {sig_field}")
    try:
        Ed25519PublicKey.from_public_bytes(b64d(pubkey_b64)).verify(b64d(sig), signing_form(obj, sig_field))
    except CanonicalizationError as e:
        raise VerificationError(f"canonicalization failed: {e}") from e
    except (InvalidSignature, ValueError, TypeError) as e:
        raise VerificationError(f"signature invalid: {e}") from e


def _parse_ts(value):
    try:
        ts = datetime.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError as e:
        raise VerificationError(f"unparseable timestamp {value!r}") from e
    return ts if ts.tzinfo else ts.replace(tzinfo=datetime.timezone.utc)


def lease_age_hours(lease, now):
    """ENT-072/074: the dead-man property. An expired lease fails verification
    mesh-wide with no revocation event — cessation of proof and cessation of
    authority are the same fact."""
    issued = _parse_ts(lease["issued_at"])
    age = (now - issued).total_seconds() / 3600.0
    ttl = lease.get("ttl_hours")
    if ttl is None:
        raise VerificationError("lease carries no ttl (ENT-072)")
    if age > float(ttl):
        raise VerificationError(f"lease {lease.get('lease_id')} expired: age {age:.2f}h > ttl {ttl}h")
    return age


def walk(chain, token, facts, now=None):
    """Walk leaf -> root, verifying each hop and unioning caveats (ES-021, ENT-093).

    `chain` is the verification chain from chain.pub: nodes ordered leaf-parent
    first, root last, each { id, pub, parent, token?, lease? }. Returns the facts
    actually used, so callers can record what the decision rested on.
    """
    now = now or datetime.datetime.now(datetime.timezone.utc)
    if not chain:
        raise VerificationError("empty chain (ENT-002: every entity is a node in a chain)")

    by_id = {n["id"]: n for n in chain}
    # A root is a node with no parent — not a node *claiming* a parent named "root".
    # Accepting the sentinel string as a terminator meant a chain with its root node
    # deleted still verified: the claim of a root stood in for the root itself.
    root = [n for n in chain if n.get("parent") is None]
    if not root:
        raise VerificationError("chain does not terminate at a root node (ENT-002)")
    for node in chain:
        parent = node.get("parent")
        if parent is not None and parent not in by_id:
            raise VerificationError(
                f"chain is broken: {node['id']} names parent {parent!r}, absent from the "
                f"chain (ENT-002)")

    facts = dict(facts)
    facts["depth"] = len(chain)

    # The lease governs every hop below it, so its age is a fact for the whole walk.
    leases = [n["lease"] for n in chain if n.get("lease")]
    if leases:
        facts["lease_age"] = lease_age_hours(leases[0], now)
        facts["lease_id"] = leases[0].get("lease_id")

    # The act token is the parent's grant to the leaf: verify with the parent's key.
    parent_id = token.get("parent")
    parent = by_id.get(parent_id)
    if parent is None:
        raise VerificationError(f"token parent {parent_id!r} absent from chain")
    facts["parent_id"] = parent_id
    facts["mint_time"] = token.get("minted_at")
    verify_detached(parent["pub"], token, "parent_sig")

    if token.get("leaf") != facts.get("leaf"):
        raise VerificationError("token does not empower the presenting leaf")

    # ES-021: union of this token's caveats and every caveat reachable to root.
    verify_caveats(token.get("caveats", []), facts)

    seen, node = set(), parent
    while node is not None:
        if node["id"] in seen:
            raise VerificationError("cycle in chain")
        seen.add(node["id"])
        if node.get("lease"):
            lease_age_hours(node["lease"], now)  # ENT-072: every hop, not once
        if node.get("token"):
            verify_caveats(node["token"].get("caveats", []), facts)
            up = by_id.get(node["token"].get("parent"))
            if up is not None:
                verify_detached(up["pub"], node["token"], "parent_sig")
        nxt = node.get("parent")
        node = by_id.get(nxt) if nxt is not None else None

    return facts


def verify_boot(chain, token, leaf_pub_b64, audience, now=None):
    """L0-012: what init checks before any payload code path exists.

    Chain walks to root, every caveat evaluates against boot-time facts, lease TTL
    valid where a lease is in the chain, and the token's audience matches the spawn
    request — for agent spawns, the story ref.
    """
    now = now or datetime.datetime.now(datetime.timezone.utc)
    facts = {"now": now.isoformat(), "leaf": leaf_pub_b64, "action": "boot",
             "audience": audience, "subject": "", "resource": "", "use_count": 0}
    used = walk(chain, token, facts, now=now)
    declared = [p for block in token.get("caveats", []) for p in block if p and p[0] == "audience"]
    if not declared:
        raise VerificationError("token is not audience-bound (ENT-075/ES-023)")
    return used
