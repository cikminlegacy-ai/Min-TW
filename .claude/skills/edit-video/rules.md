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

## 6. POTONG YANG TAK PENTING — HANYA yang dalam senarai ni (ditegaskan semula user, 2026-11-12)
**Prinsip: KEKALKAN semua isi cerita.** Jangan potong ayat/perkataan isi semata-mata nak pendekkan video atau ikut sasaran saat
(PB1 dulu terlalu banyak dipotong — user tegur). Hanya BUANG:
- Filler: "eh, aa, hmm, ok so, okey (pembuka), sebenarnya kan".
- Ayat yang diulang 2 kali (simpan sekali sahaja, take terbaik) dan false start / tersasul.
- **Pause LEBIH 0.5 saat → jump cut.** Pause bawah 0.5 s KEKAL (rentak semula jadi). (`plan_cuts.py` MAX_GAP = 0.5.)
- Intro "Hai assalamualaikum, hari ni saya nak cerita…" — buang terus, masuk hook.
- Part pandang bawah, betulkan tudung/topi/rambut, pegang phone.
- Part paling lemah — HANYA kalau jelas lemah (meleret tanpa isi). Senaraikan setiap potongan dalam mesej preview supaya user boleh minta pulangkan.
- Bercakap dengan editor ("Claude, …", "cuba zoom") — buang, ikut arahannya.
Cara kerja: mula dengan KESELURUHAN rakaman sebagai "keep", kemudian tolak senarai buang di atas (bukan pilih ayat yang nak simpan).
Selepas cut: pastikan tiada perkataan hilang — banding transcript asal vs cuts.json (mesti tinggal hanya perkataan dalam senarai buang).
Durasi funnel (funnels.md) = panduan susunan & hook sahaja, BUKAN sebab untuk buang isi.
Funnel 2 & 4: kekalkan pause sengaja (1 s lepas poin / 1–1.5 s lepas ayat pedih).

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

## 10. FONT — ikut VIBE jalan cerita (ditetapkan semula user, 2026-11-12)
- Setiap video: baca skrip, tentukan vibe/emosi, pilih font yang sesuai dengan vibe tu. Tulis pilihan + sebab dalam DESIGN.md.
- Default untuk video edukasi/neutral/santai: **Nunito + Montserrat** (bundled).
- Panduan vibe → font:
  - Sedih / sebak / kehilangan / rindu → Playfair Display (italic ayat kunci) atau EB Garamond.
  - Kisah peribadi / surat / nostalgia / catatan → Special Elite (mesin taip), Caveat atau Kalam (tulisan tangan).
  - Bangkit / motivasi / perjuangan → League Gothic atau Oswald.
  - Syukur / tenang / spiritual → Lora atau Cormorant Garamond.
  - Seram / misteri → Cinzel (atau Special Elite untuk "catatan" seram).
  - Bisnes / data / tegas → Montserrat 900 / Archivo Black.
- Subtitle mesti senang baca (Nunito / Poppins / Montserrat) walaupun tajuk guna font emosi.
- Font bukan-bundled: download .ttf/.woff2 (Google Fonts, OFL) ke `assets/fonts/` + @font-face dalam setiap fail yang guna.
- Jangan ulang kombinasi font video sebelum (design-log.md) kecuali vibe memang sama.

## 11. FAIL AKHIR UNTUK PHONE (user 2026-11-11, dikemas kini 2026-11-12)
- Fail yang dihantar: **1080x1920, saiz 90–100 MB, kualiti "level kayangan"** (setinggi mungkin dalam saiz tu).
  - Phone user tak boleh simpan fail >100 MB (120 MB gagal, 88 MB berjaya).
  - **HEVC disahkan user 2026-11-12**: fail ujian CONS1 HEVC 92 MB boleh download & main di phone user → HEVC ialah format tetap.
- `scripts/deliver.sh out/<render>.mp4 out/<name>-final-1080p.mp4` — HEVC/H.265 2-pass (x265 slow, aq-mode 3, psy-rd, tag hvc1), sasaran 95 MB,
  semak saiz & encode semula kalau terkeluar 90–100 MB, audio AAC 256k −14 LUFS. HEVC ≈ 40% lebih tajam dari H.264 pada saiz sama.
- Sandaran kalau phone/app tak boleh main HEVC: `deliver.sh <in> <out> 95 h264` (x264 veryslow, tune film).
- Encode HEVC slow ambil masa (≈10–15 min seminit video bila CPU kosong) — jalankan di background selepas render.
- Hantar fail INI sahaja (SendUserFile, display "attach"); render asal kekal dalam `out/`.
