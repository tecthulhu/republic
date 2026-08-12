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
from atom_lint import parse_file, corpus_digest, expand_inputs
from paths import ACTA, CORPUS, index_dir

BAND_REGISTRY = {  # band -> (instrument name, resolver) — resolved at run, digest-pinned below
    "B0": "tfidf-local-lexical",
}

PARAMS = {"stop_words": "english", "max_features": 512}

def instrument_manifest(band, params=None):
    """SPEC-0098 / D15: the generation boundary is the instrument, not the harness.

    Hashing the whole tool file made every refactor a re-embedding campaign — it
    conflated instrument identity with the code that happens to call it. The
    manifest is what actually determines the vectors: implementation class, its
    parameters, and the library version (a model digest joins this for semantic
    instruments). Refactor freely; change a parameter and the generation moves,
    which is exactly when it should.
    """
    import sklearn
    return {"instrument": BAND_REGISTRY[band], "band": band,
            "class": "sklearn.feature_extraction.text.TfidfVectorizer",
            "params": dict(PARAMS if params is None else params),
            "library": f"scikit-learn=={sklearn.__version__}"}

def manifest_digest(manifest):
    return hashlib.sha256(json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:16]

def resolve_instrument(band):
    from sklearn.feature_extraction.text import TfidfVectorizer
    manifest = instrument_manifest(band)
    name = manifest["instrument"]
    return name, f"{name}@{manifest_digest(manifest)}", TfidfVectorizer(**manifest["params"]), manifest

def atom_text(a, block_prose=""):
    parts = [a.get("title",""), a.get("type",""), " ".join(a.get("tags",[]) or [])]
    for k in ("question","outcome","horizon"): parts.append(str(a.get(k,"")))
    parts.append(block_prose)
    return " ".join(p for p in parts if p)

def build(corpus_dirs, band="B0"):
    instrument, digest, vec, manifest = resolve_instrument(band)
    rows, texts, all_atoms = [], [], {}
    # SPEC-0109 / D25: the discovery set spans acta/ as well as the governed
    # documents. ONT-085 exempts no type, and evidence rows are atoms — searchable
    # provenance ("what has failed before like this") is half the value of having a
    # semantic substrate at all. expand_inputs is shared with atom-lint so the two
    # controls can never disagree about what the corpus contains.
    files, _ = expand_inputs(corpus_dirs)
    for p in files:
        atoms, errs, _ = parse_file(p)
        for a, src, body in atoms:
            if "id" not in a: continue
            all_atoms[a["id"]] = (a, src, body)
            rows.append({"atom_id": a["id"], "version": str(a.get("version","")),
                         "instantiated_at": str(a.get("instantiated_at","")),
                         "embedding_model_band": band, "embedding_model_digest": digest,
                         "embedded_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                         "type": a.get("type"), "state": a.get("state"), "title": a.get("title","")})
            texts.append(atom_text(a))
    M = vec.fit_transform(texts)
    for i, r in enumerate(rows): r["vector"] = [round(float(x),5) for x in M[i].toarray()[0]]
    idx = {"model_generation": digest, "instrument_manifest": manifest,
           "corpus_digest": corpus_digest(all_atoms),
           "vocabulary_size": len(vec.vocabulary_), "rows": rows}
    # index/ is git-ignored, so on a clean checkout it does not exist. It used to be
    # created as a side effect of evidence emission; since records moved to acta/
    # (SPEC-0106), nothing else creates it and this write has to.
    (index_dir() / "embeddings.json").write_text(json.dumps(idx))
    return idx, vec, M, rows

def queries(corpus_dirs, idx):
    """Standing queries per ONT-080/089 + ENT-041 (computable subset)."""
    atoms = {}
    # Same discovery set as build() and atom-lint (SPEC-0109): coverage can only be
    # a meaningful target-zero number if the query counts what the pipeline embeds.
    files, _ = expand_inputs(corpus_dirs)
    for p in files:
        parsed, _, _ = parse_file(p)
        for a, src, _body in parsed:
            if "id" in a: atoms[a["id"]] = a
    def rid(x): return x if isinstance(x,str) else (x or {}).get("id")
    # SPEC-0097: two questions, two names. ONT-031 defines the dangling query over
    # *active* claims bound by *active* rules; the all-states line is the
    # bootstrap-phase signal, useful but not the definition. One number must never
    # wear two meanings.
    bound_active = {rid(a.get("claim")) for a in atoms.values()
                    if a.get("type") == "rule" and a.get("state") == "active"}
    bound_any = {rid(a.get("claim")) for a in atoms.values() if a.get("type")=="rule"}
    claims = [i for i,a in atoms.items() if a.get("type") in ("specification","restriction")]
    active_claims = [i for i in claims if atoms[i].get("state") == "active"]
    dangling = sorted(i for i in active_claims if i not in bound_active)
    dangling_all = sorted(i for i in claims if i not in bound_any)
    # D36 / ONT-080a: the coverage meter. Claims that are ratified and waiting for a
    # rule to make them enforceable (ONT-036). `dangling` cannot answer this — ONT-060
    # activates a claim only when a rule binds it, so it reads zero at activation by
    # construction and measures drift instead. Two questions, two names.
    ratified_claims = [i for i in claims if atoms[i].get("state") == "ratified"]
    unbound = sorted(i for i in ratified_claims if i not in bound_active)
    evidenced = {rid(json.loads(f.read_text()).get("control_ref"))
                 for f in ACTA.glob("EVID-*.json")
                 if json.loads(f.read_text()).get("verdict")=="pass"}
    rules_unevidenced = sorted(i for i,a in atoms.items() if a.get("type")=="rule"
                               and rid(a.get("control")) not in evidenced)
    embedded = {r["atom_id"] for r in idx["rows"] if r["embedding_model_digest"]==idx["model_generation"]}
    coverage_gap = sorted(set(atoms) - embedded)
    return {"total_atoms": len(atoms), "claims": len(claims), "active_claims": len(active_claims),
            "unbound_claims": unbound,
            "dangling_claims": dangling,
            "dangling_claims_all_states": dangling_all,
            "rules_without_passing_evidence": len(rules_unevidenced),
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
    the two assertions this pipeline can check on itself: measurement provenance
    completeness (ONT-088) and coverage under the current generation (ONT-089).
    The full CTRL-0007 verdict comes from tools/test_embedder.py; this row says
    only that a build ran and what it observed while running."""
    incomplete = [r["atom_id"] for r in rows if any(not r.get(f) for f in PROVENANCE_FIELDS)]
    gap = rep["embedding_coverage_gap"]
    verdict = "pass" if not incomplete and not gap else "fail"
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    evid = {"id": f"EVID-embed-{now[:19].replace(':','')}", "type": "evidence", "scope": "platform",
            "state": "active", "version": "1.0.0", "instantiated_at": now,
            "author": "embedder-pipeline", "authorized_by": None,
            "title": f"embedder pipeline build: {len(rows)} instances, provenance complete, "
                     f"coverage gap {len(gap)} (build-time observation; CTRL-0007 verdict is the suite)",
            "control_ref": "CTRL-0007",
            "subject": f"corpus@{corpus_digest}#atoms={len(rows)}@{idx['model_generation']}",
            "verdict": verdict, "checked_at": now, "checker": "embedder-pipeline",
            "assertions_run": ["ONT-088-provenance-completeness", "ONT-089-coverage"],
            "assertions_not_run": ["ONT-087-chunk-boundary", "ONT-086-generated-rendering"]}
    if incomplete: evid["incomplete_provenance"] = incomplete[:20]
    ACTA.mkdir(exist_ok=True)
    (ACTA / f"{evid['id']}.json").write_text(json.dumps(evid, indent=1))
    return evid

if __name__ == "__main__":
    dirs = [str(CORPUS)]
    idx, vec, M, rows = build(dirs)
    print(f"embedded {len(rows)} instances under generation {idx['model_generation']} (band B0)")
    rep = queries(dirs, idx)
    ev = emit_evidence(idx, rows, rep, idx["corpus_digest"])
    print(f"evidence {ev['id']}: {ev['verdict']} (subject {ev['subject']})")
    print(json.dumps({k:(v if not isinstance(v,list) or len(v)<8 else f"{len(v)} items") for k,v in rep.items()}, indent=1))
    (index_dir() / "standing_queries.json").write_text(json.dumps(rep, indent=1))
    for q in ["restrictions about credentials and authority escalation",
              "story required before any agent work begins",
              "embedding provenance and model pinning"]:
        print(f"\nquery: {q}")
        for aid, s, t in search(q, vec, M, rows, 3): print(f"  {s:5}  {aid}  {t}")
