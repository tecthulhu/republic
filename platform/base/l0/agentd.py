"""/l0/agentd — the one programmatic surface the base exposes upward (L0-020).

A local UNIX socket at /run/l0/agent.sock speaking newline-delimited JSON.
Everything else is sealed (L0-021): no other IPC, no direct bus connection from
payload code, no filesystem interface to credentials, no alternative egress.

agentd runs inside the init process rather than as a separate executable. That
is deliberate and stronger than the alternative: key material stays in exactly
one address space, so BASE-AC-3's claim (no readable key material in the payload
namespace) holds by construction rather than by file permissions. The declared
path L0-004 requires exists and serves the declared socket.

Ops per L0-020. `resolve` and `recall` are served by the data-access citizen over
the bus, which does not exist at step 4 — they return NOT_AVAILABLE, carried as a
declared interim posture per L0 open item (c), never as silence.
"""
import asyncio
import json

import subjects
from chainverify import VerificationError
from envelope import build as build_envelope, verify as verify_envelope

SOCKET_PATH = "/run/l0/agent.sock"
NOT_AVAILABLE = "NOT_AVAILABLE"


class Agentd:
    def __init__(self, ctx):
        self.ctx = ctx                      # L0Context: identity, bus, config
        self.seq = 0
        self.dropped_unverified = 0         # BASE-AC-13: dropped and counted

    # ---- outbound -------------------------------------------------------
    def _refuse(self, reason):
        return {"ok": False, "error": reason}

    async def publish(self, subject, payload, payload_type="text"):
        """Envelope-wrapped, leaf-signed, act-token attached; refused locally if the
        subject is outside the credential's grant (BASE-AC-5) or outside the closed
        taxonomy (ES-002). Local refusal means the message never reaches the bus."""
        if not subjects.in_taxonomy(subject):
            return self._refuse(f"subject outside taxonomy (ES-002): {subject}")
        if not self.ctx.subject_granted(subject):
            return self._refuse(f"subject outside credential grant (ES-003): {subject}")
        self.seq += 1
        env = build_envelope(subject, payload, self.ctx.leaf_pub, self.ctx.chain_head,
                             self.ctx.act_token, self.ctx.signer, self.seq,
                             payload_type=payload_type)
        await self.ctx.bus.publish(subject, json.dumps(env).encode())
        return {"ok": True, "seq": self.seq, "subject": subject}

    async def emit_event(self, kind, data):
        return await self.publish(subjects.event_subject(self.ctx.citizen, self.ctx.context),
                                  {"kind": kind, "data": data}, payload_type="json")

    # ---- inbound --------------------------------------------------------
    def accept_inbound(self, raw):
        """ES-013 / BASE-AC-13: an envelope failing verification is dropped, counted,
        and never delivered to the payload. Returns None on drop."""
        try:
            env = json.loads(raw)
            verify_envelope(env, self.ctx.chain, {"action": "subscribe-deliver"})
            return env
        except (ValueError, VerificationError):
            self.dropped_unverified += 1
            return None

    # ---- socket ---------------------------------------------------------
    async def _dispatch(self, req):
        op = req.get("op")
        if op == "publish":
            return await self.publish(req.get("subject", ""), req.get("payload", ""),
                                      req.get("payload_type", "text"))
        if op == "emit_event":
            return await self.emit_event(req.get("kind", "unspecified"), req.get("data"))
        if op == "subscribe":
            subject = req.get("subject", "")
            if not subjects.in_taxonomy(subject):
                return self._refuse(f"subject outside taxonomy (ES-002): {subject}")
            return {"ok": True, "subscribed": subject}
        if op in ("resolve", "recall"):
            # L0 open item (c): stubbed until the data-access citizen exists.
            return {"ok": False, "error": NOT_AVAILABLE, "op": op,
                    "posture": "interim: resolve/recall await the data-access citizen"}
        if op == "stats":
            return {"ok": True, "seq": self.seq, "dropped_unverified": self.dropped_unverified}
        return self._refuse(f"unknown op: {op}")

    async def _client(self, reader, writer):
        try:
            while line := await reader.readline():
                try:
                    resp = await self._dispatch(json.loads(line))
                except Exception as e:  # noqa: BLE001 — a failed op answers, never crashes agentd
                    resp = {"ok": False, "error": f"{type(e).__name__}: {e}"}
                writer.write((json.dumps(resp) + "\n").encode())
                await writer.drain()
        except (ConnectionResetError, BrokenPipeError):
            pass
        finally:
            writer.close()

    async def serve(self, path=SOCKET_PATH):
        server = await asyncio.start_unix_server(self._client, path=path)
        return server
