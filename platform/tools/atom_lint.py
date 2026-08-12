#!/usr/bin/env python3
"""atom-lint (CTRL-0001): validates governed files per DOC-0000.

Checks: ONT-070a boundary parsing; per-type JSON Schema validation (ONT-071);
id/prefix agreement and uniqueness (ONT-011); authorized_by past proposed
(ONT-010/061); rule claims are SPEC/RSTR never PRIN (ONT-030); reference
resolution (ONT-016); no location references in relations (ONT-016); model
literal scan (ONT-039/088); vectors-in-authored-content scan (ONT-086);
exception grammar only in ENF/WVR (ONT-056/057).
Emits an evidence record (EVID-) per run.
"""
import sys, re, json, hashlib, datetime, pathlib
import yaml, jsonschema

from paths import (ACTA, CORPUS as CORPUS_DEFAULT, REPO, SCHEMA as SCHEMA_PATH,
                   resolve as resolve_path)

PREFIX = {"PRIN":"principle","SPEC":"specification","RSTR":"restriction","CTRL":"control",
          "ENF":"enforcement","RULE":"rule","DEC":"decision","MAND":"mandate","STRAT":"strategy",
          "SPRINT":"sprint","STORY":"story","EVID":"evidence","WVR":"waiver","BLK":"blocker",
          "PROV":"provenance-link","DOC":"document","MEM":"memory"}
MODEL_LITERAL = re.compile(r"claude-\d|claude-(opus|sonnet|haiku)|gpt-[345]|gemini-\d|text-embedding-\d", re.I)
LOCATION_REF = re.compile(r"^(\.{0,2}/|[A-Za-z]:\\|https?://|file://)")
BEGIN = re.compile(r"<!--\s*atom:begin\s+id=([A-Z]+-[0-9A-Za-z._-]+)\s*-->")
END   = re.compile(r"<!--\s*atom:end\s+id=([A-Z]+-[0-9A-Za-z._-]+)\s*-->")

# The interim Acta (D17). Records live here and are committed; the generated index
# keeps only regenerable derivations. Retires by decision when the data-access
# citizen's durable consumer exists (PA-007).
ACTA_DIR = "acta"

def parse_file(path):
    """Yield (atom_dict, source, body) from frontmatter and/or ONT-070a blocks.

    `body` is the atom's prose — everything the atom says that is not its machine
    record. It is carried so content-addressed subjects (SPEC-0096) cover what an
    atom actually asserts, not merely which ids exist.
    """
    text = path.read_text()
    atoms, errors = [], []
    # Record form: one committed evidence row per file, the whole file being the
    # atom's machine record. No prose body — a record states what happened, and
    # anything a reader needs is already a field.
    if path.suffix == ".json":
        try:
            rec = json.loads(text)
            if isinstance(rec, dict) and "id" in rec:
                atoms.append((rec, f"{path}::record", ""))
            else:
                errors.append(f"{path}: record has no id")
        except ValueError as e:
            errors.append(f"{path}: record JSON error: {e}")
        return atoms, errors, text
    # frontmatter form
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end > 0:
            try:
                fm = yaml.safe_load(text[4:end])
                if isinstance(fm, dict) and "id" in fm:
                    atoms.append((fm, f"{path}::frontmatter", text[end + 5:]))
            except yaml.YAMLError as e:
                errors.append(f"{path}: frontmatter YAML error: {e}")
    # marker blocks
    pos, opens = 0, []
    for m in re.finditer(r"^<!--\s*atom:(begin|end)\s+id=([A-Z]+-[0-9A-Za-z._-]+)\s*-->", text, re.M):
        kind, aid = m.group(1), m.group(2)
        if kind == "begin":
            if opens: errors.append(f"{path}: nested atom:begin {aid} inside {opens[-1][0]} (nesting prohibited)")
            opens.append((aid, m.end()))
        else:
            if not opens: errors.append(f"{path}: atom:end {aid} without begin"); continue
            oid, start = opens.pop()
            if oid != aid: errors.append(f"{path}: marker id mismatch begin={oid} end={aid}")
            block = text[start:m.start()]
            ym = re.search(r"```yaml\n(.*?)```", block, re.S)
            if not ym: errors.append(f"{path}: atom {aid}: no yaml block"); continue
            try:
                rec = yaml.safe_load(ym.group(1))
                if isinstance(rec, dict): atoms.append((rec, f"{path}::{aid}", block[ym.end():]))
                else: errors.append(f"{path}: atom {aid}: yaml is not a mapping")
            except yaml.YAMLError as e:
                errors.append(f"{path}: atom {aid}: YAML error: {e}")
    for oid, _ in opens: errors.append(f"{path}: atom:begin {oid} never closed")
    return atoms, errors, text

def ref_id(r): return r if isinstance(r, str) else (r or {}).get("id")

def corpus_digest(all_atoms):
    """SPEC-0096: the evidence subject is content-addressed.

    Digest over the sorted sequence of (id, version, canonical atom record, prose
    body). Hashing the id set alone — the prior behaviour — meant editing any
    atom's text left the subject unchanged, so ONT-046's "current evidence against
    the current subject digest" could not detect content drift at all.
    """
    h = hashlib.sha256()
    for aid in sorted(all_atoms):
        a, _src, body = all_atoms[aid]
        # Evidence is excluded deliberately. A subject digest answers "what was
        # checked", so folding the record of checks into it would mean every run
        # changed the thing it was checking: no evidence row could ever be current
        # for a corpus that contains it. Records are validated and resolvable
        # (SPEC-0106) without being part of the subject.
        if a.get("type") == "evidence":
            continue
        h.update(json.dumps({"id": aid, "version": str(a.get("version", "")),
                             "record": a, "body": body},
                            sort_keys=True, separators=(",", ":"), default=str).encode())
    return h.hexdigest()[:16]

def expand_inputs(inputs):
    """Accept files and directories alike (SPEC-0092): a directory contributes its
    *.md tree plus any acta/ evidence rows, and a file contributes itself. A path
    that does not exist is a finding, never a silent zero.

    SPEC-0106/D17: evidence rows are records, not derived data. They are committed
    under acta/ and loaded here so an EVID- id is a resolvable reference like any
    other — which is what ONT-046/048 always implied. Derived data (vectors, query
    reports) stays in the ignored index and is never loaded as an atom.
    """
    files, errors, seen = [], [], set()

    def add(q):
        # Dedupe on the resolved path: the same file reached by two spellings
        # (corpus/../acta and ../platform/acta) is one file, not a duplicate id.
        key = q.resolve()
        if key not in seen:
            seen.add(key)
            files.append(q)

    for i in inputs:
        p = resolve_path(i)
        # A path outside the repository is never an intended subject. `..` is
        # cwd-relative by nature, so `atom_lint.py ..` means the repository root from
        # platform/ and the filesystem root from /tmp — the same footgun SPEC-0114
        # removed from the tool, still reachable through the argument. Refuse rather
        # than lint whatever happens to be up there.
        try:
            resolved = p.resolve()
            outside = REPO.resolve() not in resolved.parents and resolved != REPO.resolve()
        except OSError:
            outside = True
        if outside and not str(resolved).startswith("/tmp"):
            errors.append(f"{i}: resolves to {resolved}, outside the repository "
                          f"({REPO}) — refusing to lint outside the tree it governs")
            continue
        if p.is_dir():
            for q in sorted(p.rglob("*.md")):
                add(q)
            for q in sorted(q for q in p.rglob("*.json") if ACTA_DIR in q.parts):
                add(q)
            # Governed corpus content now cites records (a blocker's resolved_by,
            # an evidence satisfies), so linting the corpus without the Acta would
            # report those citations as unresolved. Pull in the sibling acta/ so
            # the documented `atom_lint.py corpus` keeps meaning what it says.
            for candidate in (p / ACTA_DIR, p.parent / ACTA_DIR):
                if candidate.is_dir():
                    for q in sorted(candidate.rglob("*.json")):
                        add(q)
        elif p.is_file(): add(p)
        else: errors.append(f"{i}: input path does not exist")
    return files, errors

def atom_content_hash(atom, body):
    """Canonical content of one atom instance, excluding the fields that identify
    *which* instance it is. Two instances with the same hash say the same thing."""
    record = {k: v for k, v in atom.items() if k not in ("version", "instantiated_at")}
    return hashlib.sha256(json.dumps({"record": record, "body": body},
                                     sort_keys=True, separators=(",", ":"),
                                     default=str).encode()).hexdigest()[:16]


def repo_of(paths):
    """The repository that owns the corpus being linted — not necessarily the one the
    tool lives in. Resolving the ref against the tool's own repo would compare a
    corpus against an unrelated history and silently find nothing to complain about,
    which is how this was first written and how the fixture caught it."""
    import subprocess
    for candidate in list(paths) + [str(CORPUS_DEFAULT)]:
        q = resolve_path(candidate)
        d = q if q.is_dir() else q.parent
        if not d.exists():
            continue
        r = subprocess.run(["git", "-C", str(d), "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            return pathlib.Path(r.stdout.strip())
    return REPO


def atoms_at(ref, repo):
    """Parse the corpus as it stood at a git ref, via a throwaway export.

    Reading the tree at a ref rather than diffing files means an atom that moved
    between files is still recognised as the same atom — governance attaches to ids,
    never to filenames (ONT-002).
    """
    import subprocess, tempfile, tarfile, io
    r = subprocess.run(["git", "-C", str(repo), "archive", ref],
                       capture_output=True)
    if r.returncode:
        return None, f"cannot read tree at {ref}: {r.stderr.decode()[:200]}"
    out = {}
    with tempfile.TemporaryDirectory() as td:
        with tarfile.open(fileobj=io.BytesIO(r.stdout)) as tar:
            tar.extractall(td, filter="data")
        base = pathlib.Path(td)
        for f in list(base.rglob("*.md")) + [q for q in base.rglob("*.json")
                                             if ACTA_DIR in q.parts]:
            parsed, _errs, _text = parse_file(f)
            for a, _src, body in parsed:
                if "id" in a:
                    # The full prior instance, because SPEC-0119 compares fields and
                    # not merely a content hash.
                    out[a["id"]] = (a, body)
    return out, None


# SPEC-0121 / D44: the tree-shape gate. SPEC-0091's canonical-tree clause had no
# control behind it and was violated twice with every gate green, because a prose-only
# document changes no atom digest — the corpus looks identical whether the file was
# admitted or abandoned at the root.
ROOT_ALLOWLIST = {"CLAUDE.md", "README.md", "LICENSE", "LICENSE.md",
                  "CONTRIBUTING.md", "SECURITY.md", "CODE_OF_CONDUCT.md"}
GOVERNED_NAME = re.compile(r"^(DOC|DEC|SPEC|RSTR|CTRL|ENF|RULE|MAND|STRAT|SPRINT|"
                           r"STORY|EVID|WVR|BLK|PROV|MEM|PRIN)-|^ARCHITECT_RESPONSE_")


def tree_findings(repo):
    """Every *.md is governed, allowlisted, or a violation."""
    repo = pathlib.Path(repo)
    corpus = (repo / "platform" / "corpus").resolve()
    findings = []
    for p in sorted(repo.rglob("*.md")):
        if any(part.startswith(".") or part in ("node_modules", "__pycache__")
               for part in p.parts):
            continue
        resolved = p.resolve()
        if corpus in resolved.parents:
            continue                       # governed: parsed and validated elsewhere
        rel = resolved.relative_to(repo.resolve())
        if len(rel.parts) == 1 and rel.name in ROOT_ALLOWLIST:
            continue                       # enumerated root allowlist
        text = p.read_text(encoding="utf-8", errors="replace")
        carries_atoms = bool(re.search(r"^<!--\s*atom:begin\s", text, re.M))
        governed_name = bool(GOVERNED_NAME.match(rel.name))
        if carries_atoms or governed_name:
            why = "carries atom markers" if carries_atoms else "governed naming family"
            findings.append(
                f"{rel}: governed document outside platform/corpus ({why}) — "
                f"SPEC-0091's canonical tree is the only home for governed content "
                f"(SPEC-0121). Fixtures and test data belong under a tools/ or suite/ "
                f"path that does not look governed.")
    return findings


def provenance_findings(atoms, before):
    """SPEC-0119 / D41: a new version must carry a new authoring act.

    SPEC-0113 catches content moving without a version bump. This catches the level
    beneath — the version moved but the provenance did not, so the instance claims the
    previous instance's moment or the previous instance's author. Lint passed on
    exactly that during the DEC-0004 amendment.
    """
    findings = []
    for aid, (atom, src, body) in atoms.items():
        prior = before.get(aid)
        if prior is None:
            continue
        old_atom, old_body = prior
        old_v, new_v = str(old_atom.get("version", "")), str(atom.get("version", ""))
        if new_v == old_v:
            continue
        if str(atom.get("instantiated_at", "")) == str(old_atom.get("instantiated_at", "")):
            findings.append(
                f"{src}: {aid} version moved {old_v} -> {new_v} with instantiated_at "
                f"unchanged ({atom.get('instantiated_at')}) — an instance claiming "
                f"the previous instance's moment is not a new instance (ONT-015).")
        if (atom.get("author") == RECONCILER
                and _changed_beyond_lifecycle(atom, body, old_atom, old_body)):
            findings.append(
                f"{src}: {aid} carries changes beyond a lifecycle transition while "
                f"authored by {RECONCILER}, whose only legitimate change is that "
                f"transition — an amendment is authored by whoever amended it "
                f"(ONT-010).")
    return findings


RECONCILER = "ont-060-reconciliation"


def _changed_beyond_lifecycle(atom, body, old_atom, old_body):
    """True when more than `state` moved between the two instances.

    The reconciler legitimately writes `state` (and the identity fields the content
    hash already ignores); anything else appearing under its name is a
    misattribution, which is precisely what the DEC-0004 near-miss would have been.
    """
    def strip(a):
        return {k: v for k, v in a.items() if k not in ("state", "author")}
    return atom_content_hash(strip(atom), body) != atom_content_hash(strip(old_atom), old_body)


def immutability_findings(atoms, ref, repo):
    """SPEC-0113: ONT-012/015 made structural.

    An atom whose content changed while (version, instantiated_at) stayed put is an
    edit to a published instance. Immutability had been a convention enforced by
    reviewer attention; this is the same law enforced by the gate.
    """
    before, err = atoms_at(ref, repo)
    if err:
        return [err]
    findings = []
    for aid, (atom, src, body) in atoms.items():
        prior = before.get(aid)
        if prior is None:
            continue  # new atom: nothing to compare against
        old_atom, old_body = prior
        same_identity = (
            str(atom.get("version", "")) == str(old_atom.get("version", ""))
            and str(atom.get("instantiated_at", "")) == str(old_atom.get("instantiated_at", "")))
        if same_identity and atom_content_hash(atom, body) != atom_content_hash(old_atom, old_body):
            findings.append(
                f"{src}: {aid} content changed at unchanged instance identity "
                f"(version {atom.get('version')}, instantiated_at "
                f"{atom.get('instantiated_at')}) — a published instance was edited "
                f"in place (ONT-012/015). Emit a new instance instead.")
    # SPEC-0119 rides the same tree comparison: both questions are about what moved
    # between two instances, and reading the ref twice would be wasteful and could
    # disagree with itself.
    findings += provenance_findings(atoms, before)
    return findings


def lint(corpus_dirs, schema_path):
    schema = json.loads(pathlib.Path(schema_path).read_text())
    validators = {t: jsonschema.Draft202012Validator({**schema, "$ref": f"#/$defs/{t}"}) for t in PREFIX.values()}
    all_atoms, texts = {}, {}
    files, errors = expand_inputs(corpus_dirs)
    for p in files:
        atoms, errs, text = parse_file(p); errors += errs; texts[p] = text
        for a, src, body in atoms:
            aid = a.get("id", "?")
            if aid in all_atoms: errors.append(f"{src}: duplicate id {aid} (also {all_atoms[aid][1]})")
            all_atoms[aid] = (a, src, body)
    for aid, (a, src, body) in all_atoms.items():
        pfx = aid.split("-")[0]
        t = a.get("type")
        if PREFIX.get(pfx) != t: errors.append(f"{src}: prefix {pfx} does not match type {t}")
        v = validators.get(t)
        if v is None: errors.append(f"{src}: unknown type {t}"); continue
        for e in v.iter_errors(a): errors.append(f"{src}: schema: {e.message}")
        # ONT-030: rule claim must be SPEC/RSTR
        if t == "rule":
            c = ref_id(a.get("claim", ""))
            if c and not c.startswith(("SPEC-", "RSTR-")): errors.append(f"{src}: rule claim {c} is not SPEC-/RSTR- (ONT-030)")
        # ONT-056: exception grammar only in ENF/WVR — schema shape enforces; scan others
        if t not in ("enforcement", "waiver") and ("conditions" in a or "condition" in a):
            errors.append(f"{src}: exception-grammar field on type {t} (ONT-056)")
        # ONT-086: no vectors in authored content
        if any(k in a for k in ("vector", "embedding")): errors.append(f"{src}: embedding field in authored atom (ONT-086)")
        # ONT-016: relations must be id references, never locations
        for r in a.get("relations", []) or []:
            tgt = r.get("target", "")
            if LOCATION_REF.match(str(tgt)): errors.append(f"{src}: location reference '{tgt}' in relations (ONT-016)")
        # reference resolution (targets that look like atom ids, wildcards exempt)
        def check(refv, field):
            rid = ref_id(refv)
            if rid and "*" not in rid and rid not in all_atoms:
                errors.append(f"{src}: unresolved reference {rid} in {field} (ONT-016)")
        for r in a.get("relations", []) or []:
            if re.fullmatch(r"[A-Z]+-[0-9A-Za-z._-]+", str(r.get("target",""))): check(r["target"], "relations")
        for f in ("claim","control","enforcement","rule_ref","arc_ref","sprint_ref","story_ref","control_ref","decision_ref","resolved_by"):
            if f in a and a[f]: check(a[f], f)
        for f in ("acceptance","stories","constraints"):
            for rv in a.get(f) or []: check(rv, f)
    # ONT-039/088: model literal scan across all governed text
    for p, text in texts.items():
        for m in MODEL_LITERAL.finditer(text):
            line = text[:m.start()].count("\n") + 1
            errors.append(f"{p}:{line}: model literal '{m.group(0)}' (ONT-039: band labels only)")
    # SPEC-0092: the null case is a failure. A control that checked nothing must never
    # report pass — ENT-094's fail-closed law applied to controls themselves.
    if not all_atoms:
        errors.append(f"empty-input: zero atoms parsed from {list(corpus_dirs)} "
                      f"({len(files)} file(s) read) — a check over nothing is not a pass")
    return all_atoms, errors

def main():
    import argparse
    ap = argparse.ArgumentParser(description="atom-lint (CTRL-0001)")
    ap.add_argument("paths", nargs="*", default=None,
                    help="files or directories to lint (default: the platform corpus)")
    ap.add_argument("--tree", action="store_true",
                    help="check repository tree shape (SPEC-0121): every *.md is "
                         "governed, allowlisted, or a violation")
    ap.add_argument("--since", default=None, metavar="REF",
                    help="also check instance immutability against a git ref "
                         "(SPEC-0113): content may not change without a new "
                         "(version, instantiated_at)")
    a = ap.parse_args()
    corpus = a.paths or ["corpus"]
    schema = str(SCHEMA_PATH)
    atoms, errors = lint(corpus, schema)
    if a.since:
        errors = errors + immutability_findings(atoms, a.since, repo_of(corpus))
    if a.tree or a.since:
        # SPEC-0121: a repository property, so it is checked when the repository is
        # the subject — whole-tree lint or a --since comparison.
        errors = errors + tree_findings(repo_of(corpus))
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    digest = corpus_digest(atoms)
    governed = sum(1 for a, _s, _b in atoms.values() if a.get("type") != "evidence")
    verdict = "pass" if not errors else "fail"
    # SPEC-0092: the parsed-atom count rides in the subject, so a vacuous run cannot
    # masquerade in the evidence stream even where the exit code is swallowed.
    evid = {"id": f"EVID-lint-{now[:19].replace(':','')}", "type": "evidence", "scope": "platform",
            "state": "active", "version": "1.0.0", "instantiated_at": now,
            "author": "ctrl-0001-atom-lint", "authorized_by": None,
            "title": f"atom-lint run over {len(atoms)} atoms", "control_ref": "CTRL-0001",
            # The count annotates the digest, so it counts what the digest covers:
            # governed atoms, not the evidence records excluded from it above.
            "subject": f"corpus@{digest}#atoms={governed}", "verdict": verdict,
            "checked_at": now, "checker": "ctrl-0001-atom-lint"}
    if not atoms: evid["reason"] = "empty-input"
    ACTA.mkdir(exist_ok=True)
    (ACTA / f"{evid['id']}.json").write_text(json.dumps(evid, indent=1))
    print(f"atoms parsed: {len(atoms)}")
    by_type = {}
    for aid,(a,_src,_body) in atoms.items(): by_type[a.get('type','?')] = by_type.get(a.get('type','?'),0)+1
    print("by type:", json.dumps(by_type))
    if errors:
        print(f"\nFAIL — {len(errors)} finding(s):")
        for e in errors[:40]: print("  •", e)
        if len(errors) > 40: print(f"  … and {len(errors)-40} more")
        sys.exit(1)
    print(f"\nPASS — evidence {evid['id']} emitted (subject {evid['subject']})")

if __name__ == "__main__": main()
