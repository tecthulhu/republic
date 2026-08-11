#!/l0/venv/bin/python
"""In-container probe for CTRL-0004. Runs as the *payload*, so everything it can
observe is exactly what a payload can observe — which is the point: the hardening
and sealing claims are tested from the position they are supposed to constrain.

Emits one JSON object on stdout. That output also exercises L0-032 (the base
captures payload stdout onto the telemetry subject), so a successful probe run is
simultaneously the evidence for BASE-AC-12.
"""
import json
import os
import pathlib
import socket
import sys

SOCK = "/run/l0/agent.sock"


def caps_and_nnp():
    """BASE-AC-6: capability set empty, no-new-privileges set. Read from the
    kernel's own view rather than from the spawn spec — what was requested and
    what is in force are different claims."""
    out = {"cap_eff": None, "cap_prm": None, "no_new_privs": None}
    try:
        for line in pathlib.Path("/proc/self/status").read_text().splitlines():
            if line.startswith("CapEff:"): out["cap_eff"] = line.split()[1]
            elif line.startswith("CapPrm:"): out["cap_prm"] = line.split()[1]
            elif line.startswith("NoNewPrivs:"): out["no_new_privs"] = line.split()[1]
    except OSError as e:
        out["error"] = str(e)
    return out


def shells_present():
    """BASE-AC-8. Checks PATH and the standard locations, not just one path."""
    names = ("sh", "bash", "ash", "dash", "busybox", "zsh")
    found = []
    roots = ["/bin", "/usr/bin", "/sbin", "/usr/sbin", "/usr/local/bin"]
    roots += [d for d in os.environ.get("PATH", "").split(":") if d]
    for d in dict.fromkeys(roots):
        for n in names:
            p = pathlib.Path(d, n)
            if p.exists():
                found.append(str(p))
    return found


def write_probe():
    """BASE-AC-7: /work and /tmp writable, everything else read-only."""
    results = {}
    for path in ("/work/.probe", "/tmp/.probe", "/etc/.probe", "/l0/.probe", "/.probe"):
        try:
            p = pathlib.Path(path)
            p.write_text("x")
            p.unlink()
            results[path] = "writable"
        except OSError as e:
            results[path] = f"refused: {type(e).__name__}"
    return results


def credential_material():
    """BASE-AC-3: no readable key material in the payload's view."""
    visible = []
    d = pathlib.Path("/run/l0")
    if d.is_dir():
        visible = [str(p) for p in d.iterdir() if p.name.startswith("leaf.") or p.name.endswith(".pub")]
    return {"run_l0_exists": d.is_dir(), "credential_files_visible": visible}


def call(sock_path, request):
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.settimeout(10)
            s.connect(sock_path)
            s.sendall((json.dumps(request) + "\n").encode())
            buf = b""
            while not buf.endswith(b"\n"):
                chunk = s.recv(65536)
                if not chunk:
                    break
                buf += chunk
        return json.loads(buf.decode())
    except Exception as e:  # noqa: BLE001 — the probe reports failures, never raises
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}


def socket_ops():
    import time
    citizen = os.environ.get("L0_CITIZEN", "unknown-citizen")
    context = os.environ.get("L0_CONTEXT", "service")
    # The suite publishes a rogue envelope shortly after start; wait past it so the
    # stats read below reflects a drop that has actually happened (BASE-AC-13).
    time.sleep(float(os.environ.get("L0_PROBE_DELAY_S", "0")))
    return {
        # BASE-AC-4: a message published via the socket carries a valid envelope.
        "granted_publish": call(SOCK, {"op": "publish", "payload_type": "json",
                                       "subject": f"acta.{citizen}.{context}.output",
                                       "payload": {"probe": "granted-publish"}}),
        # BASE-AC-5: outside the credential's grant, refused locally by agentd.
        "ungranted_publish": call(SOCK, {"op": "publish", "subject": "work.directive.someone-else",
                                         "payload": "should never reach the bus"}),
        # ES-002: outside the closed taxonomy entirely.
        "off_taxonomy_publish": call(SOCK, {"op": "publish", "subject": "totally.invented.subject",
                                            "payload": "nope"}),
        # BASE-AC-14: declared interim posture until the data-access citizen exists.
        "resolve": call(SOCK, {"op": "resolve", "id": "DOC-0000"}),
        "recall": call(SOCK, {"op": "recall", "query": "spawn contract"}),
        # BASE-AC-13: agentd's drop counter, read from the payload side — the only
        # thing about a rejected envelope a payload is ever allowed to learn.
        "stats": call(SOCK, {"op": "stats"}),
    }


def main():
    # BASE-AC-1's marker: if this file exists, the payload executed. The suite
    # asserts its *absence* when handoff is incomplete.
    try:
        pathlib.Path("/work/payload-ran").write_text("1")
    except OSError:
        pass

    report = {
        "uid": os.getuid(), "gid": os.getgid(),
        "caps": caps_and_nnp(),
        "shells_found": shells_present(),
        "writes": write_probe(),
        "credentials": credential_material(),
        "socket_present": pathlib.Path(SOCK).exists(),
        "socket_ops": socket_ops(),
        "base_version": pathlib.Path("/l0/BASE_VERSION").read_text().strip()
        if pathlib.Path("/l0/BASE_VERSION").exists() else None,
    }
    print("PROBE_REPORT " + json.dumps(report), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
