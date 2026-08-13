"""Ephemeral mesh for a suite run: a network, a bus, a handoff volume, an observer.

Extracted from the citizenship suite when the gates suite needed the same thing. Two
suites standing up a bus two different ways would drift, and the drift would show up as
one suite passing where the other fails for reasons that have nothing to do with the
criteria being tested.

The bus is adopted infrastructure admitted by digest-pinned allowlist (PA-013). If the
pinned digest cannot be pulled the run says so and records what it actually used in
every evidence row — it never silently substitutes.
"""
import json
import re
import subprocess
import uuid

NATS_IMAGE = "nats@sha256:b83efabe3e7def1e0a4a31ec6e078999bb17c80363f881df35edc70fcb6bb927"
NATS_FALLBACK = "nats:2.10-alpine"


def sh(*args, check=False, timeout=240):
    r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    if check and r.returncode:
        raise RuntimeError(f"{' '.join(args)}\n{r.stdout}\n{r.stderr}")
    return r


def image_digest(image):
    r = sh("docker", "image", "inspect", image, "--format", "{{.Id}}")
    return r.stdout.strip() or "sha256:unknown"


def observed(text):
    m = re.search(r"OBSERVED (\[.*\])", text)
    return json.loads(m.group(1)) if m else []


def wait_and_logs(name, timeout=240):
    sh("docker", "wait", name, timeout=timeout)
    r = sh("docker", "logs", name)
    return r.stdout + r.stderr


class Mesh:
    """One suite run's disposable infrastructure. Everything it creates, it removes."""

    def __init__(self, image):
        self.image = image
        self.tag = uuid.uuid4().hex[:8]
        self.net = f"mesh-{self.tag}"
        self.bus = f"nats-{self.tag}"
        self.vol = f"handoff-{self.tag}"
        self.created = []
        self.bus_image = None

    def __enter__(self):
        # --internal: L0-002 pins egress to the bus, and nothing was enforcing it. Every
        # citizen spawned before this could open a socket to anywhere on the internet;
        # the filesystem isolation was verified and the network side simply was not
        # checked. An internal network has no route off the host, so the bus is the only
        # thing a citizen can reach. Adapter egress (a model provider, a git remote)
        # becomes an explicit, caveat-gated addition rather than an accident of the
        # default bridge — which is what D47's `adapter:` capability describes.
        sh("docker", "network", "create", "--internal", self.net, check=True)
        self.created.append(("network", self.net))
        image = NATS_IMAGE if sh("docker", "pull", NATS_IMAGE).returncode == 0 else NATS_FALLBACK
        if image == NATS_FALLBACK:
            sh("docker", "pull", NATS_FALLBACK, check=True, timeout=300)
            print(f"  note: pinned bus digest unavailable, using {NATS_FALLBACK} "
                  f"(recorded in evidence)")
        self.bus_image = image
        sh("docker", "run", "-d", "--name", self.bus, "--network", self.net,
           "--network-alias", "nats", image, "-js", check=True)
        self.created.append(("container", self.bus))
        sh("docker", "volume", "create", self.vol, check=True)
        self.created.append(("volume", self.vol))
        return self

    def __exit__(self, *exc):
        for kind, name in reversed(self.created):
            if kind == "container":
                sh("docker", "rm", "-f", name)
            elif kind == "network":
                sh("docker", "network", "rm", name)
            elif kind == "volume":
                sh("docker", "volume", "rm", "-f", name)

    def track(self, name):
        self.created.append(("container", name))
        return name

    def track_volume(self, name):
        self.created.append(("volume", name))
        return name

    def observe(self, seconds, publish_after=None, subjects=None):
        """Watch the wire as a third party. Audit is the transport (PA-014), so a suite
        that asked the citizen what it published would be taking its word for it."""
        name = self.track(f"obs-{self.tag}-{uuid.uuid4().hex[:4]}")
        args = ["docker", "run", "-d", "--name", name, "--network", self.net,
                "--entrypoint", "/l0/venv/bin/python", self.image,
                "/l0/conformance/observe.py", "--seconds", str(seconds)]
        if subjects:
            args += ["--subjects"] + list(subjects)
        if publish_after:
            args += ["--publish-after", json.dumps(publish_after)]
        sh(*args, check=True)
        return name
