# Test 001b — Level at Fixed Axis Count
Status: FILED 2026-11-27 — approved by David ("Lets do it", 2026-11-27 14:02 PST) after his three rulings were applied.
Parent: Test 001 (filed @ cfb457e5, verdict: FAIL on slope)
Tables: Table B (43,612 verses, commit e8fdac72)
Baselines: Shuffle + Surrogate, 200 + 200 per verse, seed 42, built @ f66268d7
Vast contract for baselines: 62833394

## Question

Test 001 asked about the slope: does axis count predict distance_from_1 beyond baselines?

This test asks about the level, which groups.csv shows but no filed test has asked about yet:

At fixed axis count, is real distance_from_1 lower than shuffle distance_from_1?

## Definitions — same as Test 001, no changes

Axis count = count of `1`-letters in the verse (Alif = 1, Aleph = 1, Alpha = 1)
2-5 reduction: Factor each term to only 2^a × 5^b. Each letter contributes a + b, rest discarded.
Split: Halves, center letter standing in neither (filed spec, 26 Nov)
Left sum = sum of 2-5 exponents, first half
Right sum = sum of 2-5 exponents, second half
Ratio = left / right
Distance_from_1 = |ratio - 1.0|

## Data — already built, do not rebuild

Table B: tests/study-002/tables/table-B-verse.csv — 43,612 rows
(columns: corpus, book, ref, n_letters, n_words, axis_count, left_sum,
right_sum, ratio, distance_from_1, verse_total, lag1)
Shuffle baseline: tests/study-002/baselines/shuffle-200/summary.csv —
per-verse means over 200 shuffles
(columns: corpus, book, ref, dist_mean, dist_sd, dist_p05, dist_p95,
lag1_mean, lag1_sd; dist_mean is the per-verse mean — no aggregation
pass needed)
Surrogate baseline: tests/study-002/baselines/surrogate-200/summary.csv —
same, plus pool_size
Manifest: tests/study-002/baselines/baselines-manifest.json — sha256 2c4f3108… (shuffle summary), bf11d94b… (surrogate summary)
Full per-draw files (905 MB) are archived with the Study 002 run record; this test reads the summaries only.

## Method

For each corpus (tanakh, nt, quran-simple, quran-uthmani), for each axis bucket (0, 1, 2, 3, 4, 5, 6, 7, 8+):

Compute mean real distance_from_1 for verses in that bucket
Compute mean shuffle distance_from_1 for those same verses (200 shuffles per verse, averaged per verse, then averaged per bucket)
Compute mean surrogate distance_from_1 for those same verses (200 surrogates per verse, averaged per verse, then averaged per bucket)
Compute differences:
delta_shuffle = shuffle_mean - real_mean (positive = real below shuffle)
delta_surrogate = surrogate_mean - real_mean

Per-book consistency (Ruling 1, David 2026-11-27 — the text governs):
For each book, only buckets where that book has ≥10 verses in the bucket count.
A book is consistent if delta_shuffle > 0 in the majority of its qualifying buckets.
A book with no qualifying bucket is not counted.
A corpus meets the consistency criterion if ≥ 2/3 of its counted books are consistent.

No new shuffles. No new surrogates. Read only from baselines already built.

## Hand observations that motivate this test — NOT verdicts

From Talitha's read of groups.csv (clone at ~/workspace/rh-review/morningstar-project, verified):

Tanakh 8+: real 0.1165 vs shuffle 0.1373 (real below)
Quran-simple bucket 2: real 0.2734 vs shuffle 0.3263 (real below)
NT bucket 3: real 0.1391 vs shuffle 0.1553 (real below)
Exception: NT bucket 0 — 13 verses only, real 0.1720 vs shuffle 0.1513 (real above)
Surrogates track real closely in Tanakh buckets 4-8+, sit above real at low Quran buckets (simple bucket 0: real 0.2331, surrogate 0.2848)

These are observations from the table, not a verdict. This test will decide if they hold under the filed criterion.

## Quran forms rule (Ruling 3, David 2026-11-27 — carried from Test 001)

Quran-simple and Quran-uthmani are one tradition in two scripts.
- If both forms pass, Quran passes.
- If both forms fail, Quran fails.
- If they disagree — one passes, one fails — the verdict is FORM-DEPENDENT, not PASS, not DIALECT. Overall cannot be PASS. File as FORM-DEPENDENT with both forms' numbers shown.

DIALECT means: passes in one tradition (Tanakh, NT, or Quran as one), fails in others. Not: passes in one script.
Counts for the overall verdict: traditions = 3 (Tanakh, NT, Quran); corpora = 4 for the bucket tables.

## Pass / Fail — declared in advance

A corpus PASSES if both hold:
- Real < Shuffle (delta_shuffle > 0) in at least 7 of 9 buckets
- Per-book consistency (Ruling 1 definition above): ≥ 2/3 of counted books consistent

Flip clause (Ruling 2, David 2026-11-27 — the text governs):
If any corpus shows real > shuffle in the majority of buckets (buckets_pass < 5), the overall verdict is FAIL — even if other corpora pass.

Overall verdict:
- PASS if 2+ traditions pass AND no corpus flips AND the Quran forms do not split
- DIALECT if exactly 1 tradition passes (and no flip, no form split)
- FORM-DEPENDENT if the Quran forms disagree
- FAIL otherwise, or whenever the flip clause triggers

Thresholds are fixed. No moving goalpost after run. Distance_from_1 is the only metric. No other metric may be substituted.

## Output — numbers only, same as Test 001

Files to write to tests/study-002/results/test-001b-level/:

level-by-bucket.csv — one row per corpus × bucket: corpus, bucket, n_verses, n_books, real_mean, shuffle_mean, surrogate_mean, delta_shuffle, delta_surrogate
level-by-book.csv — one row per corpus × book × bucket: corpus, book, bucket, n_verses, real_mean, shuffle_mean, delta_shuffle
verdicts.csv — one row per corpus: corpus, buckets_pass, books_consistent, verdict (PASS/FAIL)
RESULTS.md — the verdict table and the overall verdict, and nothing else. No interpretation.

## Interpretation — not in this file

If 001b PASSES, then the hand study's 29/29 was measuring the level, not the slope. We were seeing real verses sit lower than their own shuffles at fixed axis count, and we called it "Rule B predicts distance."

If 001b FAILS, then the level effect in groups.csv is also a multiset artifact, and we close it.

Either way, Test 001's FAIL on slope stands. 001b does not overturn it. It asks a different question.

## Approval

Drafted: 2026-11-27
Rulings applied: 2026-11-27 (Ruling 1 per-book per-bucket ≥10; Ruling 2 flip clause; Ruling 3 Quran forms rule — all David's, text governs over code)
Approved by David: [x] — 2026-11-27
Filed commit: the commit that adds this file (see git history for this path)
