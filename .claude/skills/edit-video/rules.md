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
- **Rentak anti-bosan:** sekurang-kurangnya satu "bunyi cerita" atau perubahan ambience setiap 4–6 saat; bunyi besar (impact/jantung/sunyi tiba-tiba) di klimaks; muzik/ambience boleh mati 0.3–0.4 s sebelum ayat paling seram (bukan freeze video).
- **Suara tetap raja:** semua lapisan duck bawah suara; selepas render ukur bahagian bercakap vs voice.m4a (sasaran mix −14 LUFS, suara jelas ≥ 4 dB atas yang lain).
- **Sumber bunyi:** `sfx/google-sound-library.txt` (1,160 bunyi Google Sound Library, **CC BY 4.0** — kredit "Sound effects: Google Sound Library (CC BY 4.0)" dalam caption) → muat turun dengan curl dari URL dalam senarai. Bundled Pixabay (`~/.claude/skills/media-use/audio/assets/sfx`) untuk bunyi edit. Freesound & Wikimedia disekat (403/429) — jangan cuba pintas.
- Tulis **peta bunyi** (masa → perkataan → bunyi → lapisan) dalam DESIGN.md dan masukkan dalam mesej preview.

## 3C. SFX SEIRING TRANSITION IKUT EMOSI (user 2026-11-12) — WAJIB
Setiap momen emosi = **transition visual + SFX padan, serentak** (bukan SFX sahaja):
- **Jump scare / seram** (benda mengejut, "mayat", bunyi pelik): flash putih/merah 2–3 frame + camera shake/punch-in pantas + glitch/RGB split ringkas
  ↔ SFX hit/stinger seram + sub boom (+ jantung/drone naik sebelum).
- **Terkejut / twist / reveal** ("biar betul?", fakta mengejut): whip/zoom-snap + teks pop besar ↔ whoosh + impact / record-scratch.
- **Poin best / tips / hasil yang audiens dapat** (gembira, lega, harapan): pop/bounce teks, sparkle/glow, cahaya hangat, slide lembut
  ↔ chime / ding / sparkle / pop ceria; muzik naik ke cue lebih cerah.
- **Sedih / berat:** slow push + fade/desaturate ↔ low hit lembut, piano/reverse swell.
- Tulis senarai "momen emosi → transition → SFX" dalam DESIGN.md dan mesej preview. Variasi: jangan ulang pasangan sama berturut-turut.

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

## 6. POTONG YANG TAK PENTING — PADAT DENGAN POIN UTAMA (user 2026-11-12, dikemas kini)
**Prinsip: video tiada had masa, tapi mesti PADAT dengan info.** Kekalkan setiap poin/isi cerita (PB1 v1 terlalu banyak dipotong — user tegur),
tapi buang SEMUA yang buat penyampaian nampak tak profesional atau lambat: scene delay, pause berfikir, ulang perkataan, ayat meleret yang tak tambah info.
Kalau satu ayat cakap benda sama dua kali dengan perkataan lain → simpan versi paling padat. Senaraikan semua potongan isi dalam preview supaya user boleh minta pulangkan. BUANG:
- Filler: "eh, aa, hmm, mmm, eee, ok so, okey (pembuka), so, ha (pembuka), **jadi** (penyambung — user 2026-11-12: 'jadi' = delay word, buang), sebenarnya kan".
  - Whisper biasa SEMBUNYIKAN filler (dia regangkan perkataan sebelah, cth "macam" 2 s). Wajib:
    (a) transcribe dengan prompt disfluency: `transcribe.py audio.wav large-v3 "Emm, eee, hmm, aa... jadi, jadi kita orang, eh, mmm."` → token filler muncul;
    (b) `scripts/fillers.py audio.wav --min 0.25` → bunyi meleret (mmm/eee) yang Whisper tak tulis (runs dalam GAP / perkataan >0.9 s);
    (c) titik potong pada minimum tenaga di sekeliling perkataan.
- Ayat yang diulang 2 kali (simpan sekali sahaja, take terbaik) dan false start / tersasul.
  - Termasuk gagap restart 1–3 perkataan: "untuk. Untuk…", "sebab. Sebab…", "tak ada, tak ada…", "benda benda-benda" → buang salinan pertama.
    JANGAN kira penggandaan (macam-macam, benda-benda, pelik-pelik), ulangan gaya ("atas bawah, atas bawah, atas bawah") dan dialog ("tanya Cikgu, 'Cikgu, …'").
  - Awas: kalau satu salinan dah dibuang sebelum ni, jangan buang salinan yang tinggal (PB1 v3 hampir hilang "surau Jumaat · dekat taman").
- **Pause berfikir → jump cut.** `plan_cuts.py` MAX_GAP = 0.3 s (sumber) — pause lebih panjang dipotong (user 2026-11-12: pause berfikir terlalu lama buat bosan).
- **Tiada scene delay:** jangan guna hold/freeze senyap (nilai ke-4 keep.json) kecuali user minta; jeda dramatik maksimum ~0.4 s.
- Intro "Hai assalamualaikum, hari ni saya nak cerita…" — buang terus, masuk hook.
- Part pandang bawah, betulkan tudung/topi/rambut, pegang phone.
- Part paling lemah — HANYA kalau jelas lemah (meleret tanpa isi). Senaraikan setiap potongan dalam mesej preview supaya user boleh minta pulangkan.
- Bercakap dengan editor ("Claude, …", "cuba zoom") — buang, ikut arahannya.
Cara kerja: mula dengan KESELURUHAN rakaman sebagai "keep", kemudian tolak senarai buang di atas (bukan pilih ayat yang nak simpan).
Selepas cut: pastikan tiada perkataan hilang — banding transcript asal vs cuts.json (mesti tinggal hanya perkataan dalam senarai buang).
**Semakan akhir wajib:** bina audio hasil potongan (atrim+concat dari audio.wav ikut cuts.json) dan transcribe SEMULA → baca: ayat lengkap, tiada filler/ulang tinggal, tiada perkataan isi hilang. Timestamp Whisper tak tepat — jangan percaya diff timestamp sahaja.
Durasi funnel (funnels.md) = panduan susunan & hook sahaja, BUKAN sebab untuk buang isi.
Funnel 2 & 4: jeda dramatik dulu 1–1.5 s — kini MAKSIMUM 0.4 s (user tak suka scene delay).

## 6B. SPEED 1.1–1.2 (user 2026-11-12, DIRESET — 1.3 terlalu laju, JANGAN guna lagi) — WAJIB
- **Maksimum 1.2×, minimum 1.1×.** Ukur kelancaran user (selepas potong filler/pause):
  - Cakap **kurang lancar** / tersekat-sekat / meleret → **1.2×**.
  - Cakap **dah lancar** → **1.1×**.
  - Jangan sekali-kali 1.25/1.3 (PB1 v3 1.3× → user kata terlalu laju).
- Cara: `SPEED=1.1 plan_cuts.py ...` (cuts.json simpan `speed`; build_talk guna setpts + atempo — pic suara kekal). Semua masa nota/SFX ikut cuts.json/timemap.
- Nyatakan speed yang dipilih + sebab dalam mesej preview.

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
- Encode HEVC slow ambil masa (≈10–15 min seminit video bila CPU kosong). Tugasan background tool dibunuh selepas 2 jam: **jangan gabungkan render + deliver dalam satu tugasan** untuk video panjang. Jalankan deliver berasingan dan detached:
  `setsid nohup scripts/deliver.sh in.mp4 out.mp4 > out/deliver.log 2>&1 < /dev/null & disown`, kemudian pantau `out.mp4` dengan until-loop.
- Hantar fail INI sahaja (SendUserFile, display "attach"); render asal kekal dalam `out/`.

## 12. SUBTITLE PROFESIONAL (user 2026-11-12) — WAJIB, ganti semua gaya subtitle lama
User tegur: subtitle lama "kebudak-budakan" — terlalu banyak warna, lompat sana-sini, transition merapu, terlalu laju, crowded sampai orang tak tahu nak tengok muka atau subtitle.
- **Warna: hitam-putih SAHAJA.** Teks putih + bayang/outline hitam lembut (atau sebaliknya). Tiada highlight warna, tiada karaoke warna, tiada pill berwarna.
- **Saiz kecil ("size 10")**: kecil & kemas — ~44–50 px pada kanvas 1080 lebar, weight 700–800, sans bersih (Inter / Montserrat / SF-style).
- **3–5 perkataan satu kali, SATU BARIS sahaja.** Jangan pecah jadi 2 baris. Chunk ikut frasa (berhenti pada koma/noktah), min 3 max 5 perkataan (kecuali ayat memang 1–2 perkataan).
- **Kedudukan: bawah — paras dada/perut.** Bukan atas kepala, bukan di muka. Kalau framing kepala→dada, letak sedikit bawah dada. Kekal di satu kedudukan tetap (tak lompat).
- **Transition: tenang** — fade/rise kecil ≤ 0.12 s, tiada bounce/scale/pop/goyang/huruf menari. Chunk kekal di skrin sepanjang frasa (tak berkelip laju).
- Tiada emoji dalam subtitle.

## 13. GAYA EDIT PROFESIONAL — IKUT REFERENCE (user 2026-11-12) — WAJIB
- Kalau user bagi **REFERENCE video** (cth `BAHAN/REFERENCE.mov`): tiru gaya dia sebiji — susunan poin, jenis grafik, kedudukan, rentak, transition. Reference > design-log variasi (rule 9 hanya untuk elemen yang reference tak tentukan).
- Gaya rujukan yang user suka (REFERENCE PB1-Quran, @andikaputeraa): 
  - **Chip topik** kecil di atas (pill gelap translucent + ikon kecil + label 3–5 perkataan) — tukar ikut bahagian cerita.
  - **Senarai poin bertindan** (pill gelap glass, teks putih kecil) muncul satu-satu bila poin disebut, di sisi/dada — tak tutup muka; ✓/✗ / coretan untuk perbandingan.
  - **Kad angka/fakta**: panel gelap glass, label kecil huruf besar jarak lebar + angka/perkataan besar serif elegan; aksen italic serif emas untuk satu perkataan kunci.
  - **Cutaway kad**: latar video sama di-blur + gelap, kad imej/screenshot di tengah dengan tajuk chip di atas.
  - Teks hantu (ghost text) serif besar jarak lebar di belakang subjek untuk perkataan kunci — sekali-sekala.
  - Palet: gelap translucent + putih + satu aksen (emas/ikut tone video). Tiada warna-warni.
- **Tidak kebudak-budakan:** tiada sticker/emoji besar, tiada teks melompat, animasi ringkas (slide/fade 0.2–0.35 s ease-out), satu elemen baru pada satu masa, ruang kosong cukup. Warna mesti ikut tone/grade video.
- Kesan (SFX ikut emosi §3C, grade, camera punch) dikekalkan — user kata efek dah cantik — tapi versi halus/profesional.

## 14. AYAT AL-QURAN (user 2026-11-12) — WAJIB bila video ada ayat Quran / tajwid
- Teks ayat MESTI **Rasm Uthmani** (mushaf Rasm Uthmani, riwayat Hafs) — ambil dari sumber sahih (API Quran.com `text_uthmani` / Tanzil Uthmani), JANGAN taip sendiri / jangan teks "imla'i" biasa.
- Font: **KFGQPC Uthmanic Script HAFS** (Kompleks Raja Fahd) atau **Amiri Quran** — sokong tanda waqaf & harakat penuh. Render RTL, saiz cukup besar supaya baris tajwid jelas.
- Semak setiap ayat (surah:ayat) dengan sumber + dengan bahan B-roll/gambar yang user sediakan; nyatakan rujukan surah:ayat di bawah ayat.
- Highlight hukum tajwid (cth warna pada huruf ghunnah/mad) hanya kalau tepat — kalau ragu, jangan warnakan.
- Jangan ubah urutan/flow video yang user bagi.
