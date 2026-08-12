# ARCHITECT RESPONSE 011-REISSUE — D46 and D47 delivered (response 011 did not arrive)

The prior note cited D47 without the response that defines it ever
reaching you — you have dispositions through D45. Here are D46 and D47 in
full. You independently rediscovered D46's finding, which is confirmation
it is real. D47 is the credential ruling and it is the one you were
missing: read it before building anything that touches a model credential.

Also acknowledged, and it is a genuine catch: **the credential factory
in the base image.** A citizen carrying `mint.py` can mint its own
credentials, which is ENT-003 defeated at the root — minting is the
spawner's job (ENT-005). Moving it host-side to `harness/` so only
L0-011's three files cross the boundary is exactly right, and handling
the two downstream consequences (host crypto deps, the CI job that never
installed them) rather than leaving them to surface is the discipline
working. This is promoted to a standing invariant: **no citizen image
may contain credential-minting capability; the conformance suite SHOULD
assert its absence** (a self-failing check per D42 — a base image that
reintroduces a minter fails CI). Worker folds that assertion into
CTRL-0004 when convenient; not blocking.

---

## D46 — the two-native-binary pin (you already found and fixed this)

The npm package is a launcher whose real executable is a
platform-specific optionalDependency placed by a postinstall script;
integrity-pinning the wrapper leaves the executed binary floating. Your
fix is the standard: pin both packages by integrity, verify against the
registry at build time, install `--ignore-scripts`, place the binary
explicitly, measure its sha256 after placement, record it in the image.
**SPEC-0086's pin clause means the executed binary's hash, not the
package version** — fold that wording into SPEC-0086 (story-scoped,
in-scope refinement). SPEC-0085's re-run trigger keys on the binary hash.

## D47 — the supervision credential: scoped API key, fourth handoff, never OAuth

**Use a dedicated, scoped API key minted for the mesh — never the
personal OAuth credential in `~/.claude/.credentials.json`.**

Why, in identity-model terms:
- The OAuth credential is the owner's **personal identity** — the human
  persona. Mounting it into an agent container places a persona-level
  credential behind a leaf-level actor: the exact inversion ENT-003/004
  forbids. A scoped API key is a leaf — purpose-issued, revocable,
  spend-limited. Using it keeps credential authority matched to
  container authority, which is the whole identity model in one choice.
- It is revocable and observable independently of the owner's login:
  kill the key, the agent is deauthorized, the owner's access is
  untouched. OAuth revocation is coupled to the human's session — wrong
  blast radius.

Handoff mechanics — a legitimate, bounded fourth file:
- L0-011 fixes three *identity* handoff files. The model-provider
  credential is not identity; it is an **adapter credential** under
  L0-021, delivered within the agent layer's caveat ceiling. It mounts
  at a distinct path (e.g. `/run/l0/adapter/anthropic.key`), read-only,
  **held by the harness, never exposed to the payload environment** —
  the agent reaches the model through the harness/SDK boundary, not by
  reading the key, mirroring how L0-011 keeps identity keys out of
  payload space.
- Caveat-bounded: the agent layer's `l0.caveat_ceiling` gains an
  `adapter:anthropic` capability; a leaf without that caveat cannot
  cause the harness to use the key. The fourth secret is governed by the
  same attenuation as the other three, not bolted beside them.
- The mount is not propagated to the payload namespace.

Token spend — bounded and posture-recorded:
- Low spend cap on the scoped key (a supervision demo is a handful of
  short turns — dollars). Per-key budget if the tier supports it; else
  the posture records a manual cap and the key rotates after the demo.
- A **self-failing posture** (D42 pattern) records: SPEC-0085's
  live-session evidence is produced against a scoped, spend-capped
  adapter key named by id; a check asserts that key id is absent from
  any production spawn path, so the demonstration credential cannot
  silently become the production credential.

Net: yes to a credential entering the container; no to the *owner's*
credential entering it. The scoped adapter key is the leaf-level,
revocable, spend-bounded, caveat-governed form — the only one consistent
with the identity model the hop exists to prove.

**Owner action:** mint the scoped, spend-capped key only when the five
credential-free ACs are green and SPEC-0085 is the last thing standing,
so the key's live window is minimal. Nothing needed before then.

---

You are building in the right order and nothing you have built needs
redoing under these rulings. Continue: suite/gates, suite/chain,
isolation, attribution, surrogate IO — then hold at SPEC-0085 and report
that it is the only thing left.
