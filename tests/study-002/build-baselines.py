#!/usr/bin/env python3
"""Study 002, Step 1 — Baselines for Table B. NO test verdicts in this step.

David's Step 1 command (filed 2026-11-27), adapted to the tables as
built — adaptations, all mechanical:
- Table B's columns are corpus/book/ref (not tradition/verse_id) and it
  carries no stream column; streams are read from scripture/ TSVs,
  joined on (corpus, book, ref).
- Surrogate length matching uses n_letters ± 2 (the filed intent);
  David's draft compared verse_total against letter count. Where no
  same-book verse falls within ± 2 (1,255 verses in the first build),
  the pool falls back to the whole book — David's draft rule.
- Verses with right_sum = 0 have no distance (Table B leaves it blank);
  they are excluded from distance statistics and counted in the manifest.
Outputs: per-verse SUMMARY csvs under baselines/{shuffle,surrogate}-200/
(small, for the repo) and FULL per-draw csvs under baselines/full/
(archived with the run; hashes in baselines-manifest.json).
Seed 42, 200 shuffles, 200 surrogates — as filed.
"""
import csv, hashlib, json
from pathlib import Path
from multiprocessing import Pool
import numpy as np

ROOT = Path("tests/study-002")
OUT = ROOT / "baselines"
SEED = 42
N = 200
CORPORA = ["tanakh", "nt", "quran-simple", "quran-uthmani"]

def f25(v):
    a = b = 0
    while v > 1 and v % 2 == 0: v //= 2; a += 1
    while v > 1 and v % 5 == 0: v //= 5; b += 1
    return a + b

def stats(stream):
    n = len(stream); h = n // 2
    ex = [f25(v) for v in stream]
    left, right = sum(ex[:h]), sum(ex[n - h:])
    dist = abs(left / right - 1) if right else None
    if n >= 3:
        x = np.asarray(stream, dtype=float)
        lag1 = float(np.corrcoef(x[:-1], x[1:])[0, 1]) if x[:-1].std() and x[1:].std() else 0.0
    else: lag1 = 0.0
    return left, right, dist, lag1

def load_streams(corpus):
    streams = {}
    for tsv in sorted(Path("scripture", corpus).glob("*.tsv")):
        with open(tsv, encoding="utf-8") as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                streams[(tsv.stem, r["ref"])] = [int(t) for t in r["std_stream"].split()]
    return streams

def work(args):
    idx, corpus, book, ref, stream, pool = args
    rng = np.random.default_rng(SEED + idx)
    x = np.asarray(stream)
    sh_rows, dists, lag1s = [], [], []
    for s in range(N):
        sh = rng.permutation(x).tolist()
        l, r, d, g = stats(sh)
        sh_rows.append([corpus, book, ref, s, l, r, f"{d:.6f}" if d is not None else "", f"{g:.6f}"])
        if d is not None: dists.append(d)
        lag1s.append(g)
    su_rows, sdists, slag1s = [], [], []
    if pool:
        picks = rng.integers(0, len(pool), size=N)
        for s, pi in enumerate(picks):
            sv = pool[int(pi)]
            l, r, d, g = stats(sv)
            su_rows.append([corpus, book, ref, s, l, r, f"{d:.6f}" if d is not None else "", f"{g:.6f}"])
            if d is not None: sdists.append(d)
            slag1s.append(g)
    def summ(ds, gs):
        if not ds: return [""] * 6
        a = np.array(ds); g = np.array(gs)
        return [f"{a.mean():.6f}", f"{a.std():.6f}", f"{np.percentile(a,5):.6f}",
                f"{np.percentile(a,95):.6f}", f"{g.mean():.6f}", f"{g.std():.6f}"]
    return (sh_rows, [corpus, book, ref] + summ(dists, lag1s),
            su_rows, [corpus, book, ref, len(pool)] + summ(sdists, slag1s))

def main():
    B = {}
    with open(ROOT / "tables/table-B-verse.csv") as fh:
        for r in csv.DictReader(fh): B[(r["corpus"], r["book"], r["ref"])] = r
    (OUT / "shuffle-200").mkdir(parents=True, exist_ok=True)
    (OUT / "surrogate-200").mkdir(exist_ok=True)
    (OUT / "full").mkdir(exist_ok=True)
    manifest = {"seed": SEED, "n_shuffle": N, "n_surrogate": N,
                "spec": "halves, center letter standing in neither, 2^a*5^b only",
                "corpora": {}}
    idx = 0
    sh_summ, su_summ = [], []
    for corpus in CORPORA:
        streams = load_streams(corpus)
        by_book = {}
        for (book, ref), st in streams.items(): by_book.setdefault(book, []).append((ref, st))
        tasks = []
        for (book, ref), st in sorted(streams.items()):
            n = len(st)
            pool = [s2 for (r2, s2) in by_book[book] if r2 != ref and abs(len(s2) - n) <= 2]
            if not pool:
                # David's draft rule: no same-length candidates -> whole book.
                pool = [s2 for (r2, s2) in by_book[book] if r2 != ref]
            tasks.append((idx, corpus, book, ref, st, pool)); idx += 1
        with Pool(16) as p:
            results = p.map(work, tasks, chunksize=64)
        with open(OUT / "full" / f"shuffle-full-{corpus}.csv", "w", newline="") as fh:
            w = csv.writer(fh); w.writerow(["corpus", "book", "ref", "draw", "left_sum", "right_sum", "distance_from_1", "lag1"])
            for sh_rows, _, _, _ in results: w.writerows(sh_rows)
        with open(OUT / "full" / f"surrogate-full-{corpus}.csv", "w", newline="") as fh:
            w = csv.writer(fh); w.writerow(["corpus", "book", "ref", "draw", "left_sum", "right_sum", "distance_from_1", "lag1"])
            for _, _, su_rows, _ in results: w.writerows(su_rows)
        sh_summ += [r[1] for r in results]; su_summ += [r[3] for r in results]
        manifest["corpora"][corpus] = {"verses": len(tasks),
                                       "verses_right_sum_zero": sum(1 for r in results if r[1][3] == "")}
        print("done", corpus, len(tasks), flush=True)
    hdr = ["corpus", "book", "ref", "dist_mean", "dist_sd", "dist_p05", "dist_p95", "lag1_mean", "lag1_sd"]
    with open(OUT / "shuffle-200/summary.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(hdr); w.writerows(sh_summ)
    with open(OUT / "surrogate-200/summary.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["corpus", "book", "ref", "pool_size", "dist_mean", "dist_sd", "dist_p05", "dist_p95", "lag1_mean", "lag1_sd"]); w.writerows(su_summ)
    def sha(p):
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""): h.update(chunk)
        return h.hexdigest()
    manifest["sha256"] = {}
    for p in sorted(OUT.rglob("*.csv")): manifest["sha256"][str(p.relative_to(OUT))] = sha(p)
    manifest["sha256"]["tables/table-B-verse.csv"] = sha(ROOT / "tables/table-B-verse.csv")
    with open(OUT / "baselines-manifest.json", "w") as f: json.dump(manifest, f, indent=2)
    print(json.dumps(manifest["corpora"], indent=2))
    print("DONE — Step 1 baselines built. No verdicts filed.")

if __name__ == "__main__":
    main()
