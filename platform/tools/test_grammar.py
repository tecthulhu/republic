#!/usr/bin/env python3
"""CTRL-0002: grammar property suite. Reference implementation of the ENT-091–095
caveat algebra plus randomized property tests. Emits evidence."""
import random, json, datetime, pathlib, operator, sys

FACTS = {"now","mint_time","lease_age","subject","action","resource","audience","use_count","depth","parent_id","lease_id"}
OPS = {"=":operator.eq,"!=":operator.ne,"<":operator.lt,"<=":operator.le,">":operator.gt,">=":operator.ge,
       "in":lambda a,b: a in b, "prefix-of":lambda a,b: str(b).startswith(str(a))}

def check_predicate(pred, facts):
    """ENT-094: fail closed — unknown fact, unknown op, or eval error denies."""
    fact, op, lit = pred
    if fact not in FACTS or op not in OPS or fact not in facts: return False
    try: return bool(OPS[op](facts[fact], lit))
    except Exception: return False

def verify(chain, facts):
    """ENT-093/094: union of all caveats along chain; every predicate must hold."""
    return all(check_predicate(p, facts) for caveats in chain for p in caveats)

def reject_exception_construct(caveat_block):
    """ENT-095: any given/when/then structure inside a credential is rejected."""
    return not (isinstance(caveat_block, dict) and {"given","when","then"} & set(caveat_block))

def rand_pred(r):
    f = r.choice(sorted(FACTS - {"subject","action","resource","audience","parent_id","lease_id"}))
    return (f, r.choice(["<","<=",">",">=","="]), r.randint(0,100))

def run():
    r = random.Random(42); failures = []
    N = 200000
    # P1 — attenuation monotonicity (ENT-003/093): adding caveats never grants.
    for _ in range(N//4):
        parent = [[rand_pred(r) for _ in range(r.randint(0,3))]]
        child = parent + [[rand_pred(r) for _ in range(r.randint(1,3))]]
        facts = {f: r.randint(0,100) for f in FACTS}
        if verify(child, facts) and not verify(parent, facts):
            failures.append(("P1-attenuation", parent, child, facts)); break
    # P2 — fail-closed on unknown facts (ENT-094).
    for _ in range(N//4):
        chain = [[("unknown_fact_"+str(r.randint(0,9)), "=", 1)]]
        if verify(chain, {f: 1 for f in FACTS}):
            failures.append(("P2-unknown-fact", chain)); break
    # P3 — no else: a failing predicate always denies; nothing recovers it.
    for _ in range(N//4):
        chain = [[("lease_age","<",10)], [rand_pred(r) for _ in range(2)]]
        facts = {f: r.randint(0,100) for f in FACTS}; facts["lease_age"] = 50
        if verify(chain, facts):
            failures.append(("P3-no-else", chain, facts)); break
    # P4 — layer separation (ENT-095): exception constructs rejected in credentials.
    for blk in [{"given":"RULE-0001","when":"x","then":"suspend"}, {"lease_age":("<",48)}, [("action","=","read")]]:
        expect = not isinstance(blk, dict) or not ({"given","when","then"} & set(blk))
        if reject_exception_construct(blk) != expect:
            failures.append(("P4-layer-separation", blk))
    # P5 — downward revocation (ENT-051): revoking a node kills its subtree only.
    tree = {"root":None,"persona":"root","lease":"persona","leafA":"lease","leafB":"lease","sibling":"persona"}
    def alive(n, revoked):
        while n is not None:
            if n in revoked: return False
            n = tree[n]
        return True
    revoked = {"lease"}
    if alive("leafA",revoked) or alive("leafB",revoked) or not alive("sibling",revoked) or not alive("persona",revoked):
        failures.append(("P5-revocation",))
    # P6 — decay ladder expressible in the vocabulary (ONT/ENT decay claims).
    ladder = [[("lease_age","<",48)], [("lease_age","<",72),("action","=","read")]]
    fresh = {**{f:0 for f in FACTS}, "lease_age":10, "action":"write"}
    stale = {**{f:0 for f in FACTS}, "lease_age":60, "action":"read"}
    dead  = {**{f:0 for f in FACTS}, "lease_age":80, "action":"read"}
    if not verify([ladder[0]], fresh) or verify(ladder, fresh) or not verify([ladder[1]], stale) or verify([ladder[1]], dead):
        failures.append(("P6-decay",))
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    evid = {"id": f"EVID-grammar-{now[:19].replace(':','')}", "type":"evidence","scope":"platform",
            "state":"active","version":"1.0.0","instantiated_at":now,"author":"ctrl-0002","authorized_by":None,
            "title":"grammar property suite","control_ref":"CTRL-0002","subject":"caveat-algebra@ENT-091..095",
            "verdict":"pass" if not failures else "fail","checked_at":now,"checker":"ctrl-0002-grammar-suite"}
    pathlib.Path("acta").mkdir(exist_ok=True)
    pathlib.Path(f"acta/{evid['id']}.json").write_text(json.dumps(evid, indent=1))
    print(f"properties P1–P6 over ~{N} generated cases: {'PASS' if not failures else 'FAIL'}")
    for f in failures: print("  •", f)
    sys.exit(1 if failures else 0)

if __name__ == "__main__": run()
