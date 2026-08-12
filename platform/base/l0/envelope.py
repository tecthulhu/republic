"""The envelope (L0-040, ES-010–013): the platform-wide message frame.

Verification order is fixed by ES-013 and the order is load-bearing — cheapest
check first, and each step is a hard denial:
  1. `sig` verifies against sender.leaf
  2. the chain walks to root with lease TTL checked at every hop
  3. the act token evaluates against the operation facts
Failure at any step: drop, count in telemetry, never deliver (BASE-AC-13).
"""
import datetime

from canon import CanonicalizationError, signing_form
from chainverify import VerificationError, verify_caveats, walk
from keys import b64e, b64d, verify_key

ENV_VERSION = 1
MAX_INLINE_BYTES = 128 * 1024  # ES-012: above this, payload_type must be `ref`


def build(subject, payload, sender_leaf_pub, chain_head, act_token, signer, seq,
          payload_type="text", now=None):
    """ES-010. Conforming writers emit no unknown fields (closed writer)."""
    now = now or datetime.datetime.now(datetime.timezone.utc)
    env = {
        "env_version": ENV_VERSION,
        "subject": subject,
        "sender": {"leaf": sender_leaf_pub, "chain": chain_head},
        "sent_at": now.isoformat(),
        "seq": seq,
        "act_token": act_token,
        "payload_type": payload_type,
        "payload": payload,
    }
    env["sig"] = b64e(signer.sign(signing_form(env, "sig")))
    return env


def size_ok(env):
    """ES-012: large payloads never ride the bus; they go to the object store and
    the envelope carries the ref."""
    try:
        body = signing_form(env, "sig")
    except CanonicalizationError:
        return False
    return len(body) <= MAX_INLINE_BYTES or env.get("payload_type") == "ref"


def verify(env, chain, facts, now=None):
    """ES-013, in order. Raises VerificationError on any failure."""
    if not isinstance(env, dict) or env.get("env_version") != ENV_VERSION:
        raise VerificationError("unknown envelope version")
    sender = env.get("sender") or {}
    leaf = sender.get("leaf")
    if not leaf:
        raise VerificationError("envelope has no sender leaf")

    # (1) signature
    sig = env.get("sig")
    if not isinstance(sig, str):
        raise VerificationError("envelope unsigned")
    try:
        verify_key(leaf).verify(b64d(sig), signing_form(env, "sig"))
    except CanonicalizationError as e:
        raise VerificationError(f"canonicalization failed: {e}") from e
    except Exception as e:  # noqa: BLE001 — fail closed
        raise VerificationError(f"envelope signature invalid: {e}") from e

    if not size_ok(env):
        raise VerificationError("envelope exceeds inline size discipline (ES-012)")

    # (2) + (3) chain walk and act-token evaluation against operation facts (ES-022)
    token = env.get("act_token")
    if not isinstance(token, dict):
        raise VerificationError("envelope carries no act token")
    subject = env.get("subject", "")
    op_facts = dict(facts)
    op_facts.update({"leaf": leaf, "subject": subject,
                     "resource": subject.split(".")[-1]})
    op_facts.setdefault("action", "publish")
    op_facts.setdefault("now", env.get("sent_at"))
    # ES-022: `audience` is an operation fact the verifier supplies, and omitting it
    # denied every audience-bound token — which is every authority-bearing token
    # (ES-023). For acta.<citizen>.<context>.* the context segment *is* the audience,
    # so it is derived here; for subjects that carry no context the caller supplies it,
    # because only the caller knows the act's binding.
    if "audience" not in op_facts:
        parts = subject.split(".")
        if len(parts) == 4 and parts[0] == "acta":
            op_facts["audience"] = parts[2]
    used = walk(chain, token, op_facts, now=now)
    verify_caveats(token.get("caveats", []), used)
    return used
