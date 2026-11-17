---
name: hook
description: 5 cadangan hook 0–3 saat untuk video Muhaimin (TikTok/IG/Shorts). Guna bila user taip /hook diikuti topik, skrip, idea, transcript atau link Drive/video.
---

# /hook — 5 hook killer

Input: topik / skrip / idea / transcript / link Drive. Kalau link video: download (`gdown`), transcribe (Whisper, lihat `edit-video/SKILL.md` §2), baru tulis hook.
Kalau ada video yang dah diedit dalam `projects/`, guna transcript dia.
Jawab dalam Bahasa Melayu rojak santai (aku/kau). Jangan tanya soalan — buat andaian paling logik.

Baca dulu: `.claude/skills/edit-video/funnels.md` (audiens B40 KL / dewasa, 4 funnel, formula hook, larangan).

## Output (ikut format ni)
Satu baris: "Aku detect ni funnel X — topik: …"

Lepas tu **5 hook, setiap satu formula BERBEZA**:
1. **Soalan mengejut** — tanya terus sakit/situasi penonton ("Kau pernah…?").
2. **Nombor / fakta** — angka spesifik yang buat berhenti scroll.
3. **Kontra / mitos** — lawan apa orang percaya ("Ramai ingat X, sebenarnya Y").
4. **Cerita peribadi** — ayat pertama cerita yang terus masuk konflik.
5. **Janji hasil / rahsia** — apa penonton dapat kalau tonton habis (tanpa clickbait palsu).

Untuk setiap hook bagi 3 benda:
- **Ayat cakap** (≤ 3 saat, ~8–12 perkataan) — boleh terus rakam.
- **Teks on-screen** 3–5 perkataan (gaya kad serif TQ1, satu perkataan kunci italic emas → tandakan dengan *…*).
- **Visual 0–3 s** — apa nampak di frame pertama (punch-in muka / B-roll / kad nombor) + emosi (rujuk mood map rules.md §15).

Akhir: **⭐ Pilihan aku: Hook #N** + satu ayat kenapa (paling kuat untuk audiens & funnel ni).
Kalau footage dah ada: **semua hook mesti dari ayat sedia ada** dalam transcript (nyatakan saat mula–tamat) — user tak rakam tambah; potongan dipilih akan di-copy ke 0–3 s sebagai cold open.

## Peraturan
- Formula asas funnels.md: Isu Malaysia + Sakit B40 + Rasa ingin tahu. Bahasa orang biasa, analogi Malaysia.
- Tiada "Hai guys / Assalamualaikum semua" — terus masuk.
- Tiada janji kaya cepat, claim tak realistik, ayat menakutkan palsu.
- Topik agama/Quran: hormat, tepat, tiada clickbait yang mengelirukan; sebut ayat/hukum hanya kalau betul.
- Jangan ulang hook yang sama gaya dengan video lepas (semak `design-log.md`).
