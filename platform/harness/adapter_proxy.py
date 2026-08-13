#!/usr/bin/env python3
"""The adapter proxy — the model credential's holder (D47, L0-021, ENT-023).

D47 rules that a model-provider credential may enter the mesh, but never the owner's
personal one, and that the agent "reaches the model through the harness boundary, not
by reading the key". This is that boundary made real rather than described.

The shape:

    agent container            proxy container              api.anthropic.com
    (internal network,   -->   (internal + egress,     -->  (reachable only from
     no key, no route)          holds the key)                the proxy)

The agent holds no credential and has no route off the mesh — it is on an internal
network, so its only reachable peers are the bus and this proxy. The proxy holds the
key, attaches it to outbound requests, and is the single place where the mesh touches
an external entity. That is ENT-023's adapter boundary: only an adapter interface
crosses outward, and only a citizen-class actor holds adapter credentials.

Why a proxy rather than mounting the key into the agent: a key in the agent's
environment is readable by the payload, and payload code that can read a credential can
exfiltrate it — the same reason L0-011 keeps identity keys behind the agentd socket. A
compromised session here can spend the key's budget, which is why D47 caps it, but it
cannot *take* the key.

What this deliberately does not do: inspect, rewrite or filter the traffic. It is a
credential boundary, not a policy engine. Anything resembling authorization belongs in
the gate library where it is governed and evidenced.
"""
import argparse
import http.server
import os
import pathlib
import ssl
import sys
import urllib.error
import urllib.request

UPSTREAM = "https://api.anthropic.com"

# How each provider expects the credential. Parameterised rather than hardcoded,
# because the adapter is a *credential boundary* and not an Anthropic-shaped one:
# ENT-021's adapter archetype covers outbound contracts to external entities in
# general, and a boundary that only works for one vendor would be a proxy pretending
# to be an architecture. Adding a provider is a line here, not a new mechanism.
AUTH_STYLES = {
    "x-api-key": lambda key: {"x-api-key": key, "anthropic-version": "2023-06-01"},
    "bearer": lambda key: {"Authorization": f"Bearer {key}"},
}
# Hop-by-hop headers and the client's own auth: the client never supplies a real
# credential, so anything it sends under these names is discarded rather than forwarded.
STRIP = {"host", "connection", "keep-alive", "transfer-encoding", "upgrade",
         "proxy-authorization", "x-api-key", "authorization", "content-length"}


class Adapter(http.server.BaseHTTPRequestHandler):
    # HTTP/1.1 so responses can be chunked. Streaming is not a nicety here: a proxy that
    # buffers the upstream response hands the client a finished answer, and a session
    # that receives a finished answer cannot be interrupted mid-generation. SPEC-0085's
    # whole subject is in-flight control, so a buffering adapter silently makes the
    # criterion untestable while every individual call still looks correct.
    protocol_version = "HTTP/1.1"
    key = None
    upstream = UPSTREAM
    auth_style = "x-api-key"
    calls = []

    def log_message(self, fmt, *args):  # noqa: A003 — quiet by default; the mesh logs
        sys.stderr.write("[adapter] " + (fmt % args) + "\n")

    def _forward(self, method):
        length = int(self.headers.get("content-length") or 0)
        body = self.rfile.read(length) if length else None
        url = self.upstream + self.path
        headers = {k: v for k, v in self.headers.items() if k.lower() not in STRIP}
        # The credential is attached here and only here.
        headers.update(AUTH_STYLES[self.auth_style](self.key))

        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=300,
                                        context=ssl.create_default_context()) as resp:
                self.send_response(resp.status)
                for k, v in resp.headers.items():
                    if k.lower() not in STRIP:
                        self.send_header(k, v)
                self.send_header("transfer-encoding", "chunked")
                self.end_headers()
                # Chunk-by-chunk, flushed as it arrives: the client sees tokens while
                # the model is still producing them, which is the difference between a
                # session that can be interrupted and a recording that cannot.
                while True:
                    chunk = resp.read(1024)
                    if not chunk:
                        break
                    self.wfile.write(b"%x\r\n%s\r\n" % (len(chunk), chunk))
                    self.wfile.flush()
                self.wfile.write(b"0\r\n\r\n")
                self.wfile.flush()
                Adapter.calls.append((method, self.path, resp.status))
        except urllib.error.HTTPError as e:
            payload = e.read()
            self.send_response(e.code)
            self.send_header("content-type", e.headers.get("content-type", "application/json"))
            self.send_header("content-length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            Adapter.calls.append((method, self.path, e.code))
        except Exception as e:  # noqa: BLE001 — a proxy failure is a 502, not a crash
            msg = f'{{"error":"adapter: {type(e).__name__}"}}'.encode()
            self.send_response(502)
            self.send_header("content-length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg)
            Adapter.calls.append((method, self.path, 502))

    def do_POST(self):  # noqa: N802
        self._forward("POST")

    def do_GET(self):  # noqa: N802
        self._forward("GET")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--key-file", default="/run/l0/adapter/anthropic.key",
                    help="read once at startup; the file is not re-read and its path "
                         "is never passed to the agent")
    ap.add_argument("--upstream", default=UPSTREAM)
    ap.add_argument("--auth-style", default="x-api-key", choices=sorted(AUTH_STYLES),
                    help="how this provider expects the credential")
    a = ap.parse_args()

    key = pathlib.Path(a.key_file).read_text().strip()
    if not key:
        print("adapter: no credential at the handoff path; refusing to start",
              file=sys.stderr)
        return 2
    Adapter.key = key
    Adapter.upstream = a.upstream
    Adapter.auth_style = a.auth_style
    # Read once, then drop the path from the environment so a later reader of this
    # process's env learns nothing about where the credential came from.
    os.environ.pop("ADAPTER_KEY_FILE", None)

    print(f"[adapter] holding a credential of {len(key)} chars; forwarding to "
          f"{a.upstream} using {a.auth_style}", flush=True)
    server = http.server.ThreadingHTTPServer(("0.0.0.0", a.port), Adapter)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main())
