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
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "harness"))

import spawn as gate  # noqa: E402
from mesh import Mesh, image_digest, observed, sh, wait_and_logs  # noqa: E402

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
        bus_image = mesh.bus_image

    rows = emit_evidence(res, a.image, bus_image, cli_pin, a.evidence_dir)
    failed = res.failed
    print(f"\n{len(res.rows)} criteria checked, {len(failed)} failing; "
          f"{len(rows)} EVID- rows written to {a.evidence_dir}/")
    print("PASS — CTRL-0005 green" if not failed else "FAIL — CTRL-0005 red")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
