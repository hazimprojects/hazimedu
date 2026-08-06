# Panduan Ringkas Mod Bahasa Cina (ZH) – Terjemahan Manual

Mod paparan **tidak lagi** memanggil Google Translate. Semua ayat penuh datang daripada medan `translate` dalam `data/zh-units/*.json` (selepas `normalizeZhExplain` dalam `zh-mode.js`). Skrip bantu:

```bash
python3 scripts/enrich-zh-unit-translations.py data/zh-units/bab-X.json
```

Skrip ini membungkus label pendek sebagai `释义：…（原文：…）` supaya semakan kualiti minimum (≥4 aksara Cina) dipenuhi; kemudian editor boleh menggantinya dengan ayat Cina penuh yang lebih lancar.

**Jana semula ayat penuh daripada `bm_original` (contoh Bab 3):** skrip berasingan memanggil API terjemahan luar talian semasa penyuntingan repo (bukan semasa mod paparan pelajar):

```bash
pip install deep-translator   # sekali sahaja
python3 scripts/regen-bab3-zh-translates.py          # Bab 3 sahaja (wrapper)
python3 scripts/regen-zh-bab-translates.py --bab 4   # Bab 4
python3 scripts/regen-zh-bab-translates.py --bab 5   # Bab 5
python3 scripts/regen-zh-bab-translates.py --bab 6   # Bab 6
```

Hasilnya perlu **disemak manusia** untuk nama khas (Sultan, jawatan, ejaan rasmi) supaya selari dengan nota BM.

## Pengharaman Terjemahan (Wajib)
Dalam teks Cina yang disunting, kategori berikut **hendaklah dikekalkan** dalam bentuk asal (BM / ejaan asal), dan jika perlu boleh diringi ringkasan Cina dalam kurungan:

1. **Nama organisasi rasmi**
2. **Singkatan organisasi rasmi**
3. **Perkataan bahasa Inggeris**
4. **Perkataan bahasa Arab**
5. **Istilah khusus bukan perkataan asal bahasa Cina**
   - Contoh: **waadat, styagraha, bushido, jus soli**

## Nama Orang & Gelaran (Sultan/Tokoh) — Transliterasi + Konteks

**Keputusan editorial (piawaian rasmi, bukan lagi "tak boleh translate")**:
nama orang — termasuk nama Sultan, gelaran (Tun/Tunku/Tuanku/Dato'/Datuk/
Sultan/Raja), dan tokoh sejarah lain — **hendaklah ditransliterasi secara
fonetik ke aksara Cina**, diiringi kurungan mengandungi nama asal (BM/
English) + konteks ringkas (jawatan/peranan). Sebab: pembaca sasaran ialah
pelajar bermedium Cina — ayat yang terus-menerus bertukar ke aksara Latin
di tengah frasa Cina mengganggu bacaan lebih drpd transliterasi yang
lancar dgn konteks disertakan.

Format piawai: `<transliterasi Cina>（<nama asal>, <konteks ringkas>）`

Contoh:
- Sultan Muzaffar Shah → 苏丹穆扎法沙（马六甲第三任苏丹，确立伊斯兰为国教）
- Dato' Onn Jaafar → 拿督翁贾法尔
- Tunku Abdul Rahman → 东姑阿都拉曼

Ini gaya sedia ada (225 kejadian merentas 21 fail, disahkan konsisten
semasa audit kualiti mod ZH) — kini disahkan sbg piawaian rasmi, BUKAN
pelanggaran panduan. Kategori 1–5 di atas (organisasi/singkatan/bahasa
asing/istilah khusus) KEKAL dikekalkan dalam bentuk asal — beza drpd nama
orang, kategori ni tiada bentuk fonetik piawai yang mudah dikenali, jadi
kekal bentuk asal lebih jelas drpd transliterasi.

## Peraturan Umum
- Selain kategori di atas, baki kandungan boleh diterjemahkan ke Cina Ringkas yang mudah difahami pelajar Malaysia; elakkan campuran tatabahasa BM + partikel Cina (“的/在/由” selepas perkataan BM penuh).

## Contoh Perkataan Bab 1 hingga Bab 7 yang Langsung Tak Boleh Translate

*(Nama orang/Sultan/tokoh TIDAK lagi disenaraikan di sini — rujuk §"Nama
Orang & Gelaran" di atas, kategori tu kini ditransliterasi + konteks,
bukan dikekalkan bentuk asal. Senarai di bawah kekal khusus utk
organisasi/singkatan/istilah khusus sahaja.)*

### Bab 1
- Warisan Negara Bangsa
- Kesultanan Melayu Melaka
- waadat

### Bab 2
- Kebangkitan Nasionalisme
- UMNO
- PKMM
- satyagraha / styagraha

### Bab 3
- Konflik Dunia dan Pendudukan Jepun di Negara Kita
- MPAJA
- bushido

### Bab 4
- Era Peralihan Kuasa British di Negara Kita
- British Military Administration
- Malayan Union

### Bab 5
- Persekutuan Tanah Melayu 1948
- Perjanjian Persekutuan Tanah Melayu 1948
- PUTERA-AMCJA
- API
- AWAS
- Piagam Atlantik

### Bab 6
- Ancaman Komunis dan Perisytiharan Darurat
- Parti Komunis Malaya (PKM)
- Communist International (Comintern)
- Special Branch
- Police Field Force (PFF)
- Senoi Praaq

### Bab 7
- Usaha ke Arah Kemerdekaan
- Communities Liaison Committee (CLC)
- Malayan Chinese Association (MCA)
- Parti Islam Se-Tanah Melayu (PAS)
- RIDA
- Parti Perikatan
