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
        p = pathlib.Path(i)
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
    corpus = sys.argv[1:] or ["corpus"]
    schema = "schemas/atoms-1.0.0.json"
    atoms, errors = lint(corpus, schema)
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
    pathlib.Path(ACTA_DIR).mkdir(exist_ok=True)
    pathlib.Path(f"{ACTA_DIR}/{evid['id']}.json").write_text(json.dumps(evid, indent=1))
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
