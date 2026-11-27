# Study 002 — Tables

Built 2026-11-27 from the scripture corpus in this repo (`scripture/`
@ cf97a314). These tables are the prerequisite for every test in
`tests/STUDY-002-LIST.md`. **Building a table is not running a test** —
no baselines are computed here and no pass/fail is read off them.

- **table-A-book.csv** — Study 001's book-level receipts, merged
  (294 books × 10 statistics, 200 shuffles each).
- **table-B-verse.csv** — every verse in the corpus (43,612 rows):
  letter and word counts, axis count, the 2–5 exponent split sums,
  ratio, distance_from_1, verse total, per-verse lag-1.
- **table-C-word-\<corpus\>.csv** — every word (599,184 rows across the
  four files): its letters, standard value, and axis count. Filed as
  one file per corpus; the Tanakh file alone is 305,507 words.

## Definitions (as filed)

- **Axis count** = number of `1`-letters in the verse (Alif / Aleph /
  Alpha = 1).
- **2–5 exponent sum**: for a letter value v = 2^a · 5^b · m, the
  letter contributes a + b; the rest of the factorization is
  discarded. David's definition (2026-11-26): "Factor each term to
  only 2^a × 5^b."
- **Split**: first half / second half of the verse's letter stream;
  for an odd letter count the center letter stands in neither half.
- **ratio** = left_sum / right_sum; **distance_from_1** = |ratio − 1|.
  Both are blank when right_sum = 0.

## Verification receipts (checked before this build was accepted)

- The reduction reproduces David's hand numbers exactly: Psalm 19
  (WLC 19:2 = English 19:1), split at the 1: **left 45, right 43**.
  Under the filed halves split the same verse reads 47/40 in Table B —
  both are recorded; the filed list governs the tests.
- Bismillah (1:1): axis count 3, **left_sum 15** (the hand receipt).
- Fatiha axis counts in Table B: 1:5 = 4, 1:6 = 5, 1:7 = 7 — matching
  the audited hand counts.
- Greek: 1 Cor 14:6 axis 12 (the filed max), 1 Cor 13:13 axis 8.
- Row counts: Table B = 23,213 + 7,927 + 6,236 + 6,236 = 43,612
  verses; Table C word counts equal the corpus totals exactly.

## One scope note

Psalm references follow WLC numbering (superscriptions count as
verse 1), so English Psalm 19:1 is WLC 19:2. The hand ledger's
"Psalm 8:2" 0-axis edge case ran on a 21-letter clause; the full
verse (MT 8:3, 47 letters) has axis count **1** in Table B. The table
records the full verse; what the filed Test 001 does with that is
the test's business, declared in the list.
