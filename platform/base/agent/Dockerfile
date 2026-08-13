# syntax=docker/dockerfile:1
#
# L1 agent role layer (PA-011, DOC-0003 §5). FROM the gold base by digest, adding
# only its role delta: a node runtime and the pinned CLI. Build from platform/:
#
#   docker build -f base/agent/Dockerfile --build-arg BASE=l0-base:BASE-v1 \
#     -t l0-agent:0.1.0 .
#
# L0-003 is additive-only: this layer may add binaries and writable paths under
# /work; it may not reintroduce a shell, re-add a capability, regain root, widen the
# writable set, or weaken any L0-002 pin. The conformance suite runs against this
# image in CI and would fail it for any of those.
#
# SPEC-0086 — the CLI is a versioned measurement. Version and integrity hash are
# pinned below and recorded in every evidence row this story emits; a bump
# invalidates STORY-0002's prior evidence and re-runs SPEC-0081..0085 in full.

ARG BASE=l0-base:BASE-v1
ARG NODE_DEV=cgr.dev/chainguard/node@sha256:07c193f0b7c9b7a5cc0070da7384efe9f88ae92ef45a458c065a4a8dbc251fe1
ARG NODE_RUNTIME=cgr.dev/chainguard/node@sha256:71102c411350b53ff67f83c6679070a6c839306d84f9033146f8b93b0d730c78
ARG GIT_IMAGE=cgr.dev/chainguard/git@sha256:b48c8ecae911af6c02515d3da34154ea85168ee969afb5e91e6398c075217ff8

# CLI pin (SPEC-0086). Resolved 2026-08-12 from the npm registry.
#
# Two pins, because one is not enough. The npm package `@anthropic-ai/claude-code` is
# a wrapper whose `bin` points at a native `claude.exe`; the executable that actually
# runs arrives as a platform-specific optionalDependency. Pinning only the wrapper
# would pin the launcher and leave the binary floating — so the platform package is
# pinned by integrity too, and the build verifies both against the registry.
ARG CLI_VERSION=2.1.228
ARG CLI_INTEGRITY=sha512-S3Iy+c6ZuFjswQOekbVgXA+RxAuU8H2ae2nxFynqmvR5r3Gm9oyFV19XgiuatYRFKKjxP0K3i5vvvelPDgx12g==
ARG CLI_PLATFORM_PKG=@anthropic-ai/claude-code-linux-x64
ARG CLI_PLATFORM_INTEGRITY=sha512-LMrLUYW5FY3r8wsQk/U5HWacHmxlEWKxaOgNzmDn1f5FhgKsSAPpioqf2JE5AusRRKXyWvhYM1crOE/CKIqoNQ==

# ------------------------------------------------------------------ git source
# A digest-pinned image that already has git installed with its dependencies, rather
# than an apk install into a bare root — which needs repositories and keys wired into
# the new root and buys nothing over pinning an image.
FROM ${GIT_IMAGE} AS gitsrc

# ------------------------------------------------------------------ CLI stage
# npm and a shell exist here and nowhere downstream: only the installed tree and the
# node binary cross into the final image.
FROM ${NODE_DEV} AS cli
ARG CLI_VERSION
ARG CLI_INTEGRITY
USER root
WORKDIR /build
ARG CLI_PLATFORM_PKG
ARG CLI_PLATFORM_INTEGRITY

# Both integrity hashes are verified rather than trusted: a version pin alone follows a
# republished tarball, and pinning the wrapper alone leaves the native binary floating.
RUN set -eu; \
    for spec in "@anthropic-ai/claude-code@${CLI_VERSION}:${CLI_INTEGRITY}" \
                "${CLI_PLATFORM_PKG}@${CLI_VERSION}:${CLI_PLATFORM_INTEGRITY}"; do \
      pkg="${spec%:*}"; want="${spec#*:}"; \
      got="$(npm view "${pkg}" dist.integrity)"; \
      echo "  ${pkg}"; echo "    pinned:   ${want}"; echo "    registry: ${got}"; \
      [ "${got}" = "${want}" ] || { echo "integrity mismatch for ${pkg}"; exit 1; }; \
    done

# --ignore-scripts: the postinstall's only job is to copy the platform binary over the
# wrapper's bin/claude.exe, which this build does explicitly below. Placing it here
# rather than delegating means no package script executes during the image build, and
# the binary that lands is the one whose integrity was just verified.
RUN set -eu; \
    npm install -g --ignore-scripts --prefix /cli \
      "@anthropic-ai/claude-code@${CLI_VERSION}"; \
    pkgroot=/cli/lib/node_modules/@anthropic-ai/claude-code; \
    binary="${pkgroot}/node_modules/${CLI_PLATFORM_PKG}/claude"; \
    [ -x "${binary}" ] || { echo "platform binary absent: ${binary}"; exit 1; }; \
    install -m 0755 "${binary}" /cli/bin/claude; \
    /cli/bin/claude --version

# git is part of the agent role delta, not an afterthought: PA-010 names git push as
# one of the three sanctioned durable effects, and SPEC-0084 requires the session to
# produce attributable commits. An agent that cannot run git cannot produce the effects
# the architecture says it produces.
#
# Staged here so git-shell can be deleted before anything crosses into the final image:
# it is a login shell, L0-003 forbids reintroducing one, and the conformance suite
# would be right to fail an image carrying it. The final stage has no shell to delete
# it with, so it has to happen upstream.
COPY --from=gitsrc /usr/bin/git /gitroot/usr/bin/git
COPY --from=gitsrc /usr/libexec/git-core /gitroot/usr/libexec/git-core
COPY --from=gitsrc /usr/lib /gitroot/usr/lib
RUN set -eu; \
    rm -f /gitroot/usr/bin/git-shell /gitroot/usr/libexec/git-core/git-shell; \
    test ! -e /gitroot/usr/libexec/git-core/git-shell

# Record what was installed, so a running container can report its own pin without the
# harness having to know it (the descriptor is emitted, never authored — ENT-031). The
# binary digest is measured after placement, so it describes the executable that will
# actually run rather than the tarball it came from.
RUN set -eu; \
    printf '%s\n' "${CLI_VERSION}" > /cli/CLI_VERSION; \
    printf '%s\n' "${CLI_INTEGRITY}" > /cli/CLI_INTEGRITY; \
    printf '%s\n' "${CLI_PLATFORM_PKG}@${CLI_VERSION}" > /cli/CLI_PLATFORM; \
    sha256sum /cli/bin/claude | cut -d' ' -f1 > /cli/CLI_BINARY_SHA256

# ---------------------------------------------------------------- agent layer
FROM ${BASE} AS agent

COPY --from=cli /usr/bin/node /usr/bin/node
COPY --from=cli /cli /cli
COPY --from=cli /gitroot/usr/bin/git /usr/bin/git
COPY --from=cli /gitroot/usr/libexec/git-core /usr/libexec/git-core
COPY --from=cli /gitroot/usr/lib/ /usr/lib/

# /work stays the only writable path (L0-002). The CLI wants a home directory for
# state; it gets one under /work, which is tmpfs and dies with the container.
ENV NODE_PATH=/cli/lib/node_modules \
    PATH=/cli/bin:/l0/venv/bin:/usr/bin:/bin \
    HOME=/work \
    CLAUDE_CONFIG_DIR=/work/.claude

# L1 declares its caveat ceiling in image labels (PA-011, ENT-022): the maximum
# caveat families grantable to this citizen's leaves. The harness refuses a spawn
# requesting anything outside this list (BASE-AC-17), which is why it is data in the
# image rather than a promise in a document.
LABEL l0.base_version="BASE-v1" \
      l0.role_layer="agent@0.1.0" \
      l0.caveat_ceiling="[\"audience\",\"action\",\"lease_age\",\"subject\",\"resource\",\"use_count\",\"depth\",\"parent_id\",\"lease_id\",\"now\",\"mint_time\"]" \
      l0.cli_version="2.1.228" \
      l0.git_version="2.55.0"

# No CMD: an agent container is started by the harness with the session command it
# supervises. A default payload would invite a spawn that nobody supervises.
