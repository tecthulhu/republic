#!/usr/bin/env python3
"""The spawn gate (SPEC-0081, PA-004, L0-050).

One of the three chokepoints the gate library mounts. Everything here happens
*before* a container exists, because a refusal after creation is not a refusal:

  1. no story reference            -> refuse (ENF-0002)
  2. host bind or volume in spec   -> refuse (BASE-AC-9)
  3. caveats outside the ceiling   -> refuse (BASE-AC-17)
  4. unsupported base version      -> refuse (BASE-AC-16 lineage)
  5. otherwise: mint a leaf whose act token is audience-bound to the story,
     project the transport grant (ES-003), assemble the core-class injection
     set (L0-051), and start the container with zero host mounts.

Restriction *text* is never injected (ONT-032): a prohibition in a prompt primes the
behaviour it forbids, so the gate carries RSTR- ids and the injected context never
contains their text.

An earlier version of this paragraph said the gate "evaluates them pre and post". It
does not — nothing in this platform evaluates a restriction around a session, and the
ids travel as knowledge, not as armament. DEC-0007/O2 found the overclaim and rules
that each entry carries `in_force`, uniformly false today, flipping per restriction
only when a real evaluator lands. The sentence is corrected rather than deleted
because the gap it hid is the point.
"""
import argparse
import json
import pathlib
import subprocess
import sys
import uuid

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))

import mint as minting  # noqa: E402
from atom_lint import lint  # noqa: E402
from paths import CORPUS, SCHEMA  # noqa: E402

SUPPORTED_BASE = ("BASE-v1",)

# DEC-0007/D1: the knowledge-plane threshold. Ratified law reaches a citizen whether or
# not a control yet arms around it; binding is an enforcement-plane event and is
# reported per entry rather than deciding membership.
LAW_STATES = ("ratified", "active")


class SpawnRefused(Exception):
    """A refusal is a first-class outcome, not an error path. ENF-0002's on_fail."""

    def __init__(self, reason, criterion=None):
        super().__init__(reason)
        self.reason = reason
        self.criterion = criterion


def resolve_story(story_ref):
    """SPEC-0122: the spawn precondition is *resolvability*, not lifecycle state.

    The reference may arrive as the atom id (STORY-0002) or as the kebab form the
    subject taxonomy uses (story-0002, ES-002). Either must resolve to a real story
    atom; neither is required to be `ratified` or `active`.

    That leniency is deliberate and load-bearing. A story is necessarily `proposed`
    while the work that produces its acceptance evidence is in flight, and ratification
    follows green acceptance — it cannot precede it. A gate demanding ratified law
    before spawning the work that earns ratification is circular, and nothing would
    ever be built through it.

    What is *not* lenient: the reference has to name something real. Until this
    existed the gate accepted any non-empty string, so "no story, no spawn" was
    enforced against the empty string and nothing else.

    A red corpus is a refusal rather than a pass. There is no such thing as resolving
    a reference against a corpus that does not parse, and the honest answer to "does
    this name a story?" when the corpus is unreadable is *refuse*, not *assume yes*
    (ENF-0002 fails closed).
    """
    atoms, errors = lint([str(CORPUS)], str(SCHEMA))
    if errors:
        raise SpawnRefused(f"cannot resolve a story against a red corpus: "
                           f"{len(errors)} findings", "SPEC-0122")
    for candidate in (story_ref, story_ref.upper()):
        entry = atoms.get(candidate)
        if entry and entry[0].get("type") == "story":
            return candidate, entry[0]
    return None, None


def sh(*args, check=False, timeout=180):
    r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    if check and r.returncode:
        raise RuntimeError(f"{' '.join(args)}\n{r.stdout}\n{r.stderr}")
    return r


def image_labels(image):
    r = sh("docker", "image", "inspect", image, "--format", "{{json .Config.Labels}}")
    if r.returncode:
        raise SpawnRefused(f"image not available: {image}")
    return json.loads(r.stdout or "{}") or {}


def ceiling_of(image):
    labels = image_labels(image)
    raw = labels.get("l0.caveat_ceiling")
    if not raw:
        raise SpawnRefused(f"{image} declares no l0.caveat_ceiling", "BASE-AC-17")
    try:
        ceiling = json.loads(raw)
    except ValueError:
        raise SpawnRefused(f"{image} has an unparseable l0.caveat_ceiling", "BASE-AC-17")
    return ceiling, labels


# ---------------------------------------------------------------- the gate
def check(request):
    """Every refusal the gate can make, evaluated before anything is created.

    Returns the resolved spawn context on success; raises SpawnRefused otherwise.
    """
    story = request.get("story_ref")
    if not story:
        # PA-020/L0-050: story-less spawn is the refusal the whole chain rests on. If an
        # agent can run without a story, nothing downstream traces to a directive.
        raise SpawnRefused("spawn request carries no story reference", "SPEC-0081")

    # And the reference must name a story that exists: an unresolvable reference traces
    # to nothing, which is the same failure as no reference at all wearing a plausible
    # string (SPEC-0122).
    resolved_id, story_atom = resolve_story(story)
    if resolved_id is None:
        raise SpawnRefused(
            f"story reference {story!r} resolves to no story atom — a reference that "
            f"names nothing traces to nothing (SPEC-0122)", "SPEC-0122")

    mounts = request.get("mounts") or []
    if mounts:
        # BASE-AC-9. Checked here rather than in the container because by the time the
        # container could object, the mount already exists.
        raise SpawnRefused(
            f"spawn spec requests host mounts, which L0-002 does not permit: {mounts}",
            "BASE-AC-9")

    image = request["image"]
    ceiling, labels = ceiling_of(image)

    base_version = labels.get("l0.base_version")
    if base_version not in SUPPORTED_BASE:
        raise SpawnRefused(
            f"{image} declares base version {base_version!r}, not among {SUPPORTED_BASE}",
            "BASE-AC-16")

    requested = request.get("caveats")
    citizen = request["citizen"]
    if requested is None:
        requested = [
            [["audience", "=", story]],
            [["action", "in", ["boot", "publish", "request", "subscribe-deliver"]]],
            [["lease_age", "<", request.get("lease_ttl_hours", 48)]],
        ]
    exceeds = minting.within_ceiling(requested, ceiling)
    if exceeds:
        # BASE-AC-17 / ENT-022: authority is granted and attenuated, never inferred. A
        # role layer's ceiling is data in its image, so this is checkable rather than
        # a matter of trusting the request.
        raise SpawnRefused(
            f"requested caveat families {exceeds} exceed {image}'s ceiling {ceiling}",
            "BASE-AC-17")

    audience_bound = any(p and p[0] == "audience" for block in requested for p in block)
    if not audience_bound:
        raise SpawnRefused("act token would not be audience-bound (ENT-075/ES-023)",
                           "SPEC-0081")

    return {"story_ref": story, "resolved_story": resolved_id,
            "story_state": story_atom.get("state"), "citizen": citizen, "image": image,
            "ceiling": ceiling, "caveats": requested, "labels": labels}


# ------------------------------------------------------- context injection
def injection_set(story_ref, citizen, strategy_id="STRAT-0001", mandate_id=None):
    """L0-051: the core-class payload, assembled by the harness.

    `core` is laws, strategy and mandate — hash-pinned and re-asserted across context
    cycles. The strategy is carried as an id plus the hash of its resolved instance, so
    a drive-by edit is detectable by the receiving agent (ONT-041) rather than merely
    discouraged.

    Restrictions appear as ids only. Their text is never injected (ONT-032): the gate
    arms them around the session instead.
    """
    atoms, errors = lint([str(CORPUS)], str(SCHEMA))
    if errors:
        raise SpawnRefused(f"refusing to inject from a red corpus: {len(errors)} findings")

    import hashlib

    def instance_hash(aid):
        a, _src, body = atoms[aid]
        return hashlib.sha256(json.dumps({"record": a, "body": body}, sort_keys=True,
                                         default=str).encode()).hexdigest()[:16]

    def of_type(kind, states):
        return sorted(i for i, (a, _s, _b) in atoms.items()
                      if a.get("type") == kind and a.get("state") in states)

    # DEC-0007 / O1-a: ratification, not binding, is the knowledge-plane threshold. A
    # citizen knows the law of the land the moment it is law, whether or not a gate yet
    # enforces it. Today this changes nothing for documents — there are no ratified
    # documents, only active and draft — and moves restrictions from 12 to 16. Recorded
    # here because the filter is right in principle and a no-op in fact, and a reader
    # of this code should not have to measure the corpus to learn that.
    laws = of_type("document", LAW_STATES)
    restrictions = of_type("restriction", LAW_STATES)
    story = atoms[story_ref][0] if story_ref in atoms else None

    core = {
        # DEC-0007 / O2-a: every entry says whether it is in force, so presence in the
        # payload is never read as enforcement. For a document that means `active`
        # rather than merely ratified.
        "laws": [{"id": i, "instance_hash": instance_hash(i),
                  "state": atoms[i][0].get("state"),
                  "in_force": atoms[i][0].get("state") == "active"} for i in laws],
        "strategy": ({"id": strategy_id, "instance_hash": instance_hash(strategy_id)}
                     if strategy_id in atoms else None),
        "mandate": {"id": mandate_id} if mandate_id else None,
        "story": ({"id": story_ref, "title": story.get("title"),
                   "acceptance": story.get("acceptance")} if story else {"id": story_ref}),
        # DEC-0007 / D3: draft is not law and its text never enters the payload. Ids
        # and titles only, so a citizen working near a document that is in flight knows
        # it exists and knows it is not yet binding on anyone.
        "pending_law": [{"id": i, "title": atoms[i][0].get("title"), "state": "draft"}
                        for i in of_type("document", ("draft",))],
    }
    return {
        "core": core,
        # Ids only, never prose: a gate that pasted these would prime what they forbid
        # (ONT-032). `in_force` is uniformly false, and that is a measurement rather
        # than a placeholder — nothing in this platform evaluates a restriction around
        # a session yet. The module docstring above claimed such evaluation existed;
        # it did not, and DEC-0007/O2-b rules that this flag flips per restriction only
        # when an evaluator lands in code, never by declaration.
        "armed_restrictions": [{"id": i, "state": atoms[i][0].get("state"),
                                "in_force": False} for i in restrictions],
        "enforcement_note": "no restriction evaluator exists; in_force is false for all "
                            "(DEC-0007/O2-a). Presence arms nothing yet — it informs.",
        "reference_cues": {"resolve": "/run/l0/agent.sock", "recall": "/run/l0/agent.sock"},
    }


# ------------------------------------------------------------- the spawn
def prepare(request, network=None, handoff_volume=None, argv=None, extra_env=None,
            name=None):
    """Gate, mint, deliver the handoff, and build the run command — without running it.

    Split out from spawn() because a supervised session needs the container's stdin
    (SPEC-0085), which means the caller has to own the process. Everything that makes a
    citizen a citizen still happens here, so a supervised session is not a side door:
    it is gated, minted and injected exactly like a detached one, and it comes up behind
    init with identity verified and telemetry flowing.
    """
    ctx = check(request)
    story, citizen, image = ctx["story_ref"], ctx["citizen"], ctx["image"]

    minted = minting.mint(citizen, story, audience=story,
                          leaf_caveats=ctx["caveats"],
                          publish_allow=minting.transport_grant(citizen, story))
    injection = injection_set(story, citizen, mandate_id=request.get("mandate_ref"))

    tag = uuid.uuid4().hex[:8]
    volume = handoff_volume or f"handoff-{tag}"
    sh("docker", "volume", "create", volume, check=True)
    _deliver_handoff(volume, minted, image)

    container = name or request.get("name") or f"agent-{citizen}-{tag}"
    args = ["docker", "run", "--name", container,
            "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "--user", "10001:10001",
            "--tmpfs", "/work:rw,mode=1777",
            "--tmpfs", "/tmp:rw,mode=1777",
            "-v", f"{volume}:/run/l0",
            "-e", f"L0_CITIZEN={citizen}", "-e", f"L0_CONTEXT={story}",
            "-e", f"L0_AUDIENCE={story}",
            "-e", f"L0_ROLE_LAYER={ctx['labels'].get('l0.role_layer', 'agent@0.1.0')}",
            "-e", f"L0_IMAGE_DIGEST={_digest(image)}"]
    if network:
        args += ["--network", network, "-e", "L0_BUS_URL=nats://nats:4222"]
    for k, v in (extra_env or {}).items():
        args += ["-e", f"{k}={v}"]
    return {"name": container, "volume": volume, "minted": minted,
            "injection": injection, "context": ctx, "args": args,
            "image": image, "argv": list(argv or [])}


def spawn(request, network=None, handoff_volume=None, argv=None, detach=True,
          extra_env=None):
    """Mint, deliver the handoff, and start the container. Never called before check()."""
    plan = prepare(request, network, handoff_volume, argv, extra_env)
    args = list(plan["args"])
    if detach:
        args.append("-d")
    args.append(plan["image"])
    args += plan["argv"]
    r = sh(*args, timeout=240)
    return {**plan, "run": r}


def _digest(image):
    r = sh("docker", "image", "inspect", image, "--format", "{{.Id}}")
    return r.stdout.strip() or "sha256:unknown"


def _deliver_handoff(volume, minted, image):
    """L0-011's three files, written into the handoff volume by a privileged helper.

    The contents are minted on the host and passed in; nothing in the image can produce
    a credential, which is the point of moving the minter out of the citizen (ENT-003).
    """
    payload = json.dumps({"leaf.cred": minted["cred"], "leaf.token": minted["token"],
                          "chain.pub": minted["chain"]})
    writer = (
        "import json,os,sys,pathlib\n"
        "d=pathlib.Path('/handoff'); d.mkdir(parents=True,exist_ok=True)\n"
        "for name,content in json.loads(sys.argv[1]).items():\n"
        "    p=d/name; p.write_text(json.dumps(content))\n"
        "    os.chown(p,10001,10001); os.chmod(p,0o400)\n"
        "os.chown(d,10001,10001)\n")
    r = sh("docker", "run", "--rm", "--user", "0", "-v", f"{volume}:/handoff",
           "--entrypoint", "/l0/venv/bin/python", image, "-c", writer, payload,
           timeout=180)
    if r.returncode:
        raise RuntimeError(f"handoff delivery failed: {r.stdout}\n{r.stderr}")


def main():
    ap = argparse.ArgumentParser(description="spawn gate (SPEC-0081)")
    ap.add_argument("--story", default=None)
    ap.add_argument("--citizen", required=True)
    ap.add_argument("--image", required=True)
    ap.add_argument("--mount", action="append", default=[])
    ap.add_argument("--check-only", action="store_true")
    a = ap.parse_args()
    request = {"story_ref": a.story, "citizen": a.citizen, "image": a.image,
               "mounts": a.mount}
    try:
        ctx = check(request)
    except SpawnRefused as e:
        print(f"REFUSED [{e.criterion or 'gate'}]: {e.reason}")
        return 2
    print(f"admitted: story={ctx['story_ref']} citizen={ctx['citizen']} "
          f"ceiling={len(ctx['ceiling'])} families")
    if a.check_only:
        return 0
    result = spawn(request)
    print(f"started {result['name']} from volume {result['volume']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
