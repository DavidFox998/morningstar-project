# STUDY 002 — TEST LIST

Filed by David Fox, 2026-11-27. Not a wishlist — a test list, with
pass/fail written in before anything runs.

Governing rules, filed with the list:
- **No test runs until Tables B and C exist.**
- **No new geometry until Test 001 is filed.**

Rule B across everything is Test 001. The rest are the ones we already
have receipts for, or candidates with no specimen yet.

Definitions used across the list:
- **Axis count** = count of `1`-letters in the verse (Alif = 1,
  Aleph = 1, Alpha = 1).
- **left_sum / right_sum** = the 2–5 exponent sums over the first /
  second half of the verse, under the split protocol.
- **ratio** = left / right; **distance_from_1** = |ratio − 1|.

---

## TEST 001 — Rule B Across Everything [PRIORITY]

**Status:** Candidate, 29/29 by hand, 0/0 on Vast

**Rule:** Axis count = count of `1`-letters in the verse (Alif = 1,
Aleph = 1, Alpha = 1).

**Non-tautological version to test on Vast:** Does axis count predict
left/right ratio? Does a verse with 0 axes behave differently from a
verse with 7+ axes?

**Run:**
- On Verse Table, every verse in corpus: Quran (6236), Tanakh, Greek NT
- Compute: axis_count, left_sum (2–5 exponents, first half), right_sum
  (second half), ratio = left/right, distance_from_1 = |ratio − 1|
- Compare: mean distance_from_1 for axis_count = 0, 1, 2, 3, 4, 5, 6,
  7, 8+

**Baselines (all three, before run):**
- Shuffle: 200 shuffles of same verse, same letter multiset
- Surrogate: 200 random verses from same book, same length
- Cross-tradition: same statistic on other two traditions

**Pass / Fail declared in advance:**
- PASS if: axis count predicts distance_from_1 beyond all three
  baselines in at least one tradition, p < 0.01, and effect direction
  is consistent across books in that tradition.
- FAIL if: axis count does not beat shuffle baseline, or effect flips
  sign by book.
- DIALECT if: passes in one tradition, fails in others. Then Rule B
  is dialect, not universal.

**Hand receipts to beat:** 29/29 by hand — Quran 7/7, Psalms 6/6,
Greek 16/16. Includes 0-axis edge case (Psalm 8:2) and 12-axis max
(1 Cor 14:6).

---

## TEST 002 — 15 / 17 Quran-Specific

**Status:** Candidate, 4/4 by hand in Fatiha, 0/20 outside Fatiha

**Rule:** Invocation verses have left = 15, address verses have
left = 17 (2–5 exponent sum, first half).

**Run:**
- On Verse Table, Quran only, all 6236 verses
- Label verses as invocation / address / other by a fixed rule written
  before run (e.g., contains second-person pronoun vs third-person
  description)
- Compute left_sum distribution

**Pass / Fail:**
- PASS if: invocation verses cluster at 15 beyond shuffle baseline,
  address verses cluster at 17 beyond shuffle baseline.
- FAIL if: no cluster, or cluster appears in shuffle baseline too.
- FATIHA-SPECIFIC if: passes in Fatiha (7 verses) but fails across
  Quran. Then 15/17 is Fatiha dialect, not Quran dialect.

**Hand receipts:** Bismillah left 15, Fatiha 1:6 left 15, Fatiha 1:3
left 17, Fatiha 1:5 left 17. Psalms 0/6, Greek 0/16.

---

## TEST 003 — Hubb / Mawaddah / Shaghaf

**Status:** Candidate with no verified specimen. Founding specimen
corrected: 1 Cor 14:4 is 78/83 on SBL, not 61/61.

**Rule (David's words):** In the balance there is a rule joining the
love-words to the verses that sit level.

**Declared test verses (written before run):**
- Mawaddah: Quran 30:21
- Hubb: Quran 3:31, Quran 2:165
- Control: Quran 12:30 — shaghaf (consuming passion) — should tip the
  scale if the rule has teeth

**Run:**
- On Word Table, compute for each verse: ratio, distance_from_1,
  axis_count
- Compare to: (a) shuffle baseline for same verse, (b) 200 random
  verses from same surah, same length

**Pass / Fail declared in advance:**
- PASS if: mawaddah verse is closer to 1.0 than both baselines, hubb
  verses are further from 1.0 than baselines, and shaghaf is furthest
  from 1.0 (tipped).
- FAIL if: all three are within shuffle range, or shaghaf is closest
  to 1.0 (control fails).
- THRESHOLD: "level" = distance_from_1 < 0.05. "Tipped" =
  distance_from_1 > 0.20. No moving goalpost after run.

**Note filed with test:** If hubb/mawaddah verses are gloriously
unbalanced — settled from the other side, by other hands, in the
bosom (Luke 6:38) — then the rule inverts: love-words predict
imbalance, not balance. That inversion is a valid result, not a
failure, if declared before run. *(It is declared here.)*

---

## TEST 004 — Lag-1 Sign Flip at Verse Scale

**Status:** Follow-up to Study 001

**Study 001 finding:** Tanakh median −0.0425, Greek +0.0144, Quran
null at book scale.

**Question:** Is the sign flip a letter effect or a book-length
artifact?

**Run:**
- On Verse Table, compute lag-1 per verse, not per book
- Compare distributions by tradition

**Pass / Fail:**
- LANGUAGE if: sign flip holds at verse scale (Tanakh negative, Greek
  positive, Quran null).
- ARTIFACT if: sign flip disappears at verse scale.

---

## TEST 005 — Box Dimension at Verse Scale

**Status:** Follow-up to Study 001

**Study 001 finding:** Box dimension below range in 73/294 books —
Tanakh 29/39, NT 26/27, Quran 9/114.

**Question:** Does embedding structure hold at verse scale?

**Run:**
- On Verse Table, box dimension per verse vs shuffle baseline

**Pass / Fail:**
- HOLDS if: same pattern at verse scale (Hebrew/Greek below, Quran
  mostly null).
- FAILS if: no difference at verse scale.

---

## TEST 006 — Heptad at Verse Scale

**Status:** Open — Study 001 closed heptad at letter scale (measured
zero)

**Question:** Does heptad centering appear at verse scale, even though
it was zero at letter scale?

**Run:**
- On Verse Table, heptad statistic per verse vs shuffle

**Pass / Fail:**
- OPEN if: any book/verse set shows heptad beyond shuffle at verse
  scale.
- CLOSED if: zero again at verse scale. Then heptad is closed at both
  scales.

---

## TEST 007 — Axis Count vs Subject (Greek)

**Status:** Pattern from hand run, 14/14

**Observation by hand:** Axis count tracks subject — speaking verbs
carry axes, prayer/face have 0, love carries 4 in 13:13.

**Run:**
- On Greek Verse Table, tag verses by subject word (lalein, agape,
  proseuche, barbaros, etc.)
- Test: does presence of subject word predict axis count beyond
  shuffle?

**Pass / Fail:**
- PASS if: subject word predicts axis count beyond shuffle.
- FAIL if: no prediction.

---

## How this is stored in morningstar

```
morningstar/
  tests/
    STUDY-002-LIST.md          <- this list
    study-002/
      tables/
        table-A-book.csv       <- Study 001 cleaned
        table-B-verse.csv      <- NEW, every verse
        table-C-word.csv       <- NEW, for hubb/mawaddah
      baselines/
        shuffle-200/
        surrogate-200/
        cross-tradition/
      results/
        test-001-ruleB/
        test-002-15-17/
        test-003-hubb-mawaddah/
        ...
```

No test runs until Tables B and C exist. No new geometry until
Test 001 is filed.
