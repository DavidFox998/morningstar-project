# Scripture — the interchangeable corpus

*Alphabet and number as two views of one text.*

This directory holds the native-language scriptures converted, letter by
letter, into their traditional numerical values — the source layer from
which the Morning Star's geometry and engineering are to be built out.

Housed in `morningstar-project` by David Fox's direction (2026-11-27):
the scripture may migrate to its own repository later; this directory is
self-contained so it can lift out unchanged. What is derived *from* the
scripture — geometry, engineering, technology — belongs to Morningstar
proper and links back here. The blueprint stays with the building until
the building stands on its own.

## Contents

| Directory | Corpus | Books | Verses | Words | Letters |
|---|---|---|---|---|---|
| `tanakh/` | Hebrew Bible (WLC) | 39 | 23,213 | 305,507 | **1,197,042** |
| `nt/` | Greek New Testament (SBLGNT) | 27 | 7,927 | 137,554 | 678,956 |
| `quran-simple/` | Quran, simplified script | 114 surahs | 6,236 | 78,245 | 332,837 |
| `quran-uthmani/` | Quran, Uthmani script | 114 surahs | 6,236 | 77,878 | 313,974 |

External cross-checks: the Tanakh letter count 1,197,042 matches an
independent published census of the Leningrad Codex exactly; the NT word
count 137,554 matches the published SBLGNT count exactly. Quran totals
differ from the classical ~323,671 because counting regimes differ
(script form, and the source API delivering the Bismillah prefixed to
ayah 1 of each surah except 9) — both script forms are kept in parallel,
by David's direction: there is a reason for both of them, numerically,
and the difference between the forms is itself an object of study.

Per book there are two files:

- **`<book>.txt`** — the human interchange view, verse by verse,
  uncondensed: heading, native line, number line (standard values, word
  groups separated by `·`). Nothing condensed, nothing altered.
- **`<book>.tsv`** — the machine view: per verse, the letter string,
  letter count, standard total, and the standard + ordinal (+ gadol for
  Hebrew) value streams. Every view and every test regenerates from
  this layer.

`aggregates/corpus-totals.csv` carries per-book totals. `tools/` holds
the builder. `REGISTRY.md` names every source, its version and its hash.
`VALUE-TABLES.md` freezes the value tables and conventions.

## Method and gates

The texts are **downloaded, not transcribed** — decades of scholarly
machine-readable editions (see REGISTRY). The gematria is **generated,
not downloaded**: fixed traditional value tables applied letter by
letter by our own converter. The converter was trusted only after it
reproduced every anchor already on record, exactly:

- Genesis 1:1 = 28 letters, total 2,701
- Psalm 119:1 = 27 letters, total 2,379
- Psalm 119 (whole, written text only) = 4,461 letters — *corrected
  2026-11-27*: the earlier hand-built stream's 4,477 included the three
  qere margin words inline against its own header; the correction is
  documented in the study records and the margin readings are excluded
  here, as the convention always stated
- 1 Corinthians 13:11 = 95 letters, total 10,093; 13:12 = 116 letters,
  total 13,908
- Al-Fatiha 1:1 and 1:2 letter streams match the verified baselines
  exactly

Conventions (full text in VALUE-TABLES.md): letters only — vowel points,
cantillation, accents, breathings, diacritics and dagger alifs are marks,
not letters; Hebrew final forms at base value (gadol values ride in the
TSV); written (ketiv) words stand, margin (qere) readings excluded;
Greek final sigma = 200.

English is a reading layer only and never a number source: David's
reference translation is the NASB (1995 update), aligned by verse
reference outside this corpus. The NASB text is Lockman Foundation
copyright and is not reproduced here.

## Licensing of the underlying texts

- Westminster Leningrad Codex via Open Scriptures morphhb — CC-BY 4.0.
- SBL Greek New Testament via MorphGNT — SBLGNT text under the SBLGNT
  license (sblgnt.com/license); morphological data CC-BY-SA 3.0.
- Quran text — Tanzil project text as delivered by the AlQuran Cloud
  API; attribution to Tanzil (tanzil.net). The numerical streams are
  generated locally from that text.
