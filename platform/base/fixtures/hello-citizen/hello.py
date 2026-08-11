#!/l0/venv/bin/python
"""The hello-citizen payload: the smallest thing that is genuinely a citizen.

It speaks only through the agentd socket (L0-020/021) and prints to stdout, which
the base captures onto the telemetry subject (L0-032). It holds no credentials,
opens no bus connection, and knows no subject beyond the ones it was granted.
"""
import json
import os
import socket
import sys

SOCK = os.environ.get("L0_SOCKET", "/run/l0/agent.sock")


def call(request):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.settimeout(10)
        s.connect(SOCK)
        s.sendall((json.dumps(request) + "\n").encode())
        buf = b""
        while not buf.endswith(b"\n"):
            chunk = s.recv(65536)
            if not chunk:
                break
            buf += chunk
    return json.loads(buf.decode())


def main():
    citizen = os.environ.get("L0_CITIZEN", "hello-citizen")
    context = os.environ.get("L0_CONTEXT", "service")
    print(f"hello from {citizen}, context {context}")
    r = call({"op": "publish", "subject": f"acta.{citizen}.{context}.output",
              "payload": {"greeting": "hello, mesh"}, "payload_type": "json"})
    print(f"published: {json.dumps(r)}")
    r = call({"op": "emit_event", "kind": "hello.done", "data": {"ok": True}})
    print(f"event: {json.dumps(r)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
