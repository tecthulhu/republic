# Grooming & Courier — STORY-0005 / STORY-0006 cut

Two stories for the owner's queue. STORY-0005 grooms the repository into
its intended public shape. STORY-0006 builds the courier: a local MCP
server that bridges document generation (the drafting session) and
delivery (the repo), closing the gap that produced the duplicate-tree
defect and the DOC-0006 omission. Both are post-STORY-0004, neither
blocks enactment.

---

## STORY-0005 — repository grooming

Target tree (the shape the repo presents to a public reader):

```
republic/
├── README.md                  # what this is, status, corpus map, how to read it
├── LICENSE                    # lands via DEC-0002 signing, not here
├── CLAUDE.md                  # bootloader (root, per D4)
├── .gitignore
└── platform/
    ├── corpus/                # governed atoms only
    │   ├── DOC-0000_ontology.md … DOC-0006_liveness_extension.md
    │   ├── DEC-0001.md, DEC-0002.md
    │   ├── REQUIREMENTS_REGISTER.md, CONTROLS.md, ENFORCEMENT_RULES.md
    │   ├── SPAWN_CONTRACT_STORIES.md, MEMORIES_SEED.md
    │   └── correspondence/    # ARCHITECT_RESPONSE_*, worker reports
    ├── schemas/
    ├── tools/                 # + requirements.txt, tests
    └── inbox/                 # courier landing zone (STORY-0006), git-ignored
```

Grooming rules encoded by the SPECs: governed documents follow
`<ID>_<snake_name>.md`; correspondence (responses, reports) moves to
`corpus/correspondence/` — it is governed content (the atoms inside are
law) but shelved apart from the substrate documents so a reader meets
DOC-0000 before ARCHITECT_RESPONSE_002; README is descriptive-class in
spirit (status lines cite evidence subjects rather than asserting
freshness) and hand-written for now with a corpus-rendered version as
the eventual successor, per the CLAUDE.md precedent.

<!-- atom:begin id=STORY-0005 -->
```yaml
id: STORY-0005
type: story
scope: platform
state: proposed
version: 1.1.0
instantiated_at: "2026-08-11T14:50:00Z"
author: agent-worker-story-0008
authorized_by: null
title: "Repository grooming: public shape, naming, README, correspondence shelf"
tags: [grooming]
tracker_ref: "gh:tecthulhu/republic#5"
acceptance: [SPEC-0100, SPEC-0101, SPEC-0102]
```
<!-- atom:end id=STORY-0005 -->

<!-- atom:begin id=SPEC-0100 -->
```yaml
id: SPEC-0100
type: specification
scope: story:story-0005
state: proposed
version: 1.0.0
instantiated_at: "2026-08-11T01:30:00Z"
author: consul-architect
authorized_by: null
title: "Tree matches the target layout; naming convention holds"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0005
```
The repository tree matches the target layout above; every governed
document file matches `<TYPE-NNNN>_<snake>.md` or is an enumerated
register file; whole-tree lint is green with zero duplicate IDs after
the moves (git mv preserves history — no delete/re-add).
<!-- atom:end id=SPEC-0100 -->

<!-- atom:begin id=SPEC-0101 -->
```yaml
id: SPEC-0101
type: specification
scope: story:story-0005
state: proposed
version: 1.0.0
instantiated_at: "2026-08-11T01:30:00Z"
author: consul-architect
authorized_by: null
title: "README present: orientation, status with evidence subjects, corpus map"
tags: [acceptance-criterion]
binding: checked
check: human
story_ref: STORY-0005
```
README.md exists at root covering: one-paragraph what-this-is (the
public description made honest), current status naming the active story
and citing the latest evidence subject digest rather than asserting
freshness, a reading-order corpus map (DOC-0000 → 0005 → 0002 → 0003 →
0004), and the unlicensed-holding-position note until DEC-0002 signs.
<!-- atom:end id=SPEC-0101 -->

<!-- atom:begin id=SPEC-0102 -->
```yaml
id: SPEC-0102
type: specification
scope: story:story-0005
state: proposed
version: 1.0.0
instantiated_at: "2026-08-11T01:30:00Z"
author: consul-architect
authorized_by: null
title: "Correspondence shelved; substrate reading path unobstructed"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0005
```
ARCHITECT_RESPONSE_* and worker reports live under
corpus/correspondence/; their atoms still lint into the corpus (the
shelf is inside the lint path); no governed atom exists outside
platform/corpus/**.
<!-- atom:end id=SPEC-0102 -->

---

## STORY-0006 — the courier (local MCP bridge)

**Problem it closes.** Documents drafted in the claude.ai session reach
the repo today by human ferry: download, rename, place, commit. That
gap manufactured both delivery defects to date (duplicate tree, DOC-0006
omission). The courier is a small MCP server running on the owner's
box, repo-adjacent, that gives the drafting session direct but
*bounded* delivery and read-back.

**Trust posture — ENT-079 is the design.** The drafting session is an
unsigned surface; therefore the courier NEVER writes into
`platform/corpus/` and NEVER touches git. Deliveries land in
`platform/inbox/` (git-ignored) as candidates. Adoption is the existing
signed act: the owner or worker reviews, lints, moves into corpus, and
commits. The courier makes delivery mechanical and adoption deliberate —
unsigned input stays draft, with better logistics.

**Tools exposed (all read-only except the inbox):**

| Tool | Contract |
|---|---|
| `deliver(name, content)` | Write to `platform/inbox/<name>`; refuse path traversal, refuse overwrite outside inbox; returns sha256 of written bytes so the drafting session can verify integrity end-to-end |
| `read_doc(path)` | Read any file under the repo root (read-only) |
| `tree()` | Current repo file listing with hashes — kills the stale-picture class of defect at the source |
| `lint(path?)` | Run atom_lint (whole corpus or one file) and return findings — drafts get pre-checked before a human ever ferries them |
| `search(query)` | Query the embedding index — the drafting session gains recall over the live corpus instead of its own stale copy |
| `status()` | Latest evidence rows + standing-query report |

**Transport:** two deployment modes, same server. (a) Claude Desktop /
Claude Code attach it as a local stdio MCP — zero network exposure,
works today. (b) For claude.ai (this session's surface): expose via
Cloudflare tunnel as a remote MCP connector with an access token; the
tunnel is the owner's existing pattern. Mode (b) is optional and
default-off — mode (a) alone already closes the ferry gap for the
worker side, and the owner can ferry inbox deliveries from (a) sessions
with two clicks instead of five manual steps.

**Implementation sketch:** Python (`mcp` package, stdio server), ~200
lines, lives at `platform/tools/courier.py`, reuses atom_lint and
embedder as libraries. Path jail on every operation (resolved path must
be under repo root; writes must be under inbox). No credentials beyond
the optional tunnel token; the courier holds no signing capability by
construction — there is nothing in it worth stealing, which is the
correct amount.

<!-- atom:begin id=STORY-0006 -->
```yaml
id: STORY-0006
type: story
scope: platform
state: proposed
version: 1.1.0
instantiated_at: "2026-08-11T14:50:00Z"
author: agent-worker-story-0008
authorized_by: null
title: "Courier: local MCP bridging doc generation and delivery via inbox"
tags: [tooling, delivery]
tracker_ref: "gh:tecthulhu/republic#6"
acceptance: [SPEC-0103, SPEC-0104, SPEC-0105]
```
<!-- atom:end id=STORY-0006 -->

<!-- atom:begin id=SPEC-0103 -->
```yaml
id: SPEC-0103
type: specification
scope: story:story-0006
state: proposed
version: 1.0.0
instantiated_at: "2026-08-11T01:30:00Z"
author: consul-architect
authorized_by: null
title: "Courier serves the six tools over stdio MCP with a path jail"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0006
```
courier.py registers deliver/read_doc/tree/lint/search/status; a fixture
client exercises each; path-traversal attempts (../, absolute paths,
symlink escape) are refused with errors; deliver returns the sha256 of
written bytes and the bytes round-trip exactly.
<!-- atom:end id=SPEC-0103 -->

<!-- atom:begin id=SPEC-0104 -->
```yaml
id: SPEC-0104
type: specification
scope: story:story-0006
state: proposed
version: 1.0.0
instantiated_at: "2026-08-11T01:30:00Z"
author: consul-architect
authorized_by: null
title: "Courier cannot write corpus or invoke git"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0006
```
Negative fixtures: deliver targeting platform/corpus/**, schemas/**, or
tools/** is refused; no git invocation exists in courier.py (static
check) and no tool mutates anything outside platform/inbox/. The
ENT-079 posture — unsigned input lands as draft candidates only — holds
by construction, not convention.
<!-- atom:end id=SPEC-0104 -->

<!-- atom:begin id=SPEC-0105 -->
```yaml
id: SPEC-0105
type: specification
scope: story:story-0006
state: proposed
version: 1.0.0
instantiated_at: "2026-08-11T01:30:00Z"
author: consul-architect
authorized_by: null
title: "Adoption loop documented and exercised once end-to-end"
tags: [acceptance-criterion]
binding: checked
check: human
story_ref: STORY-0006
```
A real document is delivered to the inbox via MCP, pre-linted through
the courier's lint tool, adopted (moved to corpus and committed) by the
signed side, and whole-tree lint stays green — one full courier→adoption
cycle on record, with the flow written up in README or CLAUDE.md so the
next session uses it instead of the ferry.
<!-- atom:end id=SPEC-0105 -->
