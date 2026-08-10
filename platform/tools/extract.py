#!/usr/bin/env python3
"""Extraction pass: DOC-0000 + DOC-0005 requirements → atomized corpus.
Classes: prin | spec-m | spec-h | rstr-m | rstr-h. Controls: C1..C8.
Emits corpus/REQUIREMENTS_REGISTER.md, CONTROLS.md, ENFORCEMENT_RULES.md."""
import datetime
NOW = "2026-08-10T12:00:00Z"

# (source, class, control, title)
REQS = [
 # Document 0
 ("ONT-001","prin",None,"Governed atom defined as smallest independently-governed unit"),
 ("ONT-002","spec-h",None,"Genres are serialization containers; governance attaches to atom IDs only"),
 ("ONT-003","spec-m","C1","Scope values conform to platform|project|repo|story grammar"),
 ("ONT-004","spec-h",None,"No intermediate governance layers without an owning artifact"),
 ("ONT-005","spec-m","C1","Entity types never appear in the atom type registry"),
 ("ONT-010","spec-m","C1","Every atom carries the complete base interface with semver version"),
 ("ONT-011","spec-m","C1","IDs unique, correctly prefixed, never reused or renumbered"),
 ("ONT-012","spec-m","C1","Versions immutable past draft; change produces a new version"),
 ("ONT-013","spec-m","C1","No alternative authorship or approval fields on any type"),
 ("ONT-014","prin",None,"Truth is temporal; instances are time-specified statements"),
 ("ONT-015","spec-m","C8","Mutation is a new instance; instance store is append-only"),
 ("ONT-016","rstr-m","C1","No location references; references identify by id/version/time only"),
 ("ONT-017","prin",None,"Documents are assemblies of resolved atoms at a given time"),
 ("ONT-020","spec-h",None,"Components bind to facets, never the full ontology"),
 ("ONT-021","rstr-h",None,"Facets are never widened to satisfy a component"),
 ("ONT-030","spec-m","C1","No rule references a principle as its claim"),
 ("ONT-031","spec-m","C8","Dangling-claim query computable over the index"),
 ("ONT-032","spec-m","C1","Restriction fixed fields (pre+post, injection never) cannot be overridden"),
 ("ONT-033","spec-m","C1","Control implementation references resolve to invocable checkers"),
 ("ONT-034","spec-m","C1","Enforcement ladder closed; no kill value exists"),
 ("ONT-035","spec-m","C1","Every rule is a complete claim+control+enforcement triple"),
 ("ONT-037","prin",None,"Single responsibility per atom; consequences and claims change independently"),
 ("ONT-038","spec-m","C3","No lifecycle transition past proposed without a ratifying decision"),
 ("ONT-039","rstr-m","C1","No model literals anywhere in governed content; band labels only"),
 ("ONT-040","spec-m","C6","Identity leaves never exceed mandate imperium"),
 ("ONT-041","spec-m","C5","Strategy hash-pinned in mandate context and injected at spawn"),
 ("ONT-042","spec-m","C1","Every sprint declares an exit gate control"),
 ("ONT-043","spec-m","C1","Every story references at least one acceptance specification"),
 ("ONT-044","rstr-h",None,"Platform never owns backlog state; tracker is source of truth"),
 ("ONT-045","spec-m","C1","Acceptance criteria are story-scoped SPEC- atoms with tags"),
 ("ONT-046","spec-m","C8","Evidence atoms append-only, never versioned"),
 ("ONT-047","spec-m","C1","Every waiver carries an expiry; gates re-arm on expiry"),
 ("ONT-048","spec-m","C8","Provenance chain walkable end to end from any element"),
 ("ONT-050","spec-m","C1","Relations restricted to the ratified vocabulary"),
 ("ONT-055","spec-m","C1","Exception grammar parses per the given/when/meets/then/for shape"),
 ("ONT-056","spec-m","C1","Exception constructs only on waiver and enforcement atoms"),
 ("ONT-057","rstr-m","C2","No exception grammar in credentials; no limiter caveats as rule exceptions"),
 ("ONT-058","spec-m","C1","Exception instances governed: scope-narrowing, ratified targets, expiring suspends"),
 ("ONT-060","spec-m","C3","All lifecycle transitions conform to the single state machine"),
 ("ONT-061","spec-m","C3","Only decision atoms move other atoms past proposed"),
 ("ONT-062","spec-h",None,"Ratification shape identical across platform and repo scopes"),
 ("ONT-070","spec-m","C1","Atoms parse from frontmatter or marker-delimited blocks"),
 ("ONT-070a","spec-m","C1","Encoding markers pair, never nest, ids match; outside content ungoverned"),
 ("ONT-071","spec-m","C1","Every atom type validates against its versioned JSON Schema"),
 ("ONT-072","spec-m","C1","atom-lint validates every governed file in CI"),
 ("ONT-080","spec-m","C8","Standing queries computable from frontmatter plus evidence alone"),
 ("ONT-085","spec-m","C7","Every persisted instance embedded at persistence; no opt-out path"),
 ("ONT-086","rstr-m","C1","No embedding vectors in authored content"),
 ("ONT-087","spec-m","C7","Embedding chunk boundary is the atom instance"),
 ("ONT-088","spec-m","C7","Every vector row carries full measurement provenance with digest-pinned instrument"),
 ("ONT-089","spec-m","C8","Embedding coverage query computable with target zero"),
 # Document 0.5
 ("ENT-001","spec-h",None,"One entity type only; no human/agent type branching"),
 ("ENT-002","spec-m","C6","Every entity is a node in exactly one root-anchored chain"),
 ("ENT-003","rstr-m","C2","Child credentials never carry capabilities absent from parent grants"),
 ("ENT-004","rstr-m","C6","Authority never inferred, widened, or promoted at runtime"),
 ("ENT-005","spec-m","C6","Human and agent credentials share one shape and verification path"),
 ("ENT-010","rstr-h",None,"Kind never informs authorization, gating, veto, or verification"),
 ("ENT-011","spec-m","C1","Chain position carries parent, depth, caveats in §9 grammar"),
 ("ENT-012","spec-m","C4","Citizenship classes enforced: citizen, adopted, external"),
 ("ENT-013","spec-m","C3","Citizens born via birth process with decision-authorized mandates"),
 ("ENT-020","spec-m","C4","Every interface is a surface-to-contract binding with declared caveat"),
 ("ENT-021","spec-m","C1","Interface archetypes closed at four: bus, request, adapter, human"),
 ("ENT-022","rstr-m","C4","Role layers never reopen what lower layers sealed"),
 ("ENT-023","rstr-m","C4","Only adapter interfaces cross the citizenship boundary outward"),
 ("ENT-030","spec-m","C4","Every citizen publishes a signed self-descriptor at start and on change"),
 ("ENT-031","rstr-h",None,"Descriptors emitted never authored; no hand-maintained registry"),
 ("ENT-032","spec-m","C4","Descriptor validity tested by the citizenship conformance suite"),
 ("ENT-040","spec-m","C4","Interface conformance verified via bound rules producing evidence"),
 ("ENT-041","spec-m","C8","Unverified-interface query joins launch readiness"),
 ("ENT-042","spec-m","C5","Runtime behavior exceeding the descriptor is gated or raised as blocker"),
 ("ENT-050","spec-m","C6","Entity lifecycle transitions conform to minted/active/suspended/retired/revoked"),
 ("ENT-051","spec-m","C2","Revocation walks downward only; parent revocation revokes the subtree"),
 ("ENT-052","spec-m","C8","Every entity transition recorded to provenance with acting identity"),
 ("ENT-070","spec-m","C4","Each persona represented by a citizen-class custodian"),
 ("ENT-071","rstr-m","C6","Persona key never enters the custodian; custodian holds only a lease"),
 ("ENT-072","spec-m","C6","Every verifier checks lease TTL at every chain walk"),
 ("ENT-073","spec-m","C6","Lease renewal requires hardware token presence ceremony"),
 ("ENT-074","spec-m","C2","Lease decay ladder attenuates custodian authority by age thresholds"),
 ("ENT-075","rstr-m","C5","Custodian never originates authority; authority acts need per-act human proof"),
 ("ENT-076","spec-m","C6","Leaf minting requires custodian lease plus fresh device assertion"),
 ("ENT-077","spec-m","C6","Break-glass revocation credential co-signed at each renewal"),
 ("ENT-078","spec-h",None,"Enrollment ceremony: cold root to token to custodian to devices"),
 ("ENT-079","spec-m","C5","Unsigned input is draft; force requires a signed adopting act"),
 ("ENT-091","spec-m","C2","Caveats are conjunctions of guard predicates; no disjunction or else"),
 ("ENT-092","spec-m","C2","Predicates draw only on the fixed five-family fact vocabulary"),
 ("ENT-093","spec-m","C2","Composition is union; attenuation holds algebraically"),
 ("ENT-094","rstr-m","C2","Verification fails closed; unknown facts and failures deny"),
 ("ENT-095","rstr-m","C2","No exception constructs inside credentials"),
 ("ENT-096","spec-m","C7","Caveat display renderings generated from canonical form only"),
 ("ENT-097","spec-h",None,"Grammar carrier-independent; carrier implements without loss"),
]

CONTROLS = {
 "C1": ("CTRL-0001","atom-lint","codebase","tools/atom_lint.py",
        "Parses ONT-070a boundaries and frontmatter, validates schemas, ids, references, fixed fields, model literals, embedding fields, exception placement"),
 "C2": ("CTRL-0002","grammar property suite","artifact","tools/test_grammar.py",
        "Property tests over the caveat algebra: attenuation monotonicity, fail-closed verification, layer separation, downward revocation"),
 "C3": ("CTRL-0003","lifecycle transition checker","codebase","tools/atom_lint.py#transitions",
        "Validates lifecycle transitions in change history against the state machine and decision authorization"),
 "C4": ("CTRL-0004","citizenship conformance suite","runtime","suite/citizenship",
        "Runs against every derived image: hardening, identity init, descriptor, heartbeat, interface conformance, layer sealing"),
 "C5": ("CTRL-0005","gate library suite","runtime","suite/gates",
        "Tests spawn, merge, and runtime gates: story-required spawn, injection order, restriction pre/post, unsigned-input draft rule"),
 "C6": ("CTRL-0006","chain verifier suite","runtime","suite/chain",
        "Tests the identity walk: chain-to-root, lease TTL at every hop, imperium ceilings, two-party minting, break-glass"),
 "C7": ("CTRL-0007","embedder pipeline suite","artifact","tools/test_embedder.py",
        "Tests per-atom chunking, measurement provenance completeness, instrument digest pinning, generated-rendering rule"),
 "C8": ("CTRL-0008","index and query suite","artifact","suite/index",
        "Tests standing queries: dangling claims, unevidenced claims, coverage, provenance walk, append-only store"),
}

def atom(aid, typ, title, extra, tags, prose=""):
    y = [f"id: {aid}", f"type: {typ}", "scope: platform", "state: proposed", "version: 1.0.0",
         f"instantiated_at: \"{NOW}\"", "author: consul-extraction-pass", "authorized_by: null",
         "title: \"" + title + "\"", f"tags: [{', '.join(tags)}]"] + extra
    body = "\n".join(y)
    p = f"\n{prose}\n" if prose else "\n"
    return f"<!-- atom:begin id={aid} -->\n```yaml\n{body}\n```{p}<!-- atom:end id={aid} -->\n"

out = ["# Requirements Register — extraction of DOC-0000 and DOC-0005",
       "",
       "Generated by the extraction pass. Each source requirement is classified and",
       "atomized; machine-checkable claims are bound to controls in",
       "ENFORCEMENT_RULES.md. Class counts and dangling status are computed by the",
       "index, not recorded here (ONT-016: no second source of truth).",""]
counters = {"SPEC":0,"RSTR":0,"PRIN":0}
claims = []  # (atom_id, control_key)
for src, cls, ctl, title in REQS:
    if cls == "prin":
        counters["PRIN"] += 1; aid = f"PRIN-{counters['PRIN']:04d}"
        out.append(atom(aid, "principle", title, ["binding: injected"], [src.lower()]))
    elif cls.startswith("spec"):
        counters["SPEC"] += 1; aid = f"SPEC-{counters['SPEC']:04d}"
        chk = "machine" if cls == "spec-m" else "human"
        out.append(atom(aid, "specification", title, ["binding: checked", f"check: {chk}"], [src.lower()]))
        if ctl: claims.append((aid, ctl))
    else:
        counters["RSTR"] += 1; aid = f"RSTR-{counters['RSTR']:04d}"
        chk = "machine" if cls == "rstr-m" else "human"
        out.append(atom(aid, "restriction", title,
                        ["binding: checked", "phase: pre+post", "injection: never", f"check: {chk}"], [src.lower()]))
        if ctl: claims.append((aid, ctl))
open("corpus/REQUIREMENTS_REGISTER.md","w").write("\n".join(out))

co = ["# Controls",""]
for k,(cid,name,tgt,impl,desc) in CONTROLS.items():
    co.append(atom(cid,"control",name,[f"target: {tgt}",f"implementation: {impl}"],["enforcement-plane"],desc))
open("corpus/CONTROLS.md","w").write("\n".join(co))

er = ["# Enforcements and Rules","",
      atom("ENF-0001","enforcement","Block merge",["on_fail: block-merge"],["ladder"]),
      atom("ENF-0002","enforcement","Refuse spawn",["on_fail: refuse-spawn"],["ladder"]),
      atom("ENF-0003","enforcement","Suspend and escalate",["on_fail: suspend-escalate","escalation_target: tribune-veto-queue"],["ladder"]),
      atom("ENF-0004","enforcement","Advisory",["on_fail: advisory"],["ladder"])]
ENF_FOR = {"C1":"ENF-0001","C2":"ENF-0001","C3":"ENF-0001","C4":"ENF-0001",
           "C5":"ENF-0002","C6":"ENF-0002","C7":"ENF-0001","C8":"ENF-0001"}
n=0
for claim, ctl in claims:
    n+=1; rid=f"RULE-{n:04d}"; cid=CONTROLS[ctl][0]; eid=ENF_FOR[ctl]
    er.append(atom(rid,"rule",f"Bind {claim} via {cid}",
                   [f"claim: {claim}",f"control: {cid}",f"enforcement: {eid}",
                    "relations:",f"  - {{ rel: binds, target: {claim} }}",
                    f"  - {{ rel: binds, target: {cid} }}",f"  - {{ rel: binds, target: {eid} }}"],["binding"]))
open("corpus/ENFORCEMENT_RULES.md","w").write("\n".join(er))
print(f"register: {sum(counters.values())} requirement atoms ({counters}); rules: {n}; controls: {len(CONTROLS)}")
