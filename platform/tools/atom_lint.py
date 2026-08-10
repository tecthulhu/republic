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

def parse_file(path):
    """Yield (atom_dict, source) from frontmatter and/or ONT-070a blocks."""
    text = path.read_text()
    atoms, errors = [], []
    # frontmatter form
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end > 0:
            try:
                fm = yaml.safe_load(text[4:end])
                if isinstance(fm, dict) and "id" in fm:
                    atoms.append((fm, f"{path}::frontmatter"))
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
                body = yaml.safe_load(ym.group(1))
                if isinstance(body, dict): atoms.append((body, f"{path}::{aid}"))
                else: errors.append(f"{path}: atom {aid}: yaml is not a mapping")
            except yaml.YAMLError as e:
                errors.append(f"{path}: atom {aid}: YAML error: {e}")
    for oid, _ in opens: errors.append(f"{path}: atom:begin {oid} never closed")
    return atoms, errors, text

def ref_id(r): return r if isinstance(r, str) else (r or {}).get("id")

def lint(corpus_dirs, schema_path):
    schema = json.loads(pathlib.Path(schema_path).read_text())
    validators = {t: jsonschema.Draft202012Validator({**schema, "$ref": f"#/$defs/{t}"}) for t in PREFIX.values()}
    all_atoms, errors, texts = {}, [], {}
    files = [p for d in corpus_dirs for p in sorted(pathlib.Path(d).rglob("*.md"))]
    for p in files:
        atoms, errs, text = parse_file(p); errors += errs; texts[p] = text
        for a, src in atoms:
            aid = a.get("id", "?")
            if aid in all_atoms: errors.append(f"{src}: duplicate id {aid} (also {all_atoms[aid][1]})")
            all_atoms[aid] = (a, src)
    for aid, (a, src) in all_atoms.items():
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
    return all_atoms, errors

def main():
    corpus = sys.argv[1:] or ["corpus"]
    schema = "schemas/atoms-1.0.0.json"
    atoms, errors = lint(corpus, schema)
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    digest = hashlib.sha256("".join(sorted(atoms)).encode()).hexdigest()[:16]
    verdict = "pass" if not errors else "fail"
    evid = {"id": f"EVID-lint-{now[:19].replace(':','')}", "type": "evidence", "scope": "platform",
            "state": "active", "version": "1.0.0", "instantiated_at": now,
            "author": "ctrl-0001-atom-lint", "authorized_by": None,
            "title": f"atom-lint run over {len(atoms)} atoms", "control_ref": "CTRL-0001",
            "subject": f"corpus@{digest}", "verdict": verdict, "checked_at": now, "checker": "ctrl-0001-atom-lint"}
    pathlib.Path("index").mkdir(exist_ok=True)
    pathlib.Path(f"index/{evid['id']}.json").write_text(json.dumps(evid, indent=1))
    print(f"atoms parsed: {len(atoms)}")
    by_type = {}
    for aid,(a,_) in atoms.items(): by_type[a.get('type','?')] = by_type.get(a.get('type','?'),0)+1
    print("by type:", json.dumps(by_type))
    if errors:
        print(f"\nFAIL — {len(errors)} finding(s):")
        for e in errors[:40]: print("  •", e)
        if len(errors) > 40: print(f"  … and {len(errors)-40} more")
        sys.exit(1)
    print(f"\nPASS — evidence {evid['id']} emitted (subject corpus@{digest})")

if __name__ == "__main__": main()
