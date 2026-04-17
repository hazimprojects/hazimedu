# Panduan Editorial Glosari BM → ZH (Sejarah)

Dokumen ini melengkapi `docs/zh-mode-editorial-guideline.md` dan khusus untuk pengurusan glosari `data/zh-glossary.json`.

## Prinsip utama

1. **Satu istilah BM → satu padanan utama ZH**.
2. **Elak padanan bercampur** dalam satu nilai (contoh tidak digalakkan: `政府/王国`).
3. **Jika istilah BM ada pelbagai konteks**, pecahkan kepada entri frasa yang lebih spesifik.
4. **Nota konteks ringkas dibenarkan** pada bahagian metadata (`_audit`) untuk reviewer.

## Kaedah pemecahan konteks (contoh)

- Jangan gabungkan konteks moden + tradisional dalam satu istilah.
- Contoh pemecahan yang disyorkan:
  - `kerajaan` → `政府` (padanan utama lalai)
  - `kerajaan moden` → `现代政府`
  - `kerajaan tradisional` → `传统王国政体`

## Polisi istilah terlalu umum

Istilah terlalu umum dibenarkan hanya sebagai fallback minima, tetapi mesti:

- ditandakan dalam `_audit.overly_general`, dan
- disertakan cadangan frasa khusus konteks.

Contoh istilah umum yang perlu diberi perhatian: `bahasa`, `politik`, `agama`, `kampung`.

## Aliran semakan (wajib)

1. Jalankan lint:

```bash
python3 scripts/check-zh-glossary.py
```

2. Jika lint gagal, betulkan entri bercampur (`/`) atau istilah terlalu umum.
3. Reviewer bahasa + reviewer sejarah sahkan padanan canonical sebelum merge.
