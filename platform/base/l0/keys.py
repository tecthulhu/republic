"""Key material handling. Payload code never imports this — only init and agentd do.

L0-011: credential files are read once, held in memory, and unlinked before the
payload starts. The payload reaches signing only through the agentd socket
(L0-020/021), so there is no code path in which payload code touches a key.
"""
import base64

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey


def b64e(raw): return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def b64d(text):
    if isinstance(text, bytes):
        return text
    pad = "=" * (-len(text) % 4)
    return base64.urlsafe_b64decode(text + pad)


def signer_from_seed(seed_b64):
    return Ed25519PrivateKey.from_private_bytes(b64d(seed_b64))


def public_b64(private_key):
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
    return b64e(private_key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw))


# Key generation deliberately does not live here. It is the minting side's capability
# (harness/mint.py), and a citizen image that carries it carries the ability to
# manufacture its own keypairs — one step from a credential factory, which is ENT-003
# defeated at the root. The conformance suite asserts its absence, so reintroducing it
# fails CI rather than being noticed in review.
def verify_key(pub_b64):
    return Ed25519PublicKey.from_public_bytes(b64d(pub_b64))
