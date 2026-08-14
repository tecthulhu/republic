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

    # v1.2.0: at the root the allowlist is the whole rule. A file whose name matches
    # no governed family and carries no atoms is still a violation there — this is the
    # case the naming heuristic kept missing, once per new correspondence family.
    (repo / "TRIBUNE_ruling.md").write_text("# a ruling by a sender no pattern has met\n")
    r = lint_tree(repo)
    check("an unrecognised root file is caught by the rule, not by a name pattern",
          r.returncode != 0 and "not on the root allowlist" in r.stdout, r.stdout[-400:])
    (repo / "TRIBUNE_ruling.md").unlink()

    (repo / "notes.md").write_text("# scratch, carries nothing governed\n")
    r = lint_tree(repo)
    check("an unremarkable root file is caught too — the root has no ordinary notes",
          r.returncode != 0 and "not on the root allowlist" in r.stdout, r.stdout[-400:])
    (repo / "notes.md").unlink()

    # Below the root the heuristic still governs, and must not have become a blanket
    # refusal: an ordinary note under platform/ is legitimate and stays legitimate.
    (repo / "README.md").write_text("# readme\n")
    (repo / "platform" / "notes.md").write_text("# scratch, nothing governed\n")
    r = lint_tree(repo)
    check("allowlisted root files and ordinary notes below the root pass",
          r.returncode == 0, r.stdout[-400:])

    # And the heuristic below the root has not been swallowed by the root rule.
    (repo / "platform" / "ARCHITECT_RESPONSE_098.md").write_text("# a ruling, misfiled\n")
    r = lint_tree(repo)
    check("a governed-named file below the root is still caught by the heuristic",
          r.returncode != 0 and "governed naming family" in r.stdout, r.stdout[-400:])
    (repo / "platform" / "ARCHITECT_RESPONSE_098.md").unlink()

# ------------------------------------------- the canonical whitepaper rendering
# docs/WHITEPAPER.md is a deliberate second copy: one stable public link that each
# release overwrites. Two copies of one fact with nothing comparing them is the
# source-of-falsehood shape, so the copy is checked.
with tempfile.TemporaryDirectory() as td:
    repo = scaffold(td)
    docs = repo / "docs"
    docs.mkdir()

    check("no docs directory is not a finding", lint_tree(repo).returncode == 0, "")

    (docs / "REPUBLIC_WHITEPAPER_v1.0.1.md").write_text("# the paper\n\nv1.0.1 body.\n")
    (docs / "WHITEPAPER.md").write_text("# the paper\n\nv1.0.1 body.\n")
    check("canonical matching the newest versioned instance passes",
          lint_tree(repo).returncode == 0, lint_tree(repo).stdout[-400:])

    # A new version lands and the canonical is not refreshed — the one state where
    # the public link renders a superseded paper while the record holds the current.
    (docs / "REPUBLIC_WHITEPAPER_v1.1.0.md").write_text("# the paper\n\nv1.1.0 body.\n")
    r = lint_tree(repo)
    check("a versioned bump without refreshing the canonical is caught",
          r.returncode != 0 and "has drifted from it" in r.stdout, r.stdout[-400:])

    (docs / "WHITEPAPER.md").write_text("# the paper\n\nv1.1.0 body.\n")
    check("refreshing the canonical clears it", lint_tree(repo).returncode == 0,
          lint_tree(repo).stdout[-400:])

    # Ordering is by version, not filename: 1.10.0 is newer than 1.9.0.
    (docs / "REPUBLIC_WHITEPAPER_v1.9.0.md").write_text("# the paper\n\nv1.9.0 body.\n")
    (docs / "REPUBLIC_WHITEPAPER_v1.10.0.md").write_text("# the paper\n\nv1.10.0 body.\n")
    (docs / "WHITEPAPER.md").write_text("# the paper\n\nv1.10.0 body.\n")
    check("newest is chosen by version order, not lexical order",
          lint_tree(repo).returncode == 0, lint_tree(repo).stdout[-400:])

    # A canonical with nothing behind it: a citation resolves to no instance.
    for p in docs.glob("REPUBLIC_WHITEPAPER_*.md"):
        p.unlink()
    r = lint_tree(repo)
    check("a canonical with no versioned instance behind it is caught",
          r.returncode != 0 and "no versioned instance" in r.stdout, r.stdout[-400:])


# The real repository must pass both, or the gates are not deployable.
r = subprocess.run([sys.executable, LINT, "--tree"], capture_output=True, text=True)
check("the real repository passes --tree", r.returncode == 0, r.stdout[-600:])

print(f"\n{'PASS' if not failures else 'FAIL'} — SPEC-0119/0121 suite"
      f"{'' if not failures else ': ' + ', '.join(failures)}")
sys.exit(1 if failures else 0)
