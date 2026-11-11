# STRUKTUR EDIT TETAP (dari Muhaimin — guna untuk SETIAP video, jangan tanya lagi)

> Strategi (funnel, audiens, hook, CTA) ada dalam `funnels.md` — itu didahulukan. Fail ni = peraturan teknikal edit.

Format: TikTok / Instagram Reels / YouTube Shorts — **9:16 menegak, 1080x1920, 30 fps**.
(User tulis "16:9, 1080x1920" — 1080x1920 ialah 9:16 menegak. Guna 9:16 kecuali user minta lain.)

## 1. TRANSCRIBE DULU
Transcribe dulu sebelum apa-apa, supaya tahu mana nak letak animation, motion graphics dan SFX.
- ElevenLabs Scribe (video-use `helpers/transcribe.py`) kalau key ada — paling tepat, tanda filler/pause.
- Kalau takde key: Whisper `medium` (scripts/transcribe.py), language "ms".
- Baca transcript penuh; tandakan: hook candidates, nombor/fakta, nama brand, perbandingan, CTA.

## 2. ANIMATION
- Letak animation + motion graphics kat tempat yang PATUT je (fakta, nombor, perbandingan, proses, nama) — bukan setiap ayat.
- **JANGAN block muka.** Sebelum letak apa-apa, cari kotak muka (snapshot) pada setiap beat; grafik di atas kepala, di sisi bertentangan, atau full-screen cutaway (muka tak nampak langsung). Snapshot setiap beat dan semak.

## 3. SOUND EFFECT PREMIUM
- Satu SFX untuk satu aksi visual (whoosh pada cut/cutaway, pop pada teks/badge, impact pada angka besar, riser sebelum payoff — sekali je).
- Gilir 2–3 variasi; jangan whoosh sama setiap kali. Layer (whoosh + sub impact) untuk momen besar.
- Puncak SFX jatuh 1 frame selepas visual (`npx hyperframes audio <file> --json`). SFX 3–6 dB atas muzik, tak tenggelamkan suara.
- Sumber: HeyGen catalog (kalau signed in) → Openverse CC0 → bundled `media-use/audio/assets/sfx`.

## 3B. SOUND DESIGN JALAN CERITA (ditetapkan user, 2026-11-11) — WAJIB setiap video
SFX bukan hiasan transisi je — SFX **hidupkan cerita** supaya audiens tak bosan dan "nampak" apa yang diceritakan.
- **Dengar transcript, bukan tengok grafik:** setiap ayat yang sebut benda/tempat/aksi yang ada bunyi → letak bunyinya.
  Contoh: "pintu" → pintu berkeriut; "malam" → cengkerik/burung hantu; "air/mandi" → air mengalir/titis; "ular" → desis;
  "lari/jalan" → tapak kaki; "takut/berdebar" → degupan jantung; "hujan/angin" → hujan/angin; "LRT/motor" → bunyi kenderaan; "duit syiling" → syiling jatuh.
- **3 lapisan bunyi:**
  1. **Ambience** (latar tempat, panjang, perlahan ~0.15–0.3): bilik malam, kampung, bandar, surau, hujan — tukar bila cerita tukar tempat/masa.
  2. **Bunyi cerita** (spot, ikut perkataan): pintu, tapak kaki, air, ular, jantung — puncak 1 frame selepas perkataan disebut.
  3. **Bunyi edit** (whoosh, impact, riser, pop): untuk teks/transisi — sederhana, jangan tenggelamkan lapisan 1–2.
- **Rentak anti-bosan:** sekurang-kurangnya satu "bunyi cerita" atau perubahan ambience setiap 4–6 saat; bunyi besar (impact/jantung/sunyi tiba-tiba) di klimaks; **diam total 0.5–1.5s** sebelum ayat paling seram/pedih supaya ia menghentak.
- **Suara tetap raja:** semua lapisan duck bawah suara; selepas render ukur bahagian bercakap vs voice.m4a (sasaran mix −14 LUFS, suara jelas ≥ 4 dB atas yang lain).
- **Sumber bunyi:** `sfx/google-sound-library.txt` (1,160 bunyi Google Sound Library, **CC BY 4.0** — kredit "Sound effects: Google Sound Library (CC BY 4.0)" dalam caption) → muat turun dengan curl dari URL dalam senarai. Bundled Pixabay (`~/.claude/skills/media-use/audio/assets/sfx`) untuk bunyi edit. Freesound & Wikimedia disekat (403/429) — jangan cuba pintas.
- Tulis **peta bunyi** (masa → perkataan → bunyi → lapisan) dalam DESIGN.md dan masukkan dalam mesej preview.

## 4. SAFE ZONE TikTok + IG Reels (1080x1920)
Gabungan paling selamat untuk dua-dua app:
- Atas: kosong 0–220 px (status bar, tab "Following/For You", IG header).
- Bawah: tiada teks penting bawah 1330 px (caption, username, butang muzik).
- Kanan: tiada teks dalam x > 940 px (rail like/comment/share) dari y 700 ke bawah.
- Kiri: margin 60 px.
- Jadi: **semua teks & elemen penting dalam kotak x 60–940, y 220–1330.** Subtitle duduk ~1150–1300.

## 5. BACKGROUND MUSIC — suara tak tenggelam
- Muzik bed ikut mood video (tukar genre setiap video — lihat design-log.md).
- Suara: loudnorm −14 LUFS. Muzik: base ~0.12–0.15, **duck** ke ~0.05 bila bercakap guna `data-automation` volume lane (ikut word timings), naik balik waktu jeda/cutaway tanpa suara.
- Boleh `carve.mjs` (media-use) supaya muzik dip di band suara.
- Mix akhir −14 LUFS, true peak ≤ −1 dBTP. Ukur selepas render.

## 6. POTONG YANG TAK PENTING
- Buang ayat ulang (ambil take terbaik), false start, filler ("eh, aa, hmm, ok so, sebenarnya kan, jadi"), salam/intro panjang.
- Jump cut setiap pause > 0.3 s (simpan ~0.15 s nafas). Fade audio 12–30 ms setiap cut.
- Buang bahagian pandang bawah / betulkan rambut-topi-tudung / pegang phone.
- Sasaran durasi ikut FUNNEL (funnels.md): Awareness 35–55s, Consider 30–45s, Hardsell 25–35s (max 40), Storytelling TIADA had (boleh >90s). Kalau lebih, buang bahagian paling lemah.
- Funnel 2 & 4: JANGAN potong pause yang disengajakan (1s lepas poin / 1.5s lepas ayat pedih).

## 7. HOOK
- Cari ayat PALING KUAT dalam transcript (soalan mengejut, nombor besar, kontra, janji hasil). Kalau bukan di awal, pindahkan ke depan (cold open) — 0–3 s.
- 0–3 s: punch-in muka + teks hook besar + SFX kuat. Frame pertama = thumbnail: muka + teks, jangan hitam.
- Kalau user bagi HOOK LOCK, guna itu.

## 8. PREVIEW
- JANGAN render dulu. Tunjuk: storyboard contact sheets (snapshot setiap beat) + Studio preview (`preview --background`, report port) + jadual beat (masa / ayat / visual).
- Render hanya bila user cakap "render"/"ok".

## 9. DESIGN — TAK SAMA DENGAN VIDEO SEBELUM
- Baca `design-log.md` dulu. Pilih design BARU: palet warna, gaya subtitle, gaya kad/hook, jenis transition, grade, genre muzik, gaya SFX — sekurang-kurangnya 5 daripada 7 mesti beza daripada video terakhir, dan tiada kombinasi berulang dari mana-mana video lepas.
- Font TAK termasuk dalam kiraan variasi — font ikut Peraturan 10.
- Ikut kreativiti: gaya boleh diambil dari `npx hyperframes catalog` (caption-style, transition), `assets/frame-presets` dalam skill hyperframes, atau cipta sendiri.
- Selepas render, TAMBAH entri baru dalam `design-log.md`.

## 10. FONT (ditetapkan user, 2026-11-07)
- **Font utama setiap video: Nunito + Montserrat** (dua-dua bundled dalam HyperFrames, tak perlu @font-face).
  - Montserrat (800–900): headline, hook, kad, stamp, nombor besar.
  - Nunito (800–900): subtitle dan teks badan/label. Nunito lebih bulat & mesra.
  - Boleh tukar peranan (contoh subtitle Montserrat) — tapi JANGAN guna font lain untuk video biasa.
- **KECUALI video beremosi** (sedih, sebak, kisah susah/perjuangan, rindu, syukur, motivasi mendalam, nostalgia, kisah keluarga):
  - Baca skrip dulu, tentukan emosi utama, pilih font yang sentuh emosi tu. Tulis pilihan + sebab dalam DESIGN.md.
  - Panduan:
    - Sedih / sebak / kehilangan / rindu → serif lembut: **Playfair Display** (italic untuk ayat kunci) atau **EB Garamond**.
    - Kisah peribadi / surat / nostalgia → tulisan tangan: **Caveat** atau **Kalam** (perlu fail font dalam `assets/fonts/` + @font-face).
    - Bangkit / motivasi / perjuangan → tinggi & kuat: **League Gothic** atau **Oswald**.
    - Syukur / tenang / spiritual → **Lora** atau **Cormorant Garamond** (perlu @font-face).
    - Seram / misteri (+ inspirasi) → **Cinzel** 700/900 (serif poster filem seram klasik; emas untuk bahagian inspirasi). Dipakai di SERAM1.
  - Subtitle video beremosi boleh kekal Nunito supaya senang baca; font emosi dipakai pada headline/kad/ayat kunci.
  - Font bukan-bundled: download .woff2 (Google Fonts, lesen OFL) ke `assets/fonts/` dan tulis @font-face dalam setiap fail yang guna (lint `font_family_without_font_face`).
- Mix check: after render, measure the speech part vs voice.m4a; impacts/booms add a lot — keep SFX ~0.3–0.45 under a single voice (SERAM1 first mix was -10.4 LUFS).

## 11. FAIL AKHIR UNTUK PHONE (ditetapkan user, 2026-11-11)
- Fail yang dihantar kepada user: **1080x1920, saiz BAWAH 100 MB** (sasaran ~90 MB). Dikemas kini 2026-11-11: phone user gagal simpan fail 120 MB, fail 88 MB berjaya. Jangan lebih 95 MB.
- Selepas render: `scripts/deliver.sh out/<render>.mp4 out/<name>-final-1080p.mp4` (2-pass, bitrate dikira ikut durasi, loudnorm −14 LUFS). Hantar fail INI sahaja (SendUserFile, display "attach").
- Fail render asal (boleh ratusan MB) disimpan dalam `out/` sahaja; hantar hanya kalau user minta.
