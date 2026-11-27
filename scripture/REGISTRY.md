# Registry — sources, versions, hashes

Built 2026-11-27 by `tools/build_corpus.py`. Raw sources are held outside
this repository (study workspace) and are never hand-edited; this file is
the receipt that lets anyone fetch the identical inputs and rebuild.

| Corpus | Source | Version / commit | Hash |
|---|---|---|---|
| Tanakh | github.com/openscriptures/morphhb, `wlc/*.xml` (OSIS) | commit db6c5c9b46b8f39346f10915ddb1a70dcd429901 | per-file in source repo |
| New Testament | github.com/morphgnt/sblgnt, `*-morphgnt.txt` | commit aaed91e57c8e4a8dc9a2383e129ca5e75fe6393d | per-file in source repo |
| Quran, simple | api.alquran.cloud/v1/quran/quran-simple (Tanzil) | fetched 2026-11-27 | sha256 84889f681086b9d5a94222fbe4358cef77e15183c10baefda24f8f9ab9449402 |
| Quran, Uthmani | api.alquran.cloud/v1/quran/quran-uthmani (Tanzil) | fetched 2026-11-27 | sha256 0df03e1d6da4fc8138208fec1688f2b416f0dd4ebbd514179f3e5e0fbaf4195f |

Anchor gate at build time (all passed before any file was written):
Genesis 1:1 = 28 letters / 2,701 · Psalm 119:1 = 2,379 · Psalm 119 whole
= 4,461 letters (ketiv-only; corrected 2026-11-27) · 1 Cor 13:11 =
10,093 · 1 Cor 13:12 = 13,908 · Fatiha 1:1 and 1:2 streams exact.

External cross-checks after the build: Tanakh letters 1,197,042 =
independent published Leningrad census; NT words 137,554 = published
SBLGNT word count.
