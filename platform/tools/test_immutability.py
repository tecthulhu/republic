#!/usr/bin/env python3
"""SPEC-0113 fixture suite: instance immutability, enforced rather than trusted.

ONT-012/015 say a published instance never changes — a change is a new instance.
Until now that was a convention held up by reviewer attention, and this session
produced at least one near-miss where an atom's state was about to be edited in
place. The check compares the working tree against a git ref: content may move only
when (version, instantiated_at) moves with it.

Both directions are proven here, because a check that cannot fail is decoration:
the forbidden edit-in-place is caught, and the legitimate new-instance edit passes.

Run from anywhere: python3 tools/test_immutability.py
"""
import pathlib
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from paths import PLATFORM  # noqa: E402

LINT = str(PLATFORM / "tools" / "atom_lint.py")
failures = []


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{'' if ok else '  — ' + detail}")
    if not ok:
        failures.append(name)


def git(*args, cwd):
    return subprocess.run(["git", "-C", str(cwd)] + list(args),
                          capture_output=True, text=True)


ATOM = """<!-- atom:begin id=SPEC-9500 -->
```yaml
id: SPEC-9500
type: specification
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-01-01T00:00:00Z"
author: fixture
authorized_by: null
title: "immutability fixture"
binding: checked
check: machine
```
The original body, as published.
<!-- atom:end id=SPEC-9500 -->
"""


def scaffold(td):
    """A minimal repository whose corpus holds one atom, committed."""
    repo = pathlib.Path(td, "repo")
    (repo / "platform" / "corpus").mkdir(parents=True)
    (repo / "platform" / "tools").mkdir(parents=True)
    (repo / "platform" / "schemas").mkdir(parents=True)
    # The tools and schema are read from the real platform via absolute paths, so the
    # fixture repo only needs its corpus. What must be real is the git history.
    (repo / "platform" / "corpus" / "fixture.md").write_text(ATOM)
    git("init", "-q", cwd=repo)
    git("config", "user.email", "fixture@example.invalid", cwd=repo)
    git("config", "user.name", "fixture", cwd=repo)
    git("add", "-A", cwd=repo)
    git("commit", "-q", "-m", "fixture baseline", cwd=repo)
    return repo


def lint_since(repo, ref="HEAD"):
    corpus = repo / "platform" / "corpus"
    return subprocess.run([sys.executable, LINT, str(corpus), "--since", ref],
                          capture_output=True, text=True, cwd=str(repo))


with tempfile.TemporaryDirectory() as td:
    repo = scaffold(td)
    target = repo / "platform" / "corpus" / "fixture.md"

    # Baseline: unchanged tree passes.
    r = lint_since(repo)
    check("unchanged tree passes --since", r.returncode == 0,
          r.stdout[-300:] + r.stderr[-300:])

    # Forbidden: body edited, instance identity untouched.
    target.write_text(ATOM.replace("The original body, as published.",
                                   "The body, quietly rewritten."))
    r = lint_since(repo)
    caught = r.returncode != 0 and "edited in place" in r.stdout
    check("edit-in-place of the body is caught", caught, r.stdout[-400:])
    check("the finding cites ONT-012/015", "ONT-012/015" in r.stdout, r.stdout[-300:])

    # Forbidden: a field edited, instance identity untouched. State is the field this
    # session nearly changed in place, so it is the one worth testing by name.
    target.write_text(ATOM.replace("state: proposed", "state: ratified")
                          .replace("authorized_by: null", "authorized_by: DEC-0001"))
    r = lint_since(repo)
    check("edit-in-place of state is caught", r.returncode != 0 and "SPEC-9500" in r.stdout,
          r.stdout[-400:])

    # Legitimate: content changes together with a new (version, instantiated_at).
    target.write_text(ATOM.replace("state: proposed", "state: ratified")
                          .replace("authorized_by: null", "authorized_by: DEC-0001")
                          .replace("version: 1.0.0", "version: 1.1.0")
                          .replace('instantiated_at: "2026-01-01T00:00:00Z"',
                                   'instantiated_at: "2026-02-01T00:00:00Z"'))
    r = lint_since(repo)
    check("a new instance passes", r.returncode == 0, r.stdout[-400:] + r.stderr[-300:])

    # A brand-new atom has nothing to compare against and must not be flagged.
    (repo / "platform" / "corpus" / "new.md").write_text(
        ATOM.replace("SPEC-9500", "SPEC-9501").replace("immutability fixture", "new atom"))
    r = lint_since(repo)
    check("a newly added atom is not flagged", r.returncode == 0,
          r.stdout[-400:] + r.stderr[-300:])

    # An unreadable ref is a finding, not a silent pass.
    r = lint_since(repo, ref="no-such-ref")
    check("an unresolvable ref fails rather than passing quietly",
          r.returncode != 0 and "cannot read tree" in r.stdout, r.stdout[-300:])

print(f"\n{'PASS' if not failures else 'FAIL'} — SPEC-0113 immutability suite"
      f"{'' if not failures else ': ' + ', '.join(failures)}")
sys.exit(1 if failures else 0)
