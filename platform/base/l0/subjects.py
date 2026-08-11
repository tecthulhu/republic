"""Subject taxonomy (ES-001/ES-002). The taxonomy is closed.

A subject matching no pattern here is refused locally by agentd before it ever
reaches the bus (BASE-AC-5 lineage) — the closed taxonomy is enforced at the
publishing edge, not merely documented.
"""
import re

TOKEN = r"[a-z0-9-]+"
TRANSITIONS = "minted|active|suspended|retired|revoked"

PATTERNS = tuple(re.compile("^" + p + "$") for p in (
    rf"mesh\.descriptor\.{TOKEN}",
    rf"mesh\.heartbeat\.{TOKEN}",
    rf"mesh\.entity\.{TOKEN}\.({TRANSITIONS})",
    rf"acta\.{TOKEN}\.{TOKEN}\.output",
    rf"acta\.{TOKEN}\.{TOKEN}\.event",
    rf"acta\.evidence\.{TOKEN}",
    rf"acta\.retrieval\.{TOKEN}",
    rf"work\.directive\.{TOKEN}",
    rf"work\.story\.{TOKEN}\.assign",
    rf"work\.story\.{TOKEN}\.result",
    rf"work\.veto\.{TOKEN}",
    r"data\.resolve",
    r"data\.recall",
    rf"data\.query\.{TOKEN}",
))

ROOTS = ("mesh.", "acta.", "work.", "data.")


def in_taxonomy(subject):
    return isinstance(subject, str) and any(p.match(subject) for p in PATTERNS)


def descriptor_subject(citizen): return f"mesh.descriptor.{citizen}"
def heartbeat_subject(citizen): return f"mesh.heartbeat.{citizen}"
def output_subject(citizen, context): return f"acta.{citizen}.{context}.output"
def event_subject(citizen, context): return f"acta.{citizen}.{context}.event"
