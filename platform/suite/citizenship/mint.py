"""Minting helper for the conformance suite.

This is the *spawner's* job in the real system (the harness, STORY-0002). Here it
exists only so the suite can produce valid and deliberately-invalid handoffs.
It is not a citizen capability and never ships in a role layer.

Chain shape per ENT-002/071:
    root (cold)  ->  persona  ->  custodian lease (TTL)  ->  leaf
"""
import datetime
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "base" / "l0"))
sys.path.insert(0, "/l0")

from canon import signing_form            # noqa: E402
from keys import b64e, generate, signer_from_seed  # noqa: E402


def _now():
    return datetime.datetime.now(datetime.timezone.utc)


def _token(leaf_pub, parent_id, parent_seed, caveats, chain_ref="root", minted_at=None):
    tok = {
        "tok_version": 1,
        "leaf": leaf_pub,
        "parent": parent_id,
        "chain_ref": chain_ref,
        "minted_at": (minted_at or _now()).isoformat(),
        "caveats": caveats,
    }
    tok["parent_sig"] = b64e(signer_from_seed(parent_seed).sign(signing_form(tok, "parent_sig")))
    return tok


def mint(citizen, context, audience=None, lease_ttl_hours=48, lease_age_hours=0,
         leaf_caveats=None, publish_allow=None):
    """Produce the three handoff files of L0-011 plus the seeds the suite needs."""
    audience = audience or context
    root_seed, root_pub = generate()
    persona_seed, persona_pub = generate()
    lease_seed, lease_pub = generate()
    leaf_seed, leaf_pub = generate()

    issued = _now() - datetime.timedelta(hours=lease_age_hours)
    lease = {"lease_id": "lease-suite-0001", "issued_at": issued.isoformat(),
             "ttl_hours": lease_ttl_hours}

    persona_token = _token(persona_pub, "root", root_seed, [[["depth", "<=", 8]]])
    lease_token = _token(lease_pub, "persona", persona_seed, [[["lease_age", "<", lease_ttl_hours]]])

    if leaf_caveats is None:
        leaf_caveats = [
            [["audience", "=", audience]],
            [["action", "in", ["boot", "publish", "request", "subscribe-deliver"]]],
            [["lease_age", "<", lease_ttl_hours]],
        ]
    leaf_token = _token(leaf_pub, "lease", lease_seed, leaf_caveats, chain_ref=lease["lease_id"])

    chain = {
        "chain_head": "lease",
        "chain": [
            {"id": "lease", "pub": lease_pub, "parent": "persona", "lease": lease, "token": lease_token},
            {"id": "persona", "pub": persona_pub, "parent": "root", "token": persona_token},
            {"id": "root", "pub": root_pub, "parent": None},
        ],
    }

    if publish_allow is None:
        # ES-003: the transport grant is the minting parent's projection of the act
        # grant — enumerated here, never widened by the citizen at runtime.
        publish_allow = [
            f"mesh.descriptor.{citizen}",
            f"mesh.heartbeat.{citizen}",
            f"acta.{citizen}.{context}.output",
            f"acta.{citizen}.{context}.event",
        ]

    cred = {"leaf_seed_b64": leaf_seed, "leaf_pub_b64": leaf_pub,
            "nats_creds": None, "publish_allow": publish_allow}

    return {"cred": cred, "token": leaf_token, "chain": chain,
            "seeds": {"root": root_seed, "persona": persona_seed, "lease": lease_seed,
                      "leaf": leaf_seed},
            "pubs": {"root": root_pub, "persona": persona_pub, "lease": lease_pub,
                     "leaf": leaf_pub}}


def write_handoff(target_dir, minted, owner=None):
    """Files land owned by the citizen UID so init can unlink them after reading
    (L0-011 / BASE-AC-3). The helper writing them runs privileged; the citizen
    that consumes them does not."""
    import os
    d = pathlib.Path(target_dir)
    d.mkdir(parents=True, exist_ok=True)
    (d / "leaf.cred").write_text(json.dumps(minted["cred"]))
    (d / "leaf.token").write_text(json.dumps(minted["token"]))
    (d / "chain.pub").write_text(json.dumps(minted["chain"]))
    if owner and os.geteuid() == 0:
        uid, gid = owner
        os.chown(d, uid, gid)
        for f in ("leaf.cred", "leaf.token", "chain.pub"):
            os.chown(d / f, uid, gid)
            os.chmod(d / f, 0o400)
    return d


if __name__ == "__main__":
    # Used by the suite to populate a handoff volume from inside a helper container.
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--citizen", required=True)
    ap.add_argument("--context", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--break-chain", action="store_true",
                    help="corrupt the leaf token signature (BASE-AC-2 fixture)")
    ap.add_argument("--expired-lease", action="store_true",
                    help="issue a lease already past its TTL (BASE-AC-2 fixture)")
    a = ap.parse_args()

    m = mint(a.citizen, a.context,
             lease_age_hours=72 if a.expired_lease else 0,
             lease_ttl_hours=48)
    if a.break_chain:
        sig = m["token"]["parent_sig"]
        m["token"]["parent_sig"] = ("A" if sig[0] != "A" else "B") + sig[1:]
    write_handoff(a.out, m, owner=(10001, 10001))
    print(json.dumps({"citizen": a.citizen, "leaf": m["pubs"]["leaf"], "out": a.out}))
