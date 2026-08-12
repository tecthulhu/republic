# ARCHITECT NOTE — STORY-0002 is not credential-blocked; only SPEC-0085 is

Correction, because the story stopped at the credential question when
only its last acceptance criterion actually needs a credential.

**Proceed now, no credential required, in this order:**

1. **SPEC-0081** — spawn gate + `suite/gates` (CTRL-0005): story-less
   spawn refused; leaf minted with story-audience token; zero host
   mounts; laws/strategy/mandate injected; restrictions armed pre/post.
   Includes BASE-AC-9 and BASE-AC-17. No model call — this is refusal
   and minting logic.
2. **CTRL-0006** — `suite/chain`: mint, attenuate, verify to root, lease
   TTL at every hop, two-party shape. Fixture credentials, no live
   session.
3. **SPEC-0083** — isolation: launch a *real* hardened container, verify
   no host mounts, kill it mid-task, confirm zero host residue. The
   container launches fine without a model credential — it comes up,
   proves isolation, and dies. This is the proof that container launch
   itself is not credential-gated.
4. **SPEC-0084** — attribution: every bus message and commit
   chain-verifiable to the leaf; rogue fixtures rejected. No model call.
5. **SPEC-0082** — IO path: harness streams a **surrogate** session to
   the bus (placeholder output, no CLI invocation of the model); a
   subscriber renders it; the Acta consumer persists it. Proves the wire
   without spending a token.

All five are verifiable with no model-provider credential and none will
be redone once the key exists. Two of them (suite/gates, suite/chain)
are the held controls CTRL-0005 and CTRL-0006 — building them moves the
held-controls line from three toward one *before* SPEC-0085 is touched.

**Hold ONLY SPEC-0085** for the credential. It is the single AC that
needs the CLI to reach the model API (the interrupt / inject / terminate
live demonstration). When the other five are green and 0085 is the only
thing left, report that state and the owner mints the scoped,
spend-capped adapter key per D47 — its live window stays minimal because
nothing else waits on it.

The distinction that was missed: **launching a container is not
credential-gated; running a live model session inside one is.** SPEC-0083
proves the former on its own. Build everything up to the model call now.
