#!/usr/bin/env python3
"""Embedder pipeline (ONT-085–089) + index with standing queries (CTRL-0008 subset).

Instruments are pluggable and digest-pinned (ONT-088). Band resolution happens
here — never a model literal in configuration. The shipped instrument is a
deterministic local lexical vectorizer (TF-IDF), honestly labeled: it proves
the pipeline (chunking, provenance, coverage, retrieval mechanics); a semantic
model resolves into the same band slot at deployment without pipeline change.
"""
import sys, json, hashlib, datetime, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from atom_lint import parse_file

BAND_REGISTRY = {  # band -> (instrument name, resolver) — resolved at run, digest-pinned below
    "B0": "tfidf-local-lexical",
}

def resolve_instrument(band):
    from sklearn.feature_extraction.text import TfidfVectorizer
    name = BAND_REGISTRY[band]
    impl_digest = hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()[:16]
    return name, f"{name}@{impl_digest}", TfidfVectorizer(stop_words="english", max_features=512)

def atom_text(a, block_prose=""):
    parts = [a.get("title",""), a.get("type",""), " ".join(a.get("tags",[]) or [])]
    for k in ("question","outcome","horizon"): parts.append(str(a.get(k,"")))
    parts.append(block_prose)
    return " ".join(p for p in parts if p)

def build(corpus_dirs, band="B0"):
    instrument, digest, vec = resolve_instrument(band)
    rows, texts = [], []
    for d in corpus_dirs:
        for p in sorted(pathlib.Path(d).rglob("*.md")):
            atoms, errs, _ = parse_file(p)
            for a, src in atoms:
                if "id" not in a: continue
                rows.append({"atom_id": a["id"], "version": str(a.get("version","")),
                             "instantiated_at": str(a.get("instantiated_at","")),
                             "embedding_model_band": band, "embedding_model_digest": digest,
                             "embedded_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                             "type": a.get("type"), "state": a.get("state"), "title": a.get("title","")})
                texts.append(atom_text(a))
    M = vec.fit_transform(texts)
    for i, r in enumerate(rows): r["vector"] = [round(float(x),5) for x in M[i].toarray()[0]]
    idx = {"model_generation": digest, "vocabulary_size": len(vec.vocabulary_), "rows": rows}
    pathlib.Path("index/embeddings.json").write_text(json.dumps(idx))
    return idx, vec, M, rows

def queries(corpus_dirs, idx):
    """Standing queries per ONT-080/089 + ENT-041 (computable subset)."""
    atoms = {}
    for d in corpus_dirs:
        for p in sorted(pathlib.Path(d).rglob("*.md")):
            parsed, _, _ = parse_file(p)
            for a, src in parsed:
                if "id" in a: atoms[a["id"]] = a
    def rid(x): return x if isinstance(x,str) else (x or {}).get("id")
    bound = {rid(a.get("claim")) for a in atoms.values() if a.get("type")=="rule"}
    claims = [i for i,a in atoms.items() if a.get("type") in ("specification","restriction")]
    dangling = sorted(i for i in claims if i not in bound)
    evidenced = {rid(json.loads(f.read_text()).get("control_ref"))
                 for f in pathlib.Path("index").glob("EVID-*.json")
                 if json.loads(f.read_text()).get("verdict")=="pass"}
    rules_unevidenced = sorted(i for i,a in atoms.items() if a.get("type")=="rule"
                               and rid(a.get("control")) not in evidenced)
    embedded = {r["atom_id"] for r in idx["rows"] if r["embedding_model_digest"]==idx["model_generation"]}
    coverage_gap = sorted(set(atoms) - embedded)
    return {"total_atoms": len(atoms), "claims": len(claims),
            "dangling_claims": dangling, "rules_without_passing_evidence": len(rules_unevidenced),
            "controls_with_passing_evidence": sorted(x for x in evidenced if x),
            "embedding_coverage_gap": coverage_gap}

def search(q, vec, M, rows, k=5):
    from sklearn.metrics.pairwise import cosine_similarity
    sims = cosine_similarity(vec.transform([q]), M)[0]
    top = sims.argsort()[::-1][:k]
    return [(rows[i]["atom_id"], round(float(sims[i]),3), rows[i]["title"]) for i in top if sims[i] > 0]

PROVENANCE_FIELDS = ("atom_id", "version", "instantiated_at",
                     "embedding_model_band", "embedding_model_digest", "embedded_at")

def emit_evidence(idx, rows, rep, corpus_digest):
    """SPEC-0093 / PA-005: a pipeline run records. Scope is deliberately narrow —
    the two CTRL-0007 assertions this pipeline can check on itself: measurement
    provenance completeness (ONT-088) and coverage under the current generation
    (ONT-089). CTRL-0007's full suite (tools/test_embedder.py) does not exist yet,
    so this row must not be read as a complete CTRL-0007 verdict."""
    incomplete = [r["atom_id"] for r in rows if any(not r.get(f) for f in PROVENANCE_FIELDS)]
    gap = rep["embedding_coverage_gap"]
    verdict = "pass" if not incomplete and not gap else "fail"
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    evid = {"id": f"EVID-embed-{now[:19].replace(':','')}", "type": "evidence", "scope": "platform",
            "state": "active", "version": "1.0.0", "instantiated_at": now,
            "author": "embedder-pipeline", "authorized_by": None,
            "title": f"embedder pipeline: {len(rows)} instances, provenance complete, "
                     f"coverage gap {len(gap)} (partial CTRL-0007: suite not yet implemented)",
            "control_ref": "CTRL-0007",
            "subject": f"corpus@{corpus_digest}#atoms={len(rows)}@{idx['model_generation']}",
            "verdict": verdict, "checked_at": now, "checker": "embedder-pipeline",
            "assertions_run": ["ONT-088-provenance-completeness", "ONT-089-coverage"],
            "assertions_not_run": ["ONT-087-chunk-boundary", "ONT-086-generated-rendering"]}
    if incomplete: evid["incomplete_provenance"] = incomplete[:20]
    pathlib.Path("index").mkdir(exist_ok=True)
    pathlib.Path(f"index/{evid['id']}.json").write_text(json.dumps(evid, indent=1))
    return evid

if __name__ == "__main__":
    dirs = ["corpus"]
    idx, vec, M, rows = build(dirs)
    print(f"embedded {len(rows)} instances under generation {idx['model_generation']} (band B0)")
    rep = queries(dirs, idx)
    corpus_digest = hashlib.sha256("".join(sorted(r["atom_id"] for r in rows)).encode()).hexdigest()[:16]
    ev = emit_evidence(idx, rows, rep, corpus_digest)
    print(f"evidence {ev['id']}: {ev['verdict']} (subject {ev['subject']})")
    print(json.dumps({k:(v if not isinstance(v,list) or len(v)<8 else f"{len(v)} items") for k,v in rep.items()}, indent=1))
    pathlib.Path("index/standing_queries.json").write_text(json.dumps(rep, indent=1))
    for q in ["restrictions about credentials and authority escalation",
              "story required before any agent work begins",
              "embedding provenance and model pinning"]:
        print(f"\nquery: {q}")
        for aid, s, t in search(q, vec, M, rows, 3): print(f"  {s:5}  {aid}  {t}")
