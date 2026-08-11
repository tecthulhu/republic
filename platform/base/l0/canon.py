"""Canonical serialization (ES-011).

`sig` and `parent_sig` are Ed25519 over the JCS (RFC 8785) serialization of the
object with the signature field removed. Verifiers MUST canonicalize
identically; any canonicalization failure is a verification failure, fail
closed. The library is pinned in base/requirements.txt — closing DOC-0004 open
item (a) for the Python implementation. The pin is a versioned measurement: a
bump re-verifies every signature-bearing acceptance check.
"""
import rfc8785


class CanonicalizationError(Exception):
    """ES-011: canonicalization failed, therefore verification fails."""


def canonical(obj):
    try:
        return rfc8785.dumps(obj)
    except Exception as e:  # noqa: BLE001 — any failure denies (ENT-094)
        raise CanonicalizationError(str(e)) from e


def signing_form(obj, without):
    """The bytes actually signed: the object minus its signature field."""
    return canonical({k: v for k, v in obj.items() if k != without})
