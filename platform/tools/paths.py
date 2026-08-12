"""Repository-root path resolution (SPEC-0114).

Tools located their inputs relative to the caller's working directory, so every
invocation carried an unwritten precondition: "run me from platform/". That
precondition failed during the signing session, which is the regression this
module exists to prevent.

Resolution is from the tool's own location, not the caller's. A tool knows where
it lives; it should not depend on where it was called from.
"""
import pathlib

# tools/paths.py -> tools -> platform
PLATFORM = pathlib.Path(__file__).resolve().parents[1]
REPO = PLATFORM.parent

CORPUS = PLATFORM / "corpus"
ACTA = PLATFORM / "acta"
INDEX = PLATFORM / "index"
SCHEMAS = PLATFORM / "schemas"
SCHEMA = SCHEMAS / "atoms-1.0.0.json"
BASE_L0 = PLATFORM / "base" / "l0"
SUITE = PLATFORM / "suite"


def resolve(target):
    """Interpret a caller-supplied path. Absolute and existing relative paths are
    honored as given; a bare name that matches a platform directory resolves against
    the platform root, so `atom_lint.py corpus` means the same thing from anywhere."""
    p = pathlib.Path(target)
    if p.is_absolute() or p.exists():
        return p
    candidate = PLATFORM / target
    return candidate if candidate.exists() else p


def index_dir():
    """index/ is git-ignored and therefore absent on a clean checkout."""
    INDEX.mkdir(exist_ok=True)
    return INDEX


def acta_dir():
    ACTA.mkdir(exist_ok=True)
    return ACTA
