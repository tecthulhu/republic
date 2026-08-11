# syntax=docker/dockerfile:1
#
# The violating fixture (STORY-0001 / SPEC-0072 v1.1.0). Deliberately
# non-conformant: it exists to prove the sealing claims are falsifiable. A suite
# that cannot fail is not evidence, it is decoration.
#
# Violations, one per sealed property (L0-003):
#   - a shell restored into the final stage        -> BASE-AC-8 / BASE-AC-15
#   - root regained                                -> BASE-AC-6 / BASE-AC-15
#   - the base version label removed               -> BASE-AC-16
#
# Build from platform/ as context:
#   docker build -f base/fixtures/violating/Dockerfile \
#     --build-arg BASE=l0-base:BASE-v1 -t l0-violating:dev .

ARG BASE=l0-base:BASE-v1
ARG UPSTREAM_DEV=cgr.dev/chainguard/python@sha256:4c58eb78b47d5a7cee9ffe0d1df16c56778ee40b067d983fb48d677a035abf8c

FROM ${UPSTREAM_DEV} AS shellsource

FROM ${BASE}

# Reopen what the lower layer sealed. Each line is the thing L0-003 forbids.
COPY --from=shellsource /bin/busybox /bin/busybox
COPY --from=shellsource /bin/sh /bin/sh
USER 0:0

# BASE-AC-16: the base version label is dropped, so ancestry can no longer be
# asserted from the image itself.
LABEL l0.base_version="" \
      l0.role_layer="rogue@0.0.0" \
      l0.caveat_ceiling="[\"*\"]"

CMD ["/l0/venv/bin/python", "-c", "print('violating fixture running as root with a shell')"]
