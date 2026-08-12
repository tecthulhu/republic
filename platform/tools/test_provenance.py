#!/usr/bin/env python3
"""SPEC-0119 and SPEC-0121 fixtures: provenance consistency and repository tree shape.

SPEC-0113 caught content moving without a version bump. SPEC-0119 catches the level
beneath — the version moved but the provenance did not, so the instance claims the
previous instance's moment or the previous instance's author. That is not a
hypothetical: it nearly shipped during the DEC-0004 amendment, and lint was green.

SPEC-0121 catches a governed document living outside `platform/corpus/**`. That gap
let a work order sit untracked at the repository root twice with every gate passing,
because a prose-only document changes no atom digest — the corpus looks identical
whether the file was admitted or abandoned.

Run from anywhere: python3 tools/test_provenance.py
"""
import pathlib
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
    return subprocess.run(["git", "-C", str(cwd)] + list(args), capture_output=True, text=True)


ATOM = """<!-- atom:begin id=SPEC-9600 -->
```yaml
id: SPEC-9600
type: specification
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-01-01T00:00:00Z"
author: consul-draft
authorized_by: null
title: "provenance fixture"
binding: checked
check: machine
```
The original body.
<!-- atom:end id=SPEC-9600 -->
"""


def scaffold(td):
    repo = pathlib.Path(td, "repo")
    (repo / "platform" / "corpus").mkdir(parents=True)
    (repo / "platform" / "corpus" / "fixture.md").write_text(ATOM)
    (repo / "CLAUDE.md").write_text("# bootloader\n")
    git("init", "-q", cwd=repo)
    git("config", "user.email", "fixture@example.invalid", cwd=repo)
    git("config", "user.name", "fixture", cwd=repo)
    git("add", "-A", cwd=repo)
    git("commit", "-q", "-m", "baseline", cwd=repo)
    return repo


def lint_since(repo, ref="HEAD"):
    return subprocess.run([sys.executable, LINT, str(repo / "platform" / "corpus"),
                           "--since", ref], capture_output=True, text=True, cwd=str(repo))


def lint_tree(repo):
    return subprocess.run([sys.executable, LINT, str(repo / "platform" / "corpus"), "--tree"],
                          capture_output=True, text=True, cwd=str(repo))


# ---------------------------------------------------------------- SPEC-0119
with tempfile.TemporaryDirectory() as td:
    repo = scaffold(td)
    target = repo / "platform" / "corpus" / "fixture.md"

    check("baseline passes", lint_since(repo).returncode == 0, "")

    # Version moved, instantiated_at left behind — the DEC-0004 near-miss exactly.
    target.write_text(ATOM.replace("version: 1.0.0", "version: 1.1.0")
                          .replace("The original body.", "An amended body."))
    r = lint_since(repo)
    check("version bump with a stale instantiated_at is caught",
          r.returncode != 0 and "claiming the previous instance's moment" in r.stdout,
          r.stdout[-400:])

    # Version and timestamp moved together — legitimate.
    target.write_text(ATOM.replace("version: 1.0.0", "version: 1.1.0")
                          .replace('instantiated_at: "2026-01-01T00:00:00Z"',
                                   'instantiated_at: "2026-02-01T00:00:00Z"')
                          .replace("The original body.", "An amended body."))
    r = lint_since(repo)
    check("version and timestamp moving together passes", r.returncode == 0,
          r.stdout[-400:])

    # Content amended under the reconciler's name — a misattributed authoring act.
    target.write_text(ATOM.replace("version: 1.0.0", "version: 1.1.0")
                          .replace('instantiated_at: "2026-01-01T00:00:00Z"',
                                   'instantiated_at: "2026-02-01T00:00:00Z"')
                          .replace("author: consul-draft", "author: ont-060-reconciliation")
                          .replace("The original body.", "An amended body."))
    r = lint_since(repo)
    check("content amended under the reconciler's name is caught",
          r.returncode != 0 and "beyond a lifecycle transition" in r.stdout,
          r.stdout[-400:])

# A pure lifecycle transition under the reconciler's name is exactly its job. Modelled
# on what reconciliation actually writes: ratified -> active, author moved, and
# authorized_by left alone — the reconciler never ratifies, so a changed authorized_by
# under its name would be a misattribution and is correctly rejected. An earlier
# version of this fixture combined the two and was wrong, not the check.
RATIFIED = (ATOM.replace("state: proposed", "state: ratified")
                .replace("authorized_by: null", "authorized_by: DEC-0001"))

with tempfile.TemporaryDirectory() as td:
    repo = scaffold(td)
    target = repo / "platform" / "corpus" / "fixture.md"
    target.write_text(RATIFIED)
    git("commit", "-q", "-am", "ratified baseline", cwd=repo)

    target.write_text(RATIFIED.replace("state: ratified", "state: active")
                              .replace("version: 1.0.0", "version: 1.1.0")
                              .replace('instantiated_at: "2026-01-01T00:00:00Z"',
                                       'instantiated_at: "2026-02-01T00:00:00Z"')
                              .replace("author: consul-draft",
                                       "author: ont-060-reconciliation"))
    r = lint_since(repo)
    check("a lifecycle-only transition under the reconciler passes", r.returncode == 0,
          r.stdout[-500:])

    # And the same instance with any content edit alongside it is still caught.
    target.write_text(RATIFIED.replace("state: ratified", "state: active")
                              .replace("version: 1.0.0", "version: 1.1.0")
                              .replace('instantiated_at: "2026-01-01T00:00:00Z"',
                                       'instantiated_at: "2026-02-01T00:00:00Z"')
                              .replace("author: consul-draft",
                                       "author: ont-060-reconciliation")
                              .replace("The original body.", "Reworded while activating."))
    r = lint_since(repo)
    check("a content edit smuggled into a reconciler transition is caught",
          r.returncode != 0 and "beyond a lifecycle transition" in r.stdout,
          r.stdout[-400:])

# ---------------------------------------------------------------- SPEC-0121
with tempfile.TemporaryDirectory() as td:
    repo = scaffold(td)

    check("a clean tree passes --tree", lint_tree(repo).returncode == 0, "")

    # An atom-bearing file at the root: governed content outside the canonical tree.
    stray = repo / "STRAY_NOTES.md"
    stray.write_text(ATOM.replace("SPEC-9600", "SPEC-9601"))
    r = lint_tree(repo)
    check("an atom-bearing file outside the corpus is caught",
          r.returncode != 0 and "carries atom markers" in r.stdout, r.stdout[-400:])
    stray.unlink()

    # A prose-only response at the root: the case that slipped through twice, and the
    # one no digest can notice.
    (repo / "ARCHITECT_RESPONSE_099.md").write_text("# a ruling with no atoms in it\n")
    r = lint_tree(repo)
    check("a prose-only governed-named file outside the corpus is caught",
          r.returncode != 0 and "governed naming family" in r.stdout, r.stdout[-400:])
    (repo / "ARCHITECT_RESPONSE_099.md").unlink()

    # Allowlisted root files are fine, and ordinary notes are not governed-looking.
    (repo / "README.md").write_text("# readme\n")
    (repo / "notes.md").write_text("# scratch, carries nothing governed\n")
    r = lint_tree(repo)
    check("allowlisted and unremarkable root files pass", r.returncode == 0,
          r.stdout[-400:])

# The real repository must pass both, or the gates are not deployable.
r = subprocess.run([sys.executable, LINT, "--tree"], capture_output=True, text=True)
check("the real repository passes --tree", r.returncode == 0, r.stdout[-600:])

print(f"\n{'PASS' if not failures else 'FAIL'} — SPEC-0119/0121 suite"
      f"{'' if not failures else ': ' + ', '.join(failures)}")
sys.exit(1 if failures else 0)
