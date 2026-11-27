#!/usr/bin/env python3
"""Study 002, TEST 001 — Rule B Across Everything. As filed in
tests/STUDY-002-LIST.md. Numbers only; no interpretation is computed here.

Operationalization of the filed criteria (written before the run):
- Statistic per tradition: Spearman rho between axis_count (capped at 8)
  and distance_from_1 over that tradition's verses.
- p: two-sided permutation test on |rho|, 10,000 permutations, seed 42.
- "Beyond all three baselines": |rho_real| must exceed |rho| computed on
  the per-verse shuffle-mean distances and on the per-verse
  surrogate-mean distances (cross-tradition baseline = the other
  traditions' rows in the same table).
- "Direction consistent across books": among books with >= 30 valid
  verses and >= 3 distinct axis counts, >= 2/3 of per-book rhos share
  the tradition rho's sign.
- Per-tradition verdict: PASS if p < 0.01 AND beyond both baselines AND
  book-consistent; else FAIL.
- Overall: UNIVERSAL if Tanakh, NT and Quran all PASS; DIALECT if a
  proper subset PASSes; FAIL if none. Quran is one tradition in two
  scripts: it PASSes only if both forms PASS; one form only is
  recorded as FORM-DEPENDENT.
- Verses with right_sum = 0 (no distance) are excluded; counts printed.
"""
import csv, json
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr

ROOT = Path("tests/study-002")
rng = np.random.default_rng(42)

def load_summary(p):
    d = {}
    with open(p) as fh:
        for r in csv.DictReader(fh):
            d[(r["corpus"], r["book"], r["ref"])] = r
    return d

B = []
with open(ROOT / "tables/table-B-verse.csv") as fh:
    for r in csv.DictReader(fh):
        if r["distance_from_1"] != "":
            B.append(r)
SH = load_summary(ROOT / "baselines/shuffle-200/summary.csv")
SU = load_summary(ROOT / "baselines/surrogate-200/summary.csv")

def perm_p(x, y, rho_obs, n=10000):
    cnt = 0
    for _ in range(n):
        rp = spearmanr(x, rng.permutation(y))[0]
        if abs(rp) >= abs(rho_obs): cnt += 1
    return (cnt + 1) / (n + 1)

def tradition_rows(corpus):
    rows = [r for r in B if r["corpus"] == corpus]
    ax = np.array([min(int(r["axis_count"]), 8) for r in rows], dtype=float)
    real = np.array([float(r["distance_from_1"]) for r in rows])
    sh = np.array([float(SH[(r["corpus"], r["book"], r["ref"])]["dist_mean"]) for r in rows])
    su = np.array([float(SU[(r["corpus"], r["book"], r["ref"])]["dist_mean"]) for r in rows])
    return rows, ax, real, sh, su

def evaluate(corpus):
    rows, ax, real, sh, su = tradition_rows(corpus)
    rho = spearmanr(ax, real)[0]
    p = perm_p(ax, real, rho)
    rho_sh = spearmanr(ax, sh)[0]
    rho_su = spearmanr(ax, su)[0]
    books = {}
    for i, r in enumerate(rows): books.setdefault(r["book"], []).append(i)
    signs, total = 0, 0
    for book, idxs in books.items():
        if len(idxs) >= 30 and len(set(ax[idxs])) >= 3:
            rb = spearmanr(ax[idxs], real[idxs])[0]
            total += 1
            if np.sign(rb) == np.sign(rho): signs += 1
    consistent = total > 0 and signs / total >= 2 / 3
    passed = (p < 0.01) and abs(rho) > abs(rho_sh) and abs(rho) > abs(rho_su) and consistent
    groups = []
    for b in range(9):
        m = ax == b
        if m.sum():
            groups.append([corpus, "8+" if b == 8 else str(b), int(m.sum()),
                           f"{real[m].mean():.6f}", f"{sh[m].mean():.6f}", f"{su[m].mean():.6f}"])
    verdict = {"corpus": corpus, "verses": len(rows), "rho_real": f"{rho:.6f}",
               "p_perm": f"{p:.5f}", "rho_shuffle": f"{rho_sh:.6f}",
               "rho_surrogate": f"{rho_su:.6f}", "books_consistent": f"{signs}/{total}",
               "verdict": "PASS" if passed else "FAIL"}
    return groups, verdict

all_groups, verdicts = [], []
for c in ["tanakh", "nt", "quran-simple", "quran-uthmani"]:
    g, v = evaluate(c)
    all_groups += g; verdicts.append(v)
    print(v)
q_pass = [v["verdict"] == "PASS" for v in verdicts if v["corpus"].startswith("quran")]
t_pass = {v["corpus"]: v["verdict"] == "PASS" for v in verdicts}
trad = {"tanakh": t_pass["tanakh"], "nt": t_pass["nt"], "quran": all(q_pass)}
npass = sum(trad.values())
overall = "UNIVERSAL" if npass == 3 else ("FAIL" if npass == 0 else "DIALECT")
if any(q_pass) and not all(q_pass): overall += " (Quran FORM-DEPENDENT)"
print("OVERALL:", overall)

out = ROOT / "results/test-001-ruleB"
out.mkdir(parents=True, exist_ok=True)
with open(out / "groups.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["corpus", "axis_bucket", "verses", "mean_dist_real", "mean_dist_shuffle", "mean_dist_surrogate"]); w.writerows(all_groups)
with open(out / "verdicts.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(verdicts[0].keys())); w.writeheader(); w.writerows(verdicts)
lines = ["# TEST 001 — Rule B Across Everything: RESULTS (numbers only)", "",
         "Filed criteria: tests/STUDY-002-LIST.md. Method: test-001.py header.", "",
         "| corpus | verses | rho real | p (perm) | rho shuffle | rho surrogate | books consistent | verdict |",
         "|---|---|---|---|---|---|---|---|"]
for v in verdicts:
    lines.append(f"| {v['corpus']} | {v['verses']} | {v['rho_real']} | {v['p_perm']} | {v['rho_shuffle']} | {v['rho_surrogate']} | {v['books_consistent']} | {v['verdict']} |")
lines += ["", f"OVERALL: {overall}", "", "Group means in groups.csv."]
with open(out / "RESULTS.md", "w") as f: f.write("\n".join(lines) + "\n")
print("filed:", out)
