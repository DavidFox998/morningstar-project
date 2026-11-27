# Value tables and conventions — frozen v1 (2026-11-27)

Any change to this file is a new version of the corpus, and every anchor
in README.md must be re-run before the changed table is used.

## Hebrew (standard / gadol / ordinal)

Standard: א1 ב2 ג3 ד4 ה5 ו6 ז7 ח8 ט9 י10 כ20 ל30 מ40 נ50 ס60 ע70 פ80
צ90 ק100 ר200 ש300 ת400. Final forms ךםןףץ at base value (20/40/50/80/90)
in the standard stream; in the gadol stream ך500 ם600 ן700 ף800 ץ900.
Ordinal: position in the 22-letter alphabet, finals = their base letter.
Text: consonants only (points/cantillation are not letters); word = one
morphhb `<w>` element; qere margin readings (inside `<note>`) excluded.

## Greek (isopsephy / ordinal)

α1 β2 γ3 δ4 ε5 ζ7 η8 θ9 ι10 κ20 λ30 μ40 ν50 ξ60 ο70 π80 ρ100 σ200
τ300 υ400 φ500 χ600 ψ700 ω800; final sigma ς = 200. Ordinal: position
in the 24-letter alphabet, ς = σ. Accents and breathings stripped;
elided forms count as written (δι' = δι). Word = one MorphGNT row.

## Arabic (abjad / ordinal)

Abjad order and values: ا1 ب2 ج3 د4 ه5 و6 ز7 ح8 ط9 ي10 ك20 ل30 م40
ن50 س60 ع70 ف80 ص90 ق100 ر200 ش300 ت400 ث500 خ600 ذ700 ض800 ظ900
غ1000. Ordinal: position in that abjad order (1–28).
Marks, not letters: vowel marks, shadda, dagger alif (ٰ), and the
Quranic annotation marks. Mapped letters: ٱ آ أ إ → ا; ء → ا class (1);
ؤ → و class (6); ئ → ي class (10); ى → ي class (10); ة → ه class (5).
The API delivers the Bismillah prefixed to ayah 1 of every surah except
9, and as ayah 1 of surah 1; the streams follow the source exactly.
