#!/usr/bin/env python3
"""Study 002, TEST 001b — Level at Fixed Axis Count.
Implements tests/study-002/TEST-001b-LEVEL.md exactly as filed,
including David's rulings of 2026-11-27 (the text governs):
- Ruling 1: a book's consistency counts only buckets where that book
  has >= 10 verses in the bucket; consistent = delta_shuffle > 0 in
  the majority of its qualifying buckets; books with no qualifying
  bucket are not counted. Corpus criterion: >= 2/3 of counted books.
- Ruling 2 (flip clause): any corpus with buckets_pass < 5 (majority
  of buckets real > shuffle) forces overall FAIL, checked first.
- Ruling 3 (Quran forms): quran-simple and quran-uthmani are one
  tradition. Both pass -> Quran passes; both fail -> Quran fails;
  split -> overall FORM-DEPENDENT (cannot be PASS).
Overall precedence: flip -> FAIL; else form split -> FORM-DEPENDENT;
else >= 2 traditions pass -> PASS; else exactly 1 -> DIALECT;
else FAIL.
Reads only Table B and the per-verse baseline summaries already
built (dist_mean = per-verse mean over 200 draws). No new shuffles,
no new surrogates. Numbers only.
Filed and approved by David 2026-11-27.
"""
import csv
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path("tests/study-002")
OUT = ROOT / "results/test-001b-level"
OUT.mkdir(parents=True, exist_ok=True)

B = pd.read_csv(ROOT / "tables/table-B-verse.csv")
B = B[B["distance_from_1"].notna()].copy()
SH = pd.read_csv(ROOT / "baselines/shuffle-200/summary.csv")[
    ["corpus", "book", "ref", "dist_mean"]].rename(columns={"dist_mean": "shuffle_dist"})
SU = pd.read_csv(ROOT / "baselines/surrogate-200/summary.csv")[
    ["corpus", "book", "ref", "dist_mean"]].rename(columns={"dist_mean": "surrogate_dist"})
m = B.merge(SH, on=["corpus", "book", "ref"], how="left").merge(
    SU, on=["corpus", "book", "ref"], how="left")
assert m["shuffle_dist"].notna().all() and m["surrogate_dist"].notna().all()
m["bucket"] = m["axis_count"].clip(upper=8).astype(int)
m["bucket_label"] = m["bucket"].apply(lambda b: "8+" if b == 8 else str(b))

rows = []
for (corpus, b), g in m.groupby(["corpus", "bucket"]):
    rows.append({"corpus": corpus, "bucket": "8+" if b == 8 else str(b),
                 "n_verses": len(g), "n_books": g["book"].nunique(),
                 "real_mean": g["distance_from_1"].mean(),
                 "shuffle_mean": g["shuffle_dist"].mean(),
                 "surrogate_mean": g["surrogate_dist"].mean(),
                 "delta_shuffle": g["shuffle_dist"].mean() - g["distance_from_1"].mean(),
                 "delta_surrogate": g["surrogate_dist"].mean() - g["distance_from_1"].mean()})
level = pd.DataFrame(rows).sort_values(["corpus", "bucket"])
level.to_csv(OUT / "level-by-bucket.csv", index=False)

rows2 = []
for (corpus, book, b), g in m.groupby(["corpus", "book", "bucket"]):
    rows2.append({"corpus": corpus, "book": book, "bucket": "8+" if b == 8 else str(b),
                  "n_verses": len(g), "real_mean": g["distance_from_1"].mean(),
                  "shuffle_mean": g["shuffle_dist"].mean(),
                  "delta_shuffle": g["shuffle_dist"].mean() - g["distance_from_1"].mean()})
bybook = pd.DataFrame(rows2)
bybook.to_csv(OUT / "level-by-book.csv", index=False)

verdicts = []
for corpus, g in level.groupby("corpus"):
    buckets_pass = int((g["delta_shuffle"] > 0).sum())
    bg = bybook[bybook["corpus"] == corpus]
    counted, consistent = 0, 0
    for book, bb in bg.groupby("book"):
        qual = bb[bb["n_verses"] >= 10]
        if len(qual) == 0:
            continue
        counted += 1
        if (qual["delta_shuffle"] > 0).sum() > len(qual) / 2:
            consistent += 1
    frac = consistent / counted if counted else 0.0
    passed = buckets_pass >= 7 and frac >= 2 / 3
    verdicts.append({"corpus": corpus, "buckets_pass": buckets_pass,
                     "books_consistent": f"{frac:.6f}",
                     "verdict": "PASS" if passed else "FAIL",
                     "_flip": buckets_pass < 5})
V = pd.DataFrame(verdicts)
V[["corpus", "buckets_pass", "books_consistent", "verdict"]].to_csv(OUT / "verdicts.csv", index=False)

cp = {r["corpus"]: r["verdict"] == "PASS" for _, r in V.iterrows()}
flip = bool(V["_flip"].any())
form_split = cp["quran-simple"] != cp["quran-uthmani"]
quran_pass = cp["quran-simple"] and cp["quran-uthmani"]
traditions_pass = int(cp["tanakh"]) + int(cp["nt"]) + int(quran_pass)
if flip:
    overall = "FAIL"
elif form_split:
    overall = "FORM-DEPENDENT"
elif traditions_pass >= 2:
    overall = "PASS"
elif traditions_pass == 1:
    overall = "DIALECT"
else:
    overall = "FAIL"

lines = ["# Test 001b — Level at Fixed Axis Count: RESULTS (numbers only)", "",
         "| corpus | buckets_pass | books_consistent | verdict |",
         "|---|---|---|---|"]
for _, r in V.iterrows():
    lines.append(f"| {r['corpus']} | {r['buckets_pass']}/9 | {r['books_consistent']} | {r['verdict']} |")
lines += ["", f"OVERALL: {overall}", ""]
with open(OUT / "RESULTS.md", "w") as f:
    f.write("\n".join(lines))
print(V[["corpus", "buckets_pass", "books_consistent", "verdict"]].to_string(index=False))
print("OVERALL:", overall)
print("filed:", OUT)
