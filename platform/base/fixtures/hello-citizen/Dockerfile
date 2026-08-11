# syntax=docker/dockerfile:1
#
# hello-citizen — the conforming L2 fixture (STORY-0001 / SPEC-0071).
# Proves the base's claim: anything built FROM it is a mesh citizen the moment it
# starts, adding only its own payload. Build from platform/ as context:
#
#   docker build -f base/fixtures/hello-citizen/Dockerfile \
#     --build-arg BASE=l0-base:BASE-v1 -t l0-hello:dev .

ARG BASE=l0-base:BASE-v1
FROM ${BASE}

# L0-003, additive-only: a payload and nothing else. No shell restored, no
# capability re-added, no root regained, no writable path outside /work.
COPY --chmod=0755 base/fixtures/hello-citizen/hello.py /app/hello.py

LABEL l0.base_version="BASE-v1" \
      l0.role_layer="agent@0.1.0" \
      l0.caveat_ceiling="[\"audience\",\"action\",\"lease_age\"]"

CMD ["/l0/venv/bin/python", "/app/hello.py"]
