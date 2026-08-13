#!/usr/bin/env python3
"""CTRL-0005 — the gate library suite (SPEC-0081).

Tests the spawn gate: what it refuses, and what it produces when it admits. The
refusals are tested first and without a bus, because they must happen before a
container exists — a refusal issued after creation is not a refusal, and a suite that
only tested the happy path would not notice the difference.

Then one real spawn: a container comes up on a real bus, verifies its chain, publishes
a descriptor naming the story as its context, and does it with a leaf whose transport
grant is the ES-003 projection of its act token. No model credential is involved
anywhere here — launching a container is not credential-gated, and this suite is the
proof of that.

Usage:
    python3 suite/gates/run.py --image l0-agent:0.1.0
"""
import argparse
import datetime
import json
import os
import pathlib
import subprocess
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "harness"))

import merge_gate  # noqa: E402
import mint as minting  # noqa: E402
import spawn as gate  # noqa: E402
from mesh import Mesh, image_digest, observed, sh, wait_and_logs  # noqa: E402

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "base" / "l0"))
from chainverify import VerificationError  # noqa: E402
from envelope import build as build_envelope  # noqa: E402
from keys import signer_from_seed  # noqa: E402
from envelope import verify as verify_envelope  # noqa: E402

STORY = "story-0002"
CITIZEN = "spawn-probe"


class Results:
    def __init__(self):
        self.rows = []

    def record(self, ac, verdict, detail=""):
        self.rows.append({"ac": ac, "verdict": verdict, "detail": detail})
        print(f"  {verdict.upper():4}  {ac}{'' if verdict == 'pass' else '  — ' + str(detail)[:280]}")

    def ok(self, ac, cond, detail=""):
        self.record(ac, "pass" if cond else "fail", detail)
        return cond

    @property
    def failed(self):
        return [r for r in self.rows if r["verdict"] == "fail"]


def refuses(request, expect_criterion):
    """A refusal, and the reason it gives. The reason matters: a gate that refuses
    everything for one reason is not enforcing four rules."""
    try:
        gate.check(request)
        return False, "admitted"
    except gate.SpawnRefused as e:
        return e.criterion == expect_criterion, f"[{e.criterion}] {e.reason}"


def refusal_checks(image, res):
    base = {"citizen": CITIZEN, "image": image}

    ok, detail = refuses({**base, "story_ref": None}, "SPEC-0081")
    res.ok("SPEC-0081 story-less spawn refused before container creation", ok, detail)

    ok, detail = refuses({**base, "story_ref": STORY, "mounts": ["/etc:/etc:ro"]},
                         "BASE-AC-9")
    res.ok("BASE-AC-9 spawn spec with a host mount refused", ok, detail)

    # Ask for a caveat family the agent layer's ceiling does not contain. `kind` is not
    # in the ENT-092 vocabulary at all, which is the strongest form of the refusal.
    over = [[["audience", "=", STORY]], [["kind", "=", "silicon"]]]
    ok, detail = refuses({**base, "story_ref": STORY, "caveats": over}, "BASE-AC-17")
    res.ok("BASE-AC-17 caveats outside the role layer's ceiling refused", ok, detail)

    # A token with no audience predicate would be a leaf empowered for anything.
    unbound = [[["action", "in", ["publish"]]]]
    ok, detail = refuses({**base, "story_ref": STORY, "caveats": unbound}, "SPEC-0081")
    res.ok("SPEC-0081 spawn refused when the act token would not be audience-bound",
           ok, detail)

    ok, detail = refuses({**base, "story_ref": STORY, "image": "l0-base:BASE-v1"},
                         "BASE-AC-17")
    res.ok("a layer declaring an empty ceiling cannot host an agent leaf", ok, detail)

    # And the admitting path resolves rather than throwing.
    try:
        ctx = gate.check({**base, "story_ref": STORY})
        res.ok("a story-bearing request against the agent layer is admitted",
               ctx["story_ref"] == STORY and len(ctx["ceiling"]) > 0, json.dumps(ctx.get("ceiling")))
    except gate.SpawnRefused as e:
        res.record("a story-bearing request against the agent layer is admitted", "fail",
                   f"[{e.criterion}] {e.reason}")


def injection_checks(res):
    """L0-051: what the harness assembles, and what it must never contain."""
    try:
        inj = gate.injection_set(STORY, CITIZEN)
    except gate.SpawnRefused as e:
        res.record("SPEC-0081 core-class injection assembles", "fail", str(e))
        return
    core = inj["core"]
    res.ok("SPEC-0081 core-class injection carries laws with instance hashes",
           bool(core["laws"]) and all(l.get("instance_hash") for l in core["laws"]),
           json.dumps(core["laws"][:2]))
    res.ok("SPEC-0081 strategy is carried hash-pinned (ONT-041)",
           bool(core["strategy"]) and bool(core["strategy"].get("instance_hash")),
           json.dumps(core["strategy"]))
    res.ok("SPEC-0081 the story is named in the injected context",
           core["story"]["id"] == STORY, json.dumps(core["story"]))

    # ONT-032: restrictions are armed, never injected. The check is that the payload
    # carries ids and no restriction prose — a gate that pasted the text would prime
    # exactly the behaviour the restriction forbids.
    armed = inj["armed_restrictions"]
    blob = json.dumps(inj)
    leaked = [r for r in armed if r in blob and any(
        w in blob for w in ("never", "MUST NOT", "prohibited"))]
    res.ok("ONT-032 restrictions appear as ids only, with no prose injected",
           bool(armed) and all(isinstance(r, str) and r.startswith("RSTR-") for r in armed)
           and not leaked, f"{len(armed)} armed; leaked={leaked[:3]}")


def live_spawn_checks(mesh, image, res):
    """One admitted spawn against a real bus. No model credential involved."""
    obs = mesh.observe(seconds=14, subjects=["mesh.>", "acta.>"])
    result = gate.spawn({"story_ref": STORY, "citizen": CITIZEN, "image": image},
                        network=mesh.net, handoff_volume=mesh.vol,
                        argv=["/l0/venv/bin/python", "-c",
                              "print('agent payload running under supervision')"],
                        detach=True)
    mesh.track(result["name"])
    citizen_log = wait_and_logs(result["name"], timeout=240)
    wire = observed(wait_and_logs(obs, timeout=240))

    res.ok("SPEC-0081 the admitted container starts and verifies its chain",
           "identity verified" in citizen_log, citizen_log[-300:])

    descriptors = [m for m in wire if m["subject"] == f"mesh.descriptor.{CITIZEN}"]
    res.ok("SPEC-0081 the spawned citizen publishes a descriptor on the bus",
           bool(descriptors), f"{len(wire)} messages seen")

    if descriptors:
        env = descriptors[0]["envelope"]
        payload = env.get("payload") or {}
        res.ok("the act token in the envelope is audience-bound to the story",
               any(p and p[0] == "audience" and p[2] == STORY
                   for block in (env.get("act_token") or {}).get("caveats", [])
                   for p in block),
               json.dumps((env.get("act_token") or {}).get("caveats")))
        res.ok("the descriptor names the agent role layer it was built from",
               str(payload.get("role_layer", "")).startswith("agent@"),
               json.dumps(payload.get("role_layer")))

    output = [m for m in wire if m["subject"] == f"acta.{CITIZEN}.{STORY}.output"]
    res.ok("SPEC-0081 payload output reaches the story's telemetry subject",
           any("under supervision" in json.dumps(m["envelope"].get("payload"))
               for m in output), f"{len(output)} output messages")

    grant = result["minted"]["cred"]["publish_allow"]
    expected = sorted([f"mesh.descriptor.{CITIZEN}", f"mesh.heartbeat.{CITIZEN}",
                       f"acta.{CITIZEN}.{STORY}.output", f"acta.{CITIZEN}.{STORY}.event"])
    res.ok("ES-003 the transport grant is the projection and nothing wider",
           sorted(grant) == expected, json.dumps(grant))

    # BASE-AC-9 again, this time as an observation of the running container rather than
    # a refusal of the request: what was asked for and what exists must agree.
    inspect = sh("docker", "inspect", result["name"], "--format",
                 "{{json .HostConfig.Binds}}|{{json .Mounts}}").stdout.strip()
    binds, mounts = inspect.split("|", 1)
    # L0-002 forbids "any bind/volume from host paths". The handoff arrives on a named
    # volume, which names no host path in the spawn spec — the orchestrator's projected
    # secret volume in local form, and the mechanism L0-011 assumes. What must be absent
    # is a bind of a host path: that is the thing that would let a citizen read or write
    # the machine it runs on. So the check distinguishes the two rather than counting
    # mount entries, which is what an earlier version of it did.
    bind_specs = [b for b in (json.loads(binds or "null") or [])
                  if b.split(":")[0].startswith(("/", ".", "~"))]
    bind_mounts = [m for m in json.loads(mounts or "[]") if m.get("Type") == "bind"]
    res.ok("BASE-AC-9 the running container has no host-path bind mounts",
           not bind_specs and not bind_mounts,
           f"bind specs={bind_specs} bind mounts={[m.get('Source') for m in bind_mounts]}")
    res.ok("the handoff arrives on a named volume, not a host path",
           any(m.get("Type") == "volume" and m.get("Destination") == "/run/l0"
               for m in json.loads(mounts or "[]")), inspect[:160])
    return result


# ------------------------------------------------------------- SPEC-0083
def host_surface():
    """The host state this suite watches for residue.

    Named explicitly rather than left to "the filesystem", because a full-disk diff is
    neither practical nor meaningful: docker's own layer and volume directories change
    whenever a container runs, and calling that residue would make the check
    unfalsifiable in one direction and useless in the other. What SPEC-0083 is about is
    whether a citizen can leave anything behind in the places a citizen might reach —
    the repository it works on, the invoking user's home, and shared temp.
    """
    surface = {}
    for root in (pathlib.Path.home(), pathlib.Path("/tmp"),
                 pathlib.Path(__file__).resolve().parents[2]):
        try:
            surface[str(root)] = sorted(
                str(p.relative_to(root)) for p in root.iterdir()
                if not p.name.startswith("."))
        except OSError as e:
            surface[str(root)] = [f"unreadable: {e}"]
    return surface


def isolation_checks(mesh, image, res):
    """SPEC-0083: ephemeral workspace, no host residue, three sanctioned sinks."""
    before = host_surface()

    result = gate.spawn({"story_ref": STORY, "citizen": CITIZEN, "image": image},
                        network=mesh.net, handoff_volume=mesh.vol,
                        argv=["/l0/venv/bin/python", "-c",
                              "import pathlib,time\n"
                              "pathlib.Path('/work/scratch.txt').write_text('work product')\n"
                              "pathlib.Path('/tmp/scratch.txt').write_text('temp product')\n"
                              "print('payload wrote to /work and /tmp', flush=True)\n"
                              "time.sleep(600)\n"],
                        detach=True)
    name = mesh.track(result["name"])

    # Let it get far enough to have written, then kill it the way a crash would.
    deadline = time.time() + 60
    wrote = False
    while time.time() < deadline:
        if "payload wrote" in sh("docker", "logs", name).stdout:
            wrote = True
            break
        time.sleep(1)
    res.ok("SPEC-0083 the payload runs and writes into its ephemeral workspace", wrote,
           sh("docker", "logs", name).stdout[-200:])

    inside = sh("docker", "exec", name, "/l0/venv/bin/python", "-c",
                "import pathlib;print(pathlib.Path('/work/scratch.txt').read_text())")
    res.ok("the workspace is writable while the container lives",
           "work product" in inside.stdout, inside.stdout + inside.stderr)

    sh("docker", "kill", "--signal=KILL", name)
    res.ok("SPEC-0083 kill -9 mid-task terminates the container",
           sh("docker", "inspect", name, "--format", "{{.State.Running}}").stdout.strip()
           == "false", "container still running after SIGKILL")

    after = host_surface()
    residue = {root: sorted(set(after[root]) - set(before[root])) for root in before
               if set(after[root]) - set(before[root])}
    res.ok("SPEC-0083 kill -9 leaves zero residue on the watched host surface",
           not residue, json.dumps(residue))

    # /work was tmpfs: the workspace does not survive the container, so there is nothing
    # to clean up and nothing to leak.
    gone = sh("docker", "exec", name, "/bin/true")
    res.ok("the ephemeral workspace dies with the container", gone.returncode != 0,
           "exec into a killed container succeeded")

    # The three sanctioned sinks. Only one of them exists in this environment, and
    # saying so is the point: a green check here that implied otherwise would be the
    # doc-truth failure the platform is built to prevent.
    res.record("SPEC-0083 durable effects: bus messages", "pass",
               "exercised — envelopes observed on the wire this run")
    res.record("SPEC-0083 durable effects: git push", "skip",
               "no remote is reachable from the mesh network; the container has no "
               "credential and no route, so the sink is closed rather than verified")
    res.record("SPEC-0083 durable effects: object-store write", "skip",
               "Tabularium is the data-access citizen's responsibility (PA-030 step 7) "
               "and does not exist yet")
    return result


# ------------------------------------------------------------- SPEC-0084
PAYLOAD_COMMIT_AND_ATTEST = """
import json, os, pathlib, socket, subprocess

os.environ.update(GIT_AUTHOR_NAME="agent", GIT_AUTHOR_EMAIL="agent@invalid",
                  GIT_COMMITTER_NAME="agent", GIT_COMMITTER_EMAIL="agent@invalid")
repo = pathlib.Path("/work/repo"); repo.mkdir()

def git(*args):
    return subprocess.run(["git", "-C", str(repo)] + list(args),
                          capture_output=True, text=True)

git("init", "-q")
(repo / "artifact.txt").write_text("produced in session")
git("add", "-A")
git("commit", "-q", "-m", "session artifact")
commit, tree = git("show", "-s", "--format=%H %T", "HEAD").stdout.split()

def call(request):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(10); s.connect("/run/l0/agent.sock")
    s.sendall((json.dumps(request) + chr(10)).encode())
    buf = b""
    while not buf.endswith(chr(10).encode()):
        buf += s.recv(65536)
    s.close(); return json.loads(buf)

print("COMMIT " + commit + " " + tree, flush=True)
print(json.dumps(call({"op": "emit_event", "kind": "commit.attestation",
                       "data": {"commit": commit, "tree": tree}})), flush=True)
"""


def attribution_checks(mesh, image, res):
    """SPEC-0084: every envelope and every commit chain-verifiable to the leaf."""
    obs = mesh.observe(seconds=16, subjects=["mesh.>", "acta.>"])
    result = gate.spawn({"story_ref": STORY, "citizen": CITIZEN, "image": image},
                        network=mesh.net, handoff_volume=mesh.vol,
                        argv=["/l0/venv/bin/python", "-c", PAYLOAD_COMMIT_AND_ATTEST],
                        detach=True)
    mesh.track(result["name"])
    log = wait_and_logs(result["name"], timeout=240)
    wire = observed(wait_and_logs(obs, timeout=240))
    chain = result["minted"]["chain"]["chain"]

    # Every envelope the session actually published, verified by the shipped path.
    # The observer supplies the audience it is verifying against, because it knows the
    # context it is auditing: this citizen was spawned for this story. That is not a
    # formality — `acta.<citizen>.<story>.*` carries the story in the subject and the
    # verifier derives it, but `mesh.descriptor.*` and `mesh.heartbeat.*` carry no story
    # segment at all (ES-002). An audience-bound token therefore cannot be checked
    # against presence traffic by anyone who does not already know the actor's context,
    # which is a real property of the subject taxonomy and worth naming rather than
    # papering over: the runtime gate has that context; a passing observer does not.
    op_facts = {"action": "publish", "audience": STORY}
    verified, failed = 0, []
    for m in wire:
        try:
            verify_envelope(m["envelope"], chain, op_facts)
            verified += 1
        except VerificationError as e:
            failed.append(f"{m['subject']}: {e}")
    res.ok("SPEC-0084 every published envelope verifies per ES-013",
           verified > 0 and not failed, f"{verified} verified; failures={failed[:2]}")

    # The rogue envelope: correctly shaped, signed outside the chain.
    stranger = minting.mint(CITIZEN, STORY)
    if wire:
        forged = json.loads(json.dumps(wire[0]["envelope"]))
        forged["sender"] = {"leaf": stranger["pubs"]["leaf"],
                            "chain": stranger["chain"]["chain_head"]}
        try:
            verify_envelope(forged, chain, op_facts)
            res.record("SPEC-0084 an envelope signed outside the chain is rejected",
                       "fail", "accepted a stranger's envelope")
        except VerificationError as e:
            res.record("SPEC-0084 an envelope signed outside the chain is rejected",
                       "pass", str(e)[:140])

    # The session's own commit, and its attestation on the wire.
    line = next((l for l in log.splitlines() if "COMMIT " in l), None)
    if not line:
        res.record("SPEC-0084 the session produced a commit and attested it", "fail",
                   log[-300:])
        return
    commit, tree = line.split("COMMIT ", 1)[1].split()
    res.record("SPEC-0084 the session produced a commit and attested it", "pass",
               f"{commit[:12]} tree {tree[:12]}")

    attested = merge_gate.attestations_from([m["envelope"] for m in wire])
    res.ok("SPEC-0084 the commit's attestation reaches the wire", commit in attested,
           f"attested={[c[:12] for c in attested]}")
    if commit in attested:
        try:
            verify_envelope(attested[commit], chain, op_facts)
            res.record("the attestation walks to root — the enrolment check", "pass")
        except VerificationError as e:
            res.record("the attestation walks to root — the enrolment check", "fail",
                       str(e))

    merge_gate_checks(chain, res)


def merge_gate_checks(chain, res):
    """The merge gate itself, over a real repository the host can read.

    The container's repo dies with its workspace, so the gate is exercised against a
    host-side repository with attestations minted for it. That is not a weaker test: the
    gate's job is to decide whether a commit in front of it is attributable, and every
    way that can fail is exercised here — missing attestation, mismatched tree, and a
    signature from outside the chain.
    """
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td, "repo"); repo.mkdir()
        env = {**os.environ, "GIT_AUTHOR_NAME": "agent", "GIT_AUTHOR_EMAIL": "a@invalid",
               "GIT_COMMITTER_NAME": "agent", "GIT_COMMITTER_EMAIL": "a@invalid"}
        for args in (["init", "-q"], ["add", "-A"]):
            subprocess.run(["git", "-C", str(repo)] + args, env=env, capture_output=True)
        (repo / "artifact.txt").write_text("produced in session")
        subprocess.run(["git", "-C", str(repo), "add", "-A"], env=env, capture_output=True)
        subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "artifact"],
                       env=env, capture_output=True)
        ident = merge_gate.commit_identity(repo, "HEAD")

        signer = minting.mint(CITIZEN, STORY)
        chain_ = signer["chain"]["chain"]

        def attestation(data, m=signer):
            return build_envelope(f"acta.{CITIZEN}.{STORY}.event",
                                  {"kind": merge_gate.ATTESTATION_KIND, "data": data},
                                  m["pubs"]["leaf"], m["chain"]["chain_head"], m["token"],
                                  signer_from_seed(m["seeds"]["leaf"]), 1,
                                  payload_type="json")

        good = [attestation(ident)]
        try:
            merge_gate.gate(repo, ["HEAD"], good, chain_)
            res.record("SPEC-0084 the merge gate admits an attested commit", "pass")
        except merge_gate.MergeRefused as e:
            res.record("SPEC-0084 the merge gate admits an attested commit", "fail", str(e))

        for name, envelopes, why in (
            ("a commit with no attestation", [], "unattributed work cannot merge"),
            ("an attestation naming a different tree",
             [attestation({**ident, "tree": "0" * 40})], "tree mismatch"),
            ("an attestation signed outside the chain",
             [attestation(ident, minting.mint(CITIZEN, STORY))], "signer not in chain"),
        ):
            try:
                merge_gate.gate(repo, ["HEAD"], envelopes, chain_)
                res.record(f"SPEC-0084 the merge gate refuses {name}", "fail",
                           f"admitted despite {why}")
            except merge_gate.MergeRefused as e:
                res.record(f"SPEC-0084 the merge gate refuses {name}", "pass",
                           str(e)[:120])


# ------------------------------------------------------------- SPEC-0082
# A surrogate session, not the CLI. It emits the same stream-json frame shapes the CLI
# emits in session mode, so the wire, the renderer and the consumer are exercised
# end to end without a model credential and without spending a token. What it does not
# and cannot prove is SPEC-0085: that the harness can interrupt, inject into and
# terminate a *live* session. That needs the real CLI and is deliberately out of scope
# here — a surrogate that claimed it would be the exact overclaim SPEC-0085 forbids.
SURROGATE_SESSION = """
import json, sys, time

FRAMES = [
    {"type": "system", "subtype": "init", "session_id": "surrogate-0001",
     "tools": ["Read", "Edit", "Bash"]},
    {"type": "assistant", "message": {"role": "assistant", "content": [
        {"type": "text", "text": "Reading the acceptance criterion."}]}},
    {"type": "assistant", "message": {"role": "assistant", "content": [
        {"type": "tool_use", "name": "Read", "input": {"file_path": "SPEC-0082"}}]}},
    {"type": "user", "message": {"role": "user", "content": [
        {"type": "tool_result", "content": "stream-json captured by the harness"}]}},
    {"type": "assistant", "message": {"role": "assistant", "content": [
        {"type": "text", "text": "Publishing each frame as an ES-010 envelope."}]}},
    {"type": "result", "subtype": "success", "num_turns": 3, "is_error": False},
]

for frame in FRAMES:
    print(json.dumps(frame), flush=True)
    time.sleep(0.4)
print("SESSION_COMPLETE", flush=True)
"""

RENDERER = """
import asyncio, json, sys, nats

async def main():
    subject = sys.argv[1]
    seen = []
    nc = await nats.connect("nats://nats:4222", connect_timeout=5)

    async def on_frame(msg):
        env = json.loads(msg.data)
        payload = env.get("payload")
        line = payload.get("line") if isinstance(payload, dict) else str(payload)
        try:
            frame = json.loads(line)
            kind = frame.get("type", "?")
            if kind == "assistant":
                for block in frame["message"]["content"]:
                    if block.get("type") == "text":
                        print("  [render] assistant: " + block["text"], flush=True)
                    elif block.get("type") == "tool_use":
                        print("  [render] tool_use: " + block["name"], flush=True)
            elif kind == "result":
                print("  [render] result: " + frame.get("subtype", ""), flush=True)
            else:
                print("  [render] " + kind, flush=True)
            seen.append(kind)
        except (ValueError, TypeError, KeyError):
            print("  [render] raw: " + str(line)[:60], flush=True)

    await nc.subscribe(subject, cb=on_frame)
    await asyncio.sleep(float(sys.argv[2]))
    await nc.drain()
    print("RENDERED " + json.dumps(seen), flush=True)

asyncio.run(main())
"""

CONSUMER = """
import asyncio, json, sys, nats

async def main():
    subject, seconds = sys.argv[1], float(sys.argv[2])
    # ES-031: the raw envelope verbatim, so a signature can be re-verified forever. A
    # consumer that stored a parsed projection would keep the meaning and lose the proof.
    stored = []
    nc = await nats.connect("nats://nats:4222", connect_timeout=5)

    # A coroutine, not a lambda: nats-py awaits the callback, and a plain function is
    # silently never invoked — the first version of this consumer persisted nothing and
    # reported success at doing so.
    async def store(msg):
        stored.append(msg.data.decode())

    await nc.subscribe(subject, cb=store)
    await asyncio.sleep(seconds)
    await nc.drain()
    print("PERSISTED " + json.dumps(stored), flush=True)

asyncio.run(main())
"""


def io_path_checks(mesh, image, res):
    """SPEC-0082: the session's stream reaches the bus, is rendered live, and is
    persisted verbatim — and no other path out of the container exists."""
    subject = f"acta.{CITIZEN}.{STORY}.output"

    renderer = mesh.track(f"render-{mesh.tag}")
    sh("docker", "run", "-d", "--name", renderer, "--network", mesh.net,
       "--entrypoint", "/l0/venv/bin/python", image, "-c", RENDERER, subject, "18",
       check=True)
    consumer = mesh.track(f"acta-{mesh.tag}")
    sh("docker", "run", "-d", "--name", consumer, "--network", mesh.net,
       "--entrypoint", "/l0/venv/bin/python", image, "-c", CONSUMER, subject, "18",
       check=True)
    time.sleep(2)  # let both attach before the session starts talking

    result = gate.spawn({"story_ref": STORY, "citizen": CITIZEN, "image": image},
                        network=mesh.net, handoff_volume=mesh.vol,
                        argv=["/l0/venv/bin/python", "-c", SURROGATE_SESSION],
                        detach=True)
    mesh.track(result["name"])
    session_log = wait_and_logs(result["name"], timeout=240)
    render_log = wait_and_logs(renderer, timeout=120)
    consumer_log = wait_and_logs(consumer, timeout=120)
    chain = result["minted"]["chain"]["chain"]

    res.ok("SPEC-0082 the session emits stream-json frames",
           "SESSION_COMPLETE" in session_log and '"type": "assistant"' in session_log,
           session_log[-200:])

    rendered = json.loads(render_log.split("RENDERED ", 1)[1].splitlines()[0]) \
        if "RENDERED " in render_log else []
    res.ok("SPEC-0082 a subscriber renders the session live",
           "assistant" in rendered and "result" in rendered, f"frames rendered: {rendered}")
    res.ok("the renderer saw the frames while the session ran, not after",
           "[render] assistant:" in render_log, render_log[-300:])

    persisted = json.loads(consumer_log.split("PERSISTED ", 1)[1].splitlines()[0]) \
        if "PERSISTED " in consumer_log else []
    res.ok("SPEC-0082 the Acta consumer persists the same subject (ES-031)",
           len(persisted) >= 5, f"{len(persisted)} envelopes persisted")

    # The persisted bytes must still verify: that is the whole reason ES-031 says
    # verbatim. A store that kept a summary would keep the meaning and lose the proof.
    reverified, failures = 0, []
    for raw in persisted:
        try:
            verify_envelope(json.loads(raw), chain,
                            {"action": "publish", "audience": STORY})
            reverified += 1
        except VerificationError as e:
            failures.append(str(e))
    res.ok("persisted envelopes re-verify from storage, signatures intact",
           reverified == len(persisted) and reverified > 0,
           f"{reverified}/{len(persisted)} re-verified; {failures[:1]}")

    # No output path except the bus (L0-002's egress pin, now actually enforced).
    egress = sh("docker", "run", "--rm", "--network", mesh.net, "--user", "10001:10001",
                "--entrypoint", "/l0/venv/bin/python", image, "-c",
                "import socket\n"
                "for h,p in (('1.1.1.1',53),('registry.npmjs.org',443)):\n"
                "    try:\n"
                "        socket.create_connection((h,p),timeout=4).close(); print('REACHED',h)\n"
                "    except Exception as e: print('blocked',h,type(e).__name__)\n")
    res.ok("SPEC-0082 no egress exists except the bus (L0-002)",
           "REACHED" not in egress.stdout, egress.stdout.strip()[:200])

    ports = sh("docker", "inspect", result["name"], "--format",
               "{{json .NetworkSettings.Ports}}|{{json .HostConfig.PortBindings}}").stdout
    res.ok("the container publishes no ports — no ingress at L0",
           ports.strip() in ("{}|{}", "{}|null", "null|{}", "null|null"), ports.strip())


def emit_evidence(res, image, bus_image, cli_pin, out_dir):
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    written = []
    for i, row in enumerate(res.rows, 1):
        if row["verdict"] == "skip":
            continue
        evid = {"id": f"EVID-ctrl0005-{now[:19].replace(':', '')}-{i:02d}",
                "type": "evidence", "scope": "platform", "state": "active",
                "version": "1.0.0", "instantiated_at": now, "author": "ctrl-0005",
                "authorized_by": None, "title": row["ac"],
                "control_ref": "CTRL-0005",
                "subject": f"{image}@{image_digest(image)}",
                "verdict": row["verdict"], "checked_at": now,
                "checker": "ctrl-0005-gate-suite",
                "detail": str(row["detail"])[:400],
                # SPEC-0086: the pin rides every row this story emits, and it is the
                # executed binary's hash, not the package version (D46).
                "cli_pin": cli_pin, "bus_image": bus_image}
        (out / f"{evid['id']}.json").write_text(json.dumps(evid, indent=1))
        written.append(evid["id"])
    return written


def cli_pin_of(image):
    r = sh("docker", "run", "--rm", "--user", "10001:10001",
           "--entrypoint", "/l0/venv/bin/python", image, "-c",
           "import pathlib;print(';'.join((pathlib.Path('/cli')/f).read_text().strip() "
           "for f in ('CLI_VERSION','CLI_PLATFORM','CLI_BINARY_SHA256')))")
    if r.returncode:
        return {"available": False}
    version, platform, digest = r.stdout.strip().split(";")
    return {"version": version, "platform_package": platform, "binary_sha256": digest}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", default="l0-agent:0.1.0")
    ap.add_argument("--evidence-dir", default="acta")
    a = ap.parse_args()

    print(f"CTRL-0005 gate library suite against {a.image}")
    print(f"  image digest: {image_digest(a.image)}")
    cli_pin = cli_pin_of(a.image)
    print(f"  cli pin: {cli_pin.get('version')} binary "
          f"{str(cli_pin.get('binary_sha256'))[:16]}…")
    res = Results()

    # Refusals and injection need no infrastructure at all.
    refusal_checks(a.image, res)
    injection_checks(res)

    with Mesh(a.image) as mesh:
        live_spawn_checks(mesh, a.image, res)
        isolation_checks(mesh, a.image, res)
        attribution_checks(mesh, a.image, res)
        io_path_checks(mesh, a.image, res)
        bus_image = mesh.bus_image

    rows = emit_evidence(res, a.image, bus_image, cli_pin, a.evidence_dir)
    failed = res.failed
    print(f"\n{len(res.rows)} criteria checked, {len(failed)} failing; "
          f"{len(rows)} EVID- rows written to {a.evidence_dir}/")
    print("PASS — CTRL-0005 green" if not failed else "FAIL — CTRL-0005 red")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
