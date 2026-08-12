#!/usr/bin/env python3
"""CTRL-0004 — the citizenship conformance suite (DOC-0003 §6).

Runs against a derived image and checks BASE-AC-1 … BASE-AC-16. Each AC emits an
EVID- row against the image digest, per SPEC-0073.

BASE-AC-9 and BASE-AC-17 are *not* here: they are harness-tested refusals and
moved to STORY-0002 / SPEC-0081 v1.1.0 under D5. The suite reports them as
out-of-scope rather than silently omitting them, so a reader of the evidence can
tell the difference between "passed" and "not run here".

Usage:
    python3 suite/citizenship/run.py --image l0-hello:dev
    python3 suite/citizenship/run.py --image l0-violating:dev --expect-fail

Host requirements: docker, plus the pinned tool dependencies (tools/requirements.txt).
The second one is new and deliberate — minting moved to the harness, so the host signs
the handoff and only the resulting files cross into a container. Before that, every
citizen image carried a credential factory it must never be able to use (ENT-003).

The bus, the observer and the citizen still run as containers, nothing is installed
into an image, and no host path is bound into a citizen.
"""
import argparse
import datetime
import json
import pathlib
import re
import subprocess
import sys
import uuid

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "harness"))

import mint as minting  # noqa: E402  — the single minter lives with the spawner
from mesh import (NATS_FALLBACK, NATS_IMAGE, Mesh as BaseMesh,  # noqa: E402
                  image_digest, observed, sh, wait_and_logs)

# The bus is adopted infrastructure, admitted by digest-pinned allowlist (PA-013).
# Resolved 2026-08-11 from nats:2.10-alpine; a versioned measurement like any other
# pin. If this digest cannot be pulled the suite says so in its output and records
# what it actually used in every evidence row — it never silently substitutes.
CITIZEN = "hello-citizen"
CONTEXT = "story-0001"
HEARTBEAT_S = 2


class Results:
    def __init__(self):
        self.rows = []

    def record(self, ac, verdict, detail=""):
        self.rows.append({"ac": ac, "verdict": verdict, "detail": detail})
        mark = {"pass": "PASS", "fail": "FAIL", "skip": "SKIP"}[verdict]
        print(f"  {mark}  {ac}{'' if verdict == 'pass' else '  — ' + str(detail)[:300]}")

    def ok(self, ac, cond, detail=""):
        self.record(ac, "pass" if cond else "fail", detail)
        return cond

    @property
    def failed(self):
        return [r for r in self.rows if r["verdict"] == "fail"]


class Mesh(BaseMesh):
    """The citizenship suite's mesh: the shared one plus a citizen spawn and a handoff
    minted on the host, since the minter no longer ships inside the image (ENT-003)."""

    def mint(self, break_chain=False, expired_lease=False):
        """Deliver L0-011's three files into the handoff volume.

        Previously a helper container ran a minter copied into the image, which meant
        every citizen carried a credential factory it must never be able to use. The
        harness mints on the host now and only the resulting files cross the boundary.
        """
        m = minting.mint(CITIZEN, CONTEXT,
                         lease_age_hours=72 if expired_lease else 0,
                         lease_ttl_hours=48)
        if break_chain:
            sig = m["token"]["parent_sig"]
            m["token"]["parent_sig"] = ("A" if sig[0] != "A" else "B") + sig[1:]
        payload = json.dumps({"leaf.cred": m["cred"], "leaf.token": m["token"],
                              "chain.pub": m["chain"]})
        writer = ("import json,os,sys,pathlib\n"
                  "d=pathlib.Path('/handoff'); d.mkdir(parents=True,exist_ok=True)\n"
                  "for name,content in json.loads(sys.argv[1]).items():\n"
                  "    p=d/name; p.write_text(json.dumps(content))\n"
                  "    os.chown(p,10001,10001); os.chmod(p,0o400)\n"
                  "os.chown(d,10001,10001)\n")
        name = self.track(f"mint-{self.tag}-{uuid.uuid4().hex[:4]}")
        return sh("docker", "run", "--name", name, "--user", "0",
                  "-v", f"{self.vol}:/handoff", "--entrypoint", "/l0/venv/bin/python",
                  self.image, "-c", writer, payload)

    def run_citizen(self, argv, handoff=True, extra_env=None, detach=True):
        """The spawn spec the harness will one day produce. Note what is absent:
        no host bind, no capability, no privilege escalation, no writable rootfs."""
        name = self.track(f"citizen-{self.tag}-{uuid.uuid4().hex[:4]}")
        args = ["docker", "run", "--name", name, "--network", self.net,
                "--read-only", "--cap-drop", "ALL",
                "--security-opt", "no-new-privileges",
                "--user", "10001:10001",
                "--tmpfs", "/work:rw,mode=1777",
                "--tmpfs", "/tmp:rw,mode=1777",
                "-e", f"L0_CITIZEN={CITIZEN}", "-e", f"L0_CONTEXT={CONTEXT}",
                "-e", f"L0_AUDIENCE={CONTEXT}", "-e", "L0_BUS_URL=nats://nats:4222",
                "-e", f"L0_HEARTBEAT_S={HEARTBEAT_S}",
                "-e", f"L0_IMAGE_DIGEST={image_digest(self.image)}"]
        if handoff:
            args += ["-v", f"{self.vol}:/run/l0"]
        for k, v in (extra_env or {}).items():
            args += ["-e", f"{k}={v}"]
        args += ["-d"] if detach else []
        args += [self.image] + list(argv)
        r = sh(*args, timeout=240)
        return name, r

def probe_report(text):
    m = re.search(r"PROBE_REPORT (\{.*\})", text)
    return json.loads(m.group(1)) if m else None


# ---------------------------------------------------------------- the checks
def identity_and_handoff(mesh, res):
    """BASE-AC-1, BASE-AC-2 — negatives first: prove the gate refuses before
    proving it admits."""
    _, r = mesh.run_citizen(["/l0/venv/bin/python", "/l0/conformance/probe.py"],
                            handoff=False, detach=False)
    res.ok("BASE-AC-1 no handoff -> non-zero exit, payload never runs",
           r.returncode != 0 and "PROBE_REPORT" not in (r.stdout + r.stderr),
           f"exit={r.returncode}")

    mesh.mint(break_chain=True)
    _, r = mesh.run_citizen(["/l0/venv/bin/python", "/l0/conformance/probe.py"], detach=False)
    broken_ok = r.returncode != 0 and "PROBE_REPORT" not in (r.stdout + r.stderr)

    mesh.mint(expired_lease=True)
    _, r2 = mesh.run_citizen(["/l0/venv/bin/python", "/l0/conformance/probe.py"], detach=False)
    expired_ok = r2.returncode != 0 and "PROBE_REPORT" not in (r2.stdout + r2.stderr)

    res.ok("BASE-AC-2 broken chain and expired lease -> non-zero at init",
           broken_ok and expired_ok,
           f"broken exit={r.returncode} expired exit={r2.returncode}")


def live_citizen(mesh, res):
    """Everything observable about a correctly-started citizen, in one run."""
    mesh.mint()
    rogue = {"subject": f"work.story.{CONTEXT}.assign",
             "data": {"env_version": 1, "subject": f"work.story.{CONTEXT}.assign",
                      "sender": {"leaf": "AAAA", "chain": "lease"}, "sent_at": "2026-01-01T00:00:00Z",
                      "seq": 1, "act_token": {}, "payload_type": "text",
                      "payload": "rogue", "sig": "AAAA"}}
    obs = mesh.observe(seconds=14, publish_after=rogue)
    name, _ = mesh.run_citizen(["/l0/venv/bin/python", "/l0/conformance/probe.py"],
                               extra_env={"L0_PROBE_DELAY_S": "6"})
    citizen_log = wait_and_logs(name, timeout=240)
    wire = observed(wait_and_logs(obs, timeout=240))
    report = probe_report(citizen_log)

    if not report:
        res.record("BASE-AC-3..8,12,14 probe report", "fail", citizen_log[-500:])
        return wire, None

    res.ok("BASE-AC-3 no credential material in payload namespace",
           report["credentials"]["credential_files_visible"] == [],
           report["credentials"])
    res.ok("BASE-AC-6 uid/gid 10001, caps empty, no-new-privileges",
           report["uid"] == 10001 and report["gid"] == 10001
           and report["caps"]["cap_eff"] == "0000000000000000"
           and report["caps"]["no_new_privs"] == "1", report["caps"] | {"uid": report["uid"]})
    writes = report["writes"]
    res.ok("BASE-AC-7 read-only rootfs, /work and /tmp writable",
           writes["/work/.probe"] == "writable" and writes["/tmp/.probe"] == "writable"
           and all(v.startswith("refused") for k, v in writes.items()
                   if k not in ("/work/.probe", "/tmp/.probe")), writes)
    res.ok("BASE-AC-8 no shell in the final stage", report["shells_found"] == [],
           report["shells_found"])

    ops = report["socket_ops"]
    res.ok("BASE-AC-4 socket publish produces a verifiable envelope",
           ops["granted_publish"].get("ok") is True, ops["granted_publish"])
    res.ok("BASE-AC-5 publish outside the grant refused locally",
           ops["ungranted_publish"].get("ok") is False
           and ops["off_taxonomy_publish"].get("ok") is False,
           {"ungranted": ops["ungranted_publish"], "off_taxonomy": ops["off_taxonomy_publish"]})
    minting = report["minting"]
    res.ok("BASE-AC-18 no credential-minting capability in the image",
           not minting["minting_surfaces"] and not minting["mint_module_present"],
           minting)
    res.record("BASE-AC-14 resolve/recall", "pass"
               if ops["resolve"].get("error") == "NOT_AVAILABLE" else "fail",
               "declared interim posture: NOT_AVAILABLE until the data-access citizen exists")
    return wire, report


def wire_checks(wire, res, expect_citizen=True):
    """BASE-AC-10, 11, 12, 13 — read off the bus, not off the citizen's word."""
    descriptors = [m for m in wire if m["subject"] == f"mesh.descriptor.{CITIZEN}"]
    res.ok("BASE-AC-10 signed schema-conformant descriptor observed",
           bool(descriptors) and descriptor_valid(descriptors[0]["envelope"]),
           descriptors[0]["envelope"] if descriptors else "no descriptor on the wire")

    beats = sorted((m for m in wire if m["subject"] == f"mesh.heartbeat.{CITIZEN}"),
                   key=lambda m: m["at"])
    seqs = [m["envelope"]["payload"]["seq"] for m in beats if "payload" in m["envelope"]]
    gaps = [round(b["at"] - a["at"], 2) for a, b in zip(beats, beats[1:])]
    within = all(HEARTBEAT_S * 0.8 <= g <= HEARTBEAT_S * 1.2 for g in gaps)
    res.ok("BASE-AC-11 heartbeats at declared cadence +/-20%, seq monotonic",
           len(beats) >= 3 and seqs == sorted(seqs) and len(set(seqs)) == len(seqs) and within,
           {"count": len(beats), "gaps": gaps, "seqs": seqs})

    out = [m for m in wire if m["subject"] == f"acta.{CITIZEN}.{CONTEXT}.output"]
    payloads = json.dumps([m["envelope"].get("payload") for m in out])
    res.ok("BASE-AC-12 payload stdout captured onto the telemetry subject",
           bool(out) and "PROBE_REPORT" in payloads, f"{len(out)} output messages")


def descriptor_valid(env):
    d = env.get("payload") or {}
    required = ("descriptor_version", "entity", "citizen", "image_digest",
                "base_version", "role_layer", "interfaces", "heartbeat")
    return (isinstance(env.get("sig"), str) and all(k in d for k in required)
            and d["base_version"].startswith("BASE-v"))


def dropped_counter(report, res):
    stats = (report or {}).get("socket_ops", {}).get("stats") or {}
    res.record("BASE-AC-13 invalid inbound envelope dropped and counted",
               "pass" if stats.get("dropped_unverified", 0) >= 1 else "fail",
               stats or "probe did not report agentd stats")


def sealing(mesh, res, image):
    """BASE-AC-15, BASE-AC-16 — the layer-sealing negatives (SPEC-0072 v1.1.0)."""
    labels = json.loads(sh("docker", "image", "inspect", image, "--format",
                           "{{json .Config.Labels}}").stdout or "{}")
    res.ok("BASE-AC-16 l0.base_version label present and supported",
           (labels or {}).get("l0.base_version", "").startswith("BASE-v"), labels)

    cfg = json.loads(sh("docker", "image", "inspect", image, "--format",
                        "{{json .Config}}").stdout or "{}")
    user_ok = str(cfg.get("User", "")).startswith("10001")
    # A handoff is single-use: init unlinks the credentials once it has read them
    # (L0-011), so every citizen start needs a freshly minted one. That the second
    # start would otherwise fail is the shredding working, not a suite bug.
    mesh.mint()
    _, r = mesh.run_citizen(["/l0/venv/bin/python", "-c",
                             "import pathlib,os;"
                             "print('SHELLS', [str(p) for p in map(pathlib.Path,"
                             "['/bin/sh','/bin/bash','/bin/busybox']) if p.exists()])"],
                            detach=False)
    shells = "SHELLS []" in (r.stdout + r.stderr)
    res.ok("BASE-AC-15 image re-adding shell/root/caps fails the suite",
           user_ok and shells, {"user": cfg.get("User"), "shell_probe": r.stdout.strip()[-200:]})


def emit_evidence(res, image, image_dig, bus_image, out_dir):
    """SPEC-0073: an EVID- row per AC against the image digest. Rows land in the
    generated index; publishing them onto acta.evidence.ctrl-0004 needs the gate's
    own minted identity, which is the harness's job in STORY-0002 — recorded here
    as the reason the bus half is not claimed."""
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    written = []
    for i, row in enumerate(res.rows, 1):
        if row["verdict"] == "skip":
            # An AC that did not run has no evidence. Recording it as a verdict
            # would be a claim the suite did not earn (ONT-046: a claim without
            # current evidence is an aspiration, and the query must be able to
            # see that it is one).
            continue
        ac = row["ac"].split()[0]
        evid = {"id": f"EVID-ctrl0004-{now[:19].replace(':', '')}-{i:02d}",
                "type": "evidence", "scope": "platform", "state": "active",
                "version": "1.0.0", "instantiated_at": now,
                "author": "ctrl-0004", "authorized_by": None,
                "title": f"{ac}: {row['ac']}",
                "control_ref": "CTRL-0004", "subject": f"{image}@{image_dig}",
                "verdict": row["verdict"],
                "checked_at": now, "checker": "ctrl-0004-citizenship-suite",
                "acceptance_criterion": ac, "detail": str(row["detail"])[:400],
                "bus_image": bus_image}
        p = out / f"{evid['id']}.json"
        p.write_text(json.dumps(evid, indent=1))
        written.append(p.name)
    return written


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--expect-fail", action="store_true",
                    help="violating fixture: the suite must report failures")
    ap.add_argument("--evidence-dir", default="acta")
    a = ap.parse_args()

    print(f"CTRL-0004 citizenship conformance suite against {a.image}")
    print(f"  image digest: {image_digest(a.image)}")
    res = Results()

    with Mesh(a.image) as mesh:
        identity_and_handoff(mesh, res)
        wire, report = live_citizen(mesh, res)
        wire_checks(wire, res)
        dropped_counter(report, res)
        sealing(mesh, res, a.image)
        bus_image = mesh.bus_image

    res.record("BASE-AC-9  (harness-tested)", "skip", "moved to STORY-0002 / SPEC-0081 v1.1.0")
    res.record("BASE-AC-17 (harness-tested)", "skip", "moved to STORY-0002 / SPEC-0081 v1.1.0")

    rows = emit_evidence(res, a.image, image_digest(a.image), bus_image, a.evidence_dir)
    failed = res.failed
    print(f"\n{len(res.rows)} criteria checked, {len(failed)} failing; "
          f"{len(rows)} EVID- rows written to {a.evidence_dir}/")

    if a.expect_fail:
        print("PASS — violating fixture failed the suite as required"
              if failed else "FAIL — violating fixture passed; the sealing claims are not falsifiable")
        return 0 if failed else 1
    print("PASS — CTRL-0004 green" if not failed else "FAIL — CTRL-0004 red")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
