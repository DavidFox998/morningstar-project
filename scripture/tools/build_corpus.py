#!/usr/bin/env python3
"""Build the interchangeable scripture corpus (alphabet <-> numerical value)
for morningstar-project/scripture/.

Sources (raw, hashed in REGISTRY.md, never hand-edited):
  Hebrew  : openscriptures/morphhb wlc/*.xml (OSIS, WLC 4.20)
  Greek   : morphgnt/sblgnt *-morphgnt.txt (SBLGNT)
  Arabic  : AlQuran Cloud v1 quran-simple / quran-uthmani (Tanzil text)

Conventions (frozen v1, see VALUE-TABLES.md in the repo):
  - letters only: vowel points, cantillation, accents, breathings,
    diacritics, dagger alifs and editorial marks are not letters
  - Hebrew final forms at base value in `std`, at gadol value in `gadol`
  - qere margin readings excluded; the written (ketiv) words stand
  - Greek final sigma = 200 in `std`
  - Arabic mapped letters: wasla/hamza alifs -> alif; ؤ -> waw class;
    ئ and ى -> ya class; ة -> ha class; standalone ء -> 1
  - the Quran API delivers the Bismillah prefixed to ayah 1 of every
    surah except 9 (and as ayah 1 of surah 1); streams follow the
    source exactly, unedited

The anchor gate runs BEFORE anything is written. Any miss aborts.
"""
import csv, json, re, sys, unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

SRC = Path.home() / "workspace/gematria-corpus-src"
OUT = Path.home() / "workspace/rh-review/morningstar-project/scripture"
NS = "{http://www.bibletechnologies.net/2003/OSIS/namespace}"

# ---------------- value tables ----------------
HEB_STD = dict(zip("אבגדהוזחטיךכלםמןנסעףפץצקרשת",
                   [1,2,3,4,5,6,7,8,9,10,20,20,30,40,40,50,50,60,70,80,80,90,90,100,200,300,400]))
HEB_GADOL = dict(HEB_STD); HEB_GADOL.update({"ך":500,"ם":600,"ן":700,"ף":800,"ץ":900})
HEB_ORD = {}
for i, ch in enumerate("אבגדהוזחטיכלמנסעפצקרשת", 1): HEB_ORD[ch] = i
for f, b in zip("ךםןףץ", "כמנפצ"): HEB_ORD[f] = HEB_ORD[b]

GRK_STD = dict(zip("αβγδεζηθικλμνξοπρστυφχψω",
                   [1,2,3,4,5,7,8,9,10,20,30,40,50,60,70,80,100,200,300,400,500,600,700,800]))
GRK_STD["ς"] = 200; GRK_STD["ϛ"] = 6; GRK_STD["ϟ"] = 90; GRK_STD["ϡ"] = 900
GRK_ORD = {ch: i for i, ch in enumerate("αβγδεζηθικλμνξοπρστυφχψω", 1)}
GRK_ORD["ς"] = GRK_ORD["σ"]

ABJAD_ORDER = "ابجدهوزحطيكلمنسعفصقرشتثخذضظغ"
ABJAD_STD = dict(zip(ABJAD_ORDER, [1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,500,600,700,800,900,1000]))
ABJAD_ORD = {ch: i for i, ch in enumerate(ABJAD_ORDER, 1)}
AR_MAP = {"ٱ":"ا","آ":"ا","أ":"ا","إ":"ا","ٲ":"ا","ٳ":"ا","ء":"ا",
          "ؤ":"و","ئ":"ي","ى":"ي","ة":"ه","ؤ":"و","ئ":"ي"}
AR_MARKS = re.compile(r"[ً-ٰٟٖ-ۭـ﻿]")

def strip_greek_accents(w):
    return "".join(c for c in unicodedata.normalize("NFD", w)
                   if unicodedata.category(c) != "Mn")

# ---------------- Hebrew ----------------
TANAKH_ORDER = [("Gen","Genesis"),("Exod","Exodus"),("Lev","Leviticus"),
    ("Num","Numbers"),("Deut","Deuteronomy"),("Josh","Joshua"),
    ("Judg","Judges"),("1Sam","1 Samuel"),("2Sam","2 Samuel"),
    ("1Kgs","1 Kings"),("2Kgs","2 Kings"),("Isa","Isaiah"),("Jer","Jeremiah"),
    ("Ezek","Ezekiel"),("Hos","Hosea"),("Joel","Joel"),("Amos","Amos"),
    ("Obad","Obadiah"),("Jonah","Jonah"),("Mic","Micah"),("Nah","Nahum"),
    ("Hab","Habakkuk"),("Zeph","Zephaniah"),("Hag","Haggai"),("Zech","Zechariah"),
    ("Mal","Malachi"),("Ps","Psalms"),("Prov","Proverbs"),("Job","Job"),
    ("Song","Song of Songs"),("Ruth","Ruth"),("Lam","Lamentations"),
    ("Eccl","Ecclesiastes"),("Esth","Esther"),("Dan","Daniel"),("Ezra","Ezra"),
    ("Neh","Nehemiah"),("1Chr","1 Chronicles"),("2Chr","2 Chronicles")]

def hebrew_book(code):
    tree = ET.parse(SRC / "morphhb/wlc" / f"{code}.xml")
    verses = []  # (chapter, verse, [word letter-strings])
    for verse in tree.getroot().iter(f"{NS}verse"):
        oid = verse.get("osisID")  # e.g. Gen.1.1
        parts = oid.split(".")
        ch, vs = int(parts[-2]), int(parts[-1])
        words = []
        def walk(el, in_note):
            for child in el:
                tag = child.tag.replace(NS, "")
                if tag == "w" and not in_note:
                    txt = "".join(child.itertext())
                    letters = "".join(c for c in txt if c in HEB_STD)
                    if letters: words.append(letters)
                else:
                    walk(child, in_note or tag == "note")
        walk(verse, False)
        verses.append((ch, vs, words))
    return verses

# ---------------- Greek ----------------
def greek_book(path):
    verses = {}
    order = []
    for line in path.read_text(encoding="utf-8").splitlines():
        f = line.split()
        if len(f) < 5: continue
        pos, word_print, word_norm = f[0], f[3], f[4]
        ch, vs = int(pos[2:4]), int(pos[4:6])
        plain = "".join(c for c in strip_greek_accents(word_norm).lower()
                        if c in GRK_STD)
        key = (ch, vs)
        if key not in verses: verses[key] = []; order.append(key)
        verses[key].append((word_print, plain))
    return [(ch, vs, verses[(ch, vs)]) for ch, vs in order]

# ---------------- Arabic ----------------
def arabic_letters(text):
    text = AR_MARKS.sub("", text)
    out = []
    for c in text:
        c = AR_MAP.get(c, c)
        if c in ABJAD_STD: out.append(c)
    return "".join(out)

def arabic_edition(fname):
    data = json.loads((SRC / fname).read_text(encoding="utf-8"))["data"]
    surahs = []
    for s in data["surahs"]:
        verses = []
        for a in s["ayahs"]:
            words = []
            for w in a["text"].split():
                letters = arabic_letters(w)
                if letters: words.append(letters)
            verses.append((a["numberInSurah"], words, a["text"].replace("﻿", "").strip()))
        surahs.append((s["number"], s["englishName"], verses))
    return surahs

# ---------------- rendering ----------------
def render_book(outdir, fname, title, source_line, verses_norm, table_std,
                table_ord, table_alt=None, alt_name=None):
    """verses_norm: list of (ref_label, native_line, [letter-words])"""
    outdir.mkdir(parents=True, exist_ok=True)
    n_words = n_letters = total = 0
    tsv_rows, txt_blocks = [], []
    for ref, native, words in verses_norm:
        std_stream, ord_stream, alt_stream = [], [], []
        for w in words:
            std_stream.append(" ".join(str(table_std[c]) for c in w))
            ord_stream.append(" ".join(str(table_ord[c]) for c in w))
            if table_alt: alt_stream.append(" ".join(str(table_alt[c]) for c in w))
        flat = [table_std[c] for w in words for c in w]
        n_words += len(words); n_letters += len(flat); total += sum(flat)
        num_line = " · ".join(std_stream)
        txt_blocks.append(f"## {ref}\n{native}\n{num_line}\n")
        row = [ref, " ".join(words), str(len(flat)), str(sum(flat)),
               " ".join(std_stream), " ".join(ord_stream)]
        if table_alt: row.append(" ".join(alt_stream))
        tsv_rows.append("\t".join(row))
    header = (f"# {title}\nSource: {source_line}\n"
              f"Verses: {len(verses_norm)}  Words: {n_words}  Letters: {n_letters}  "
              f"Standard total: {total}\n"
              f"Format per verse: heading, native line, number line "
              f"(standard values, word groups separated by ·).\n"
              f"The machine file {fname}.tsv carries per-verse letter strings, "
              f"standard and ordinal streams"
              + (f" and the {alt_name} stream" if table_alt else "") + ".\n\n")
    (outdir / f"{fname}.txt").write_text(header + "\n".join(txt_blocks), encoding="utf-8")
    cols = "ref\tletters\tletter_count\tstd_total\tstd_stream\tord_stream"
    if table_alt: cols += f"\t{alt_name}_stream"
    (outdir / f"{fname}.tsv").write_text(cols + "\n" + "\n".join(tsv_rows) + "\n", encoding="utf-8")
    return dict(verses=len(verses_norm), words=n_words, letters=n_letters, total=total)

# ---------------- anchors ----------------
def check(name, got, want):
    if got != want:
        print(f"ANCHOR FAIL: {name}: got {got}, want {want}"); sys.exit(1)
    print(f"anchor ok: {name} = {got}")

def main():
    # Hebrew anchors first (build Gen + Ps in memory)
    gen = hebrew_book("Gen")
    g11 = [w for ch, vs, w in gen if (ch, vs) == (1, 1)][0]
    flat = [HEB_STD[c] for w in g11 for c in w]
    check("Gen 1:1 letters", len(flat), 28)
    check("Gen 1:1 total", sum(flat), 2701)
    ps = hebrew_book("Ps")
    ps119 = [v for v in ps if v[0] == 119]
    # Ketiv-only count is 4461. The 2026-11-26 hand-built stream's 4477
    # included the three qere margin words (16 letters) inline, against
    # its own header — see CORRECTION note in gematria-streams.
    check("Ps 119 letters (ketiv only)", sum(len(w) for _, _, ws in ps119 for w in ws), 4461)
    p119v1 = [w for ch, vs, w in ps119 if vs == 1][0]
    check("Ps 119:1 total", sum(HEB_STD[c] for w in p119v1 for c in w), 2379)

    # Greek anchor
    gfiles = sorted((SRC / "sblgnt").glob("*-morphgnt.txt"))
    books_gr = {}
    for p in gfiles: books_gr[p.name] = greek_book(p)
    co = [b for n, b in books_gr.items() if n.startswith("67-")][0]
    for (ch, vs, want_letters, want_total) in [(13, 11, 95, 10093), (13, 12, 116, 13908)]:
        words = [pl for _, v, ws in co if v == vs for _, pl in ws]
        # co entries are (ch, vs, [(print, plain)])
        words = [pl for c2, v2, ws in co if (c2, v2) == (ch, vs) for _, pl in ws]
        flat = [GRK_STD[c] for w in words for c in w]
        check(f"1 Cor {ch}:{vs} letters", len(flat), want_letters)
        check(f"1 Cor {ch}:{vs} total", sum(flat), want_total)

    # Arabic anchors (simple form, Fatiha 1:1-1:2 streams from the baseline file)
    simple = arabic_edition("quran-simple.json")
    fatiha = simple[0][2]
    s11 = [c for _, ws, _ in fatiha if _ == 1]  # placeholder replaced below
    v1 = [ws for n, ws, _ in fatiha if n == 1][0]
    v2 = [ws for n, ws, _ in fatiha if n == 2][0]
    st1 = [ABJAD_STD[c] for w in v1 for c in w]
    st2 = [ABJAD_STD[c] for w in v2 for c in w]
    check("Fatiha 1:1 stream", st1, [2,60,40,1,30,30,5,1,30,200,8,40,50,1,30,200,8,10,40])
    check("Fatiha 1:2 stream", st2, [1,30,8,40,4,30,30,5,200,2,1,30,70,1,30,40,10,50])
    uthmani = arabic_edition("quran-uthmani.json")
    print("ALL ANCHORS PASS")

    if "--check" in sys.argv: return

    agg = []
    # Tanakh
    for i, (code, name) in enumerate(TANAKH_ORDER, 1):
        verses = hebrew_book(code) if code not in ("Gen", "Ps") else (gen if code == "Gen" else ps)
        norm = [(f"{name} {ch}:{vs}", " ".join(ws), ws) for ch, vs, ws in verses]
        r = render_book(OUT / "tanakh", f"{i:02d}-{code}", f"{name} (Hebrew, WLC)",
                        "Open Scriptures morphhb, Westminster Leningrad Codex 4.20, "
                        "consonants only, standard values (gadol in TSV)",
                        norm, HEB_STD, HEB_ORD, HEB_GADOL, "gadol")
        agg.append(["tanakh", name, r["verses"], r["words"], r["letters"], r["total"]])
        print("tanakh", name, r)
    # NT
    nt_names = ["Matthew","Mark","Luke","John","Acts","Romans","1 Corinthians",
        "2 Corinthians","Galatians","Ephesians","Philippians","Colossians",
        "1 Thessalonians","2 Thessalonians","1 Timothy","2 Timothy","Titus",
        "Philemon","Hebrews","James","1 Peter","2 Peter","1 John","2 John",
        "3 John","Jude","Revelation"]
    for i, p in enumerate(gfiles, 1):
        name = nt_names[i - 1]
        norm = [(f"{name} {ch}:{vs}", " ".join(pr for pr, _ in ws),
                 [pl for _, pl in ws]) for ch, vs, ws in books_gr[p.name]]
        r = render_book(OUT / "nt", f"{i:02d}-{p.name.split('-')[1]}", f"{name} (Greek, SBLGNT)",
                        "MorphGNT SBLGNT, accents/breathings stripped, final sigma = 200",
                        norm, GRK_STD, GRK_ORD)
        agg.append(["nt", name, r["verses"], r["words"], r["letters"], r["total"]])
        print("nt", name, r)
    # Quran both forms
    for edition, surahs in [("quran-simple", simple), ("quran-uthmani", uthmani)]:
        for num, ename, verses in surahs:
            norm = [(f"{num}:{n}", raw, ws) for n, ws, raw in verses]
            r = render_book(OUT / edition, f"{num:03d}", f"Surah {num} {ename} (Arabic, {edition})",
                            f"AlQuran Cloud {edition} (Tanzil text), abjad values, "
                            "diacritics/dagger alifs are marks not letters",
                            norm, ABJAD_STD, ABJAD_ORD)
            agg.append([edition, f"{num} {ename}", r["verses"], r["words"], r["letters"], r["total"]])
        print(edition, "done")
    (OUT / "aggregates").mkdir(parents=True, exist_ok=True)
    with open(OUT / "aggregates/corpus-totals.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["corpus", "book", "verses", "words", "letters", "std_total"])
        w.writerows(agg)
    print("WROTE", OUT)

if __name__ == "__main__":
    main()
