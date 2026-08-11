#!/l0/venv/bin/python
"""/l0/init — PID 1 (L0-010).

Sequence, in order, any step failing exits non-zero without starting the payload:
    verify handoff (L0-011) -> verify chain (L0-012) -> connect bus ->
    publish descriptor (L0-030) -> start heartbeat (L0-031) -> run payload

Identity is the gate the application starts behind: there is no payload code path
before verification, which is why the payload is launched at the very end of this
file and nowhere else.

One reading recorded plainly: L0-010 says "exec payload" while L0-032 requires the
base to capture payload stdout/stderr onto the telemetry subject. A true exec()
replaces PID 1 and makes capture impossible, so init supervises the payload as a
child and pumps its output. Supervision is also what lets PID 1 reap orphans and
emit the final telemetry event of L0-052.
"""
import asyncio
import datetime
import json
import os
import pathlib
import sys

import subjects
from agentd import Agentd
from chainverify import VerificationError, verify_boot
from keys import public_b64, signer_from_seed

HANDOFF = pathlib.Path("/run/l0")
CRED, TOKEN, CHAIN = HANDOFF / "leaf.cred", HANDOFF / "leaf.token", HANDOFF / "chain.pub"
BASE_VERSION_FILE = pathlib.Path("/l0/BASE_VERSION")

EXIT_NO_HANDOFF = 78      # BASE-AC-1
EXIT_BAD_CHAIN = 77       # BASE-AC-2
EXIT_BUS = 76


def log(msg):
    print(f"[l0.init] {msg}", file=sys.stderr, flush=True)


class L0Context:
    """What init verified, handed to agentd. Holds the only reference to the signer."""

    def __init__(self, cred, token, chain, config):
        self.signer = signer_from_seed(cred["leaf_seed_b64"])
        self.leaf_pub = public_b64(self.signer)
        self.act_token = token
        self.chain = chain["chain"]
        self.chain_head = chain.get("chain_head") or (self.chain[0]["id"] if self.chain else "")
        self.publish_allow = cred.get("publish_allow", [])   # ES-003 projection, minted upstream
        self.citizen = config["citizen"]
        self.context = config["context"]
        self.role_layer = config["role_layer"]
        self.mandate_ref = config.get("mandate_ref")
        self.image_digest = config.get("image_digest", "sha256:unknown")
        self.heartbeat_s = config["heartbeat_s"]
        self.bus = None

    def subject_granted(self, subject):
        """ES-003: the transport grant is the projection of the act grant. Prefix
        matching with an explicit trailing wildcard; no implicit widening."""
        for pattern in self.publish_allow:
            if pattern.endswith(".>") and subject.startswith(pattern[:-2] + "."):
                return True
            if pattern.endswith(".*"):
                head = pattern[:-2]
                if subject.startswith(head + ".") and "." not in subject[len(head) + 1:]:
                    return True
            if subject == pattern:
                return True
        return False


def read_handoff():
    """L0-011: exactly three inputs, as mounted files. Read once, held in memory,
    then unlinked so the payload namespace contains no readable key material."""
    missing = [str(p) for p in (CRED, TOKEN, CHAIN) if not p.is_file()]
    if missing:
        log(f"handoff incomplete, refusing to start payload: missing {missing}")
        sys.exit(EXIT_NO_HANDOFF)
    try:
        cred = json.loads(CRED.read_text())
        token = json.loads(TOKEN.read_text())
        chain = json.loads(CHAIN.read_text())
    except ValueError as e:
        log(f"handoff unparseable: {e}")
        sys.exit(EXIT_NO_HANDOFF)
    return cred, token, chain


def shred_handoff():
    """L0-011's observable property (BASE-AC-3). L0-011 specifies that the mount is
    not propagated into the payload's namespace; doing that literally needs mount
    namespace manipulation, which requires capabilities L0-002 drops. Unlinking
    after read achieves the checkable claim within the hardening envelope. Recorded
    as an interim posture, not passed off as the specified mechanism."""
    for p in (CRED, TOKEN, CHAIN):
        try:
            p.unlink()
        except OSError as e:
            log(f"could not unlink {p}: {e} — payload namespace may retain key material")


def config_from_env():
    return {
        "citizen": os.environ.get("L0_CITIZEN", "unknown-citizen"),
        "context": os.environ.get("L0_CONTEXT", "service"),
        "role_layer": os.environ.get("L0_ROLE_LAYER", "base@BASE-v1"),
        "mandate_ref": os.environ.get("L0_MANDATE_REF"),
        "image_digest": os.environ.get("L0_IMAGE_DIGEST", "sha256:unknown"),
        "heartbeat_s": int(os.environ.get("L0_HEARTBEAT_S", "30")),
        "bus_url": os.environ.get("L0_BUS_URL", "nats://127.0.0.1:4222"),
        "audience": os.environ.get("L0_AUDIENCE") or os.environ.get("L0_CONTEXT", "service"),
    }


def descriptor(ctx):
    """L0-030 / ENT-030/031: emitted, never authored."""
    return {
        "descriptor_version": 1,
        "entity": ctx.leaf_pub,
        "citizen": ctx.citizen,
        "image_digest": ctx.image_digest,
        "base_version": BASE_VERSION_FILE.read_text().strip() if BASE_VERSION_FILE.exists() else "unknown",
        "role_layer": ctx.role_layer,
        "mandate_ref": ctx.mandate_ref,
        "interfaces": [
            {"contract": "SPEC-0082", "direction": "exposes", "archetype": "bus",
             "required_caveat": None},
        ],
        "heartbeat": {"subject": subjects.heartbeat_subject(ctx.citizen),
                      "cadence_s": ctx.heartbeat_s},
    }


async def heartbeat_loop(ctx, agent):
    """L0-031. Staleness interpretation is a consumer concern, not a base concern."""
    started = datetime.datetime.now(datetime.timezone.utc)
    seq = 0
    while True:
        seq += 1
        uptime = (datetime.datetime.now(datetime.timezone.utc) - started).total_seconds()
        await agent.publish(subjects.heartbeat_subject(ctx.citizen),
                            {"entity": ctx.leaf_pub, "image_digest": ctx.image_digest,
                             "uptime_s": round(uptime, 3), "seq": seq},
                            payload_type="json")
        await asyncio.sleep(ctx.heartbeat_s)


async def pump(stream, agent, ctx, label):
    """L0-032: payload stdout/stderr captured by the base and published. No L0
    configuration disables this — there is no branch here that can be switched off."""
    subject = subjects.output_subject(ctx.citizen, ctx.context)
    while line := await stream.readline():
        text = line.decode(errors="replace").rstrip("\n")
        print(f"[{label}] {text}", flush=True)
        await agent.publish(subject, {"stream": label, "line": text}, payload_type="json")


async def run_payload(argv, agent, ctx):
    proc = await asyncio.create_subprocess_exec(
        *argv, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        env={**os.environ, "L0_SOCKET": "/run/l0/agent.sock"})
    await asyncio.gather(pump(proc.stdout, agent, ctx, "stdout"),
                         pump(proc.stderr, agent, ctx, "stderr"))
    rc = await proc.wait()
    await agent.emit_event("payload.exit", {"exit_status": rc})
    return rc


async def main():
    argv = sys.argv[1:]
    config = config_from_env()

    cred, token, chain = read_handoff()                      # L0-011
    ctx = L0Context(cred, token, chain, config)
    try:
        verify_boot(ctx.chain, token, ctx.leaf_pub, config["audience"])   # L0-012
    except VerificationError as e:
        log(f"chain verification failed, refusing to start payload: {e}")
        sys.exit(EXIT_BAD_CHAIN)
    shred_handoff()
    log(f"identity verified: leaf {ctx.leaf_pub[:12]}… audience {config['audience']}")

    import nats
    try:
        ctx.bus = await nats.connect(config["bus_url"], connect_timeout=5, max_reconnect_attempts=3)
    except Exception as e:  # noqa: BLE001
        log(f"bus unreachable at {config['bus_url']}: {e}")
        sys.exit(EXIT_BUS)

    agent = Agentd(ctx)
    server = await agent.serve()

    async def on_inbound(msg):
        """BASE-AC-13: verification happens before anything reaches the payload.
        There is no delivery path for an envelope that fails ES-013 — it is dropped
        and counted here, one frame below any payload-visible surface."""
        agent.accept_inbound(msg.data)

    await ctx.bus.subscribe(f"work.story.{ctx.context}.assign", cb=on_inbound)
    await agent.publish(subjects.descriptor_subject(ctx.citizen), descriptor(ctx),
                        payload_type="json")                  # L0-030
    hb = asyncio.create_task(heartbeat_loop(ctx, agent))       # L0-031

    rc = 0
    if argv:
        rc = await run_payload(argv, agent, ctx)
    else:
        log("no payload argv; running as a bare citizen (descriptor + heartbeat only)")
        await asyncio.sleep(float(os.environ.get("L0_IDLE_S", "3600")))

    hb.cancel()
    server.close()
    await ctx.bus.drain()
    return rc


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
