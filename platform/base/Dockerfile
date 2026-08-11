# syntax=docker/dockerfile:1
#
# L0 gold base image (DOC-0003). Anything built FROM this is a mesh citizen the
# moment it starts (PA-011). Build from platform/ as the context:
#
#   docker build -f base/Dockerfile -t l0-base:BASE-v1 .
#
# L0-001: minimal, digest-pinned upstream; the final stage carries no shell, no
# package manager and no compiler toolchain. Wolfi (Chainguard) per D7 — glibc,
# so the pinned CLI runtime of STORY-0002 has somewhere to stand. The digests
# below are versioned measurements: changing either is a new BASE minor version
# and re-runs the conformance suite in full.
#
# Chainguard's public catalogue serves :latest only, so these digests are
# garbage-collected upstream over time. A rebuild after GC must re-pin, which is
# a BASE version bump by L0-001 — the discipline holds, but the pin is not
# indefinitely re-pullable and that is a property of the upstream, not a choice.

ARG UPSTREAM_DEV=cgr.dev/chainguard/python@sha256:4c58eb78b47d5a7cee9ffe0d1df16c56778ee40b067d983fb48d677a035abf8c
ARG UPSTREAM=cgr.dev/chainguard/python@sha256:69437de912cc3b5d36a2480b8fb0c3f658f151d8bc1978d19a6412be3a4983d5

# ---------------------------------------------------------------- build stage
# The build stage has apk, a shell and a compiler. None of it survives into the
# final stage: only the virtualenv and three crafted files are copied forward.
FROM ${UPSTREAM_DEV} AS build
USER root
WORKDIR /build

COPY base/requirements.txt .
RUN python -m venv /l0/venv \
 && /l0/venv/bin/pip install --no-cache-dir --disable-pip-version-check -r requirements.txt \
 && find /l0/venv -name '__pycache__' -type d -prune -exec rm -rf {} + \
 && rm -rf /l0/venv/lib/*/site-packages/pip /l0/venv/lib/*/site-packages/setuptools \
           /l0/venv/bin/pip* /l0/venv/bin/activate*

# L0-002: fixed UID:GID 10001:10001, no login shell. The passwd entry exists so
# the identity is nameable in logs and process listings; the nologin shell is a
# statement of intent, since no shell exists in the final stage to log into.
RUN mkdir -p /stage/work \
 && chown 10001:10001 /stage/work \
 && (cat /etc/passwd; echo 'citizen:x:10001:10001:citizen:/work:/sbin/nologin') > /stage/passwd \
 && (cat /etc/group;  echo 'citizen:x:10001:') > /stage/group

# ---------------------------------------------------------------- final stage
FROM ${UPSTREAM} AS base

COPY --from=build /l0/venv /l0/venv
COPY --from=build /stage/passwd /etc/passwd
COPY --from=build /stage/group /etc/group
COPY --from=build --chown=10001:10001 /stage/work /work

# L0-004: the base embeds init, the socket server, the conformance suite and the
# contract version at known paths. CTRL-0004's implementation reference
# (suite/citizenship) is the same source that ships here, so the suite in the
# image and the suite in CI cannot drift apart.
COPY --chmod=0755 base/l0/init.py /l0/init
COPY base/l0/*.py /l0/
COPY suite/citizenship/ /l0/conformance/
COPY base/BASE_VERSION /l0/BASE_VERSION

# Read-only rootfs is a runtime pin (L0-002); bytecode writing would fight it.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/l0/venv/bin:/usr/bin:/bin

USER 10001:10001
WORKDIR /work
ENTRYPOINT ["/l0/init"]

# L1 role layers overwrite l0.role_layer and l0.caveat_ceiling with their own
# values; an empty ceiling here means the base grants nothing by inheritance.
LABEL l0.base_version="BASE-v1" \
      l0.role_layer="" \
      l0.caveat_ceiling="[]"
