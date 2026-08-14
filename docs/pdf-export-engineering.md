# Eksport PDF & Pratonton PDF — Sejarah & Disiplin Penuh

> Dipecahkan drpd `CLAUDE.md` (2026-08-14) — enjin eksport PDF ialah
> bahagian PALING kompleks & paling byk pepijat sejarah dlm codebase
> ni (~1500 baris drpd 3156 baris asal `CLAUDE.md`). Rujuk fail ni
> SEBELUM ubah apa-apa dlm `_generatePages()`, `_pickPdfSplitY()`,
> `_bodyHtmlNode()`, `_kwHtmlOne()`, atau mana-mana fungsi `_pdf*`/
> `_zym-pdf*` dlm `assets/js/main.js`. Ringkasan AWAS paling kritikal
> kekal dlm `CLAUDE.md` — fail ni ialah rekod penuh punca/fix/
> pengesahan Playwright setiap pepijat.

## Eksport PDF — Susun Atur 2 Lajur (skop Bab 1, Bab 2 & Bab 3)

Pengguna minta gaya "2 lajur" (spt nota Scribd rujukan pelajar — mudah
lipat 2, guna ruang kosong dgn bijak). Skop asal DIHADKAN kpd Bab 1
sahaja, kemudian DILUASKAN ke Bab 2, kemudian Bab 3
(`_pdfIsTwoColumnScope()`, regex `/\/notes\/bab-[123](-\d+)?\.html$/i`
pd `window.location.pathname`) — bab lain kekal 1 lajur asal, TIADA
perubahan langsung drpd semakan skop ni (kod lama berjalan
byte-demi-byte sama bila `twoCol=false`).
**Bila luaskan ke bab baharu, WAJIB turut lengkapkan liputan
`HZ_PDF_OPENMOJI_MAP` 100% konsep bab tu dulu** (rujuk §"enjin
`html2canvas-pro`" di bawah, seksyen "Peta ikon PDF") — 2 keputusan
skop ni (2-lajur & peta ikon) dikemas kini SERENTAK setiap kali bab
baharu dimasukkan, sbb 2-lajur (lebar lajur sempit) & liputan ikon
penuh (elak campuran gaya OpenMoji/Fluent) sama-sama makin genting
bila lebar kandungan menyempit.

**Teknik: komposisi CANVAS 2D SELEPAS capture, BUKAN CSS `column-
count`.** CSS multi-column + html2canvas ialah kombinasi terkenal
tak boleh dipercayai (rujuk sejarah pepijat html2canvas dlm fail ni —
baseline teks, SVG). Pendekatan sebenar: tangkap kontena pd LEBAR
SATU LAJUR sahaja (`PDF_2COL_COL_WIDTH_PX`, ~384px, drpd
`PDF_2COL_COL_WIDTH_MM`=90mm × ketumpatan asal 794px/186mm), biar
kandungan alir jadi lebih TINGGI & SEMPIT secara semula jadi (spt
akhbar), guna SEMULA algoritma smart-split sedia ada (`_pickPdfSplitY`
dll., TAK diubah langsung — cuma `pxPerMm`/`pxPerPage` kini berdasar
lebar lajur, bukan lebar kandungan penuh) utk hasilkan "slices"
(lajur), kemudian GANDINGKAN 2 slice bersebelahan (kiri+kanan) via
`canvas.drawImage()` biasa ke SATU kanvas muka surat penuh —
lukisan 2D biasa PASCA-capture, jadi TIADA risiko keserasian
html2canvas langsung. Garis panduan lipat (putus-putus halus)
dilukis di tengah jurang guna `ctx.setLineDash()`.

Lebar hasil (2×lajur + jurang) sepadan TEPAT `cW×pxPerMm` (186mm)
sbb `PDF_2COL_COL_WIDTH_MM×2 + PDF_2COL_GUTTER_MM === 186` — pilih
angka2 ni bila ubah margin muka surat, jgn asal round.

**AWAS — `white-space:nowrap` pd `.zpkw` WAJIB dlm mod 2 lajur (&
kekal selamat dlm mod 1 lajur).** Bila frasa kata kunci BERBILANG
PERKATAAN (cth. "Alam Melayu") terpaksa pisah PERTENGAHAN frasa
merentas baris pd lebar lajur sempit (~300px), `box-decoration-
break:clone` (utk sokong penyerlah wrap berbilang baris) buat
html2canvas-pro GAGAL — hasilkan blob latar meleret merentasi
SELURUH baki lebar baris & TELAN teks biasa di sekelilingnya (bukan
sekadar offset — teks BENAR-BENAR hilang drpd output). Disahkan
piksel demi piksel: frasa PENDEK/tak wrap tak terjejas, cuma frasa
yg genuinely terbelah pertengahan yg rosak. `white-space:nowrap`
paksa seluruh frasa berpindah SEKALI GUS ke baris seterusnya, elak
senario box-decoration-break yg rapuh ni terus (juga makna
`box-decoration-break` sendiri jadi tak relevan, dibuang). Frasa
terpanjang di korpus Bab 1 (~36 aksara, "kemenangan yang gemilang /
bercahaya") diukur ~257px pd 13px bold Fredoka — muat selesa dlm
lebar lajur ~300-330px; kalau tambah kandungan baharu dgn frasa kata
kunci JAUH lebih panjang, sahkan lebarnya sebelum push (guna teknik
serupa: `span.getBoundingClientRect().width` pd font/saiz sebenar).
Bab 2 (frasa lagi panjang — nama pertubuhan/tokoh, cth. "Majlis
Perundangan Negeri-negeri Selat (Straits Settlements Legislative
Council)" ~296px) disahkan via Playwright pd enjin PDF SEBENAR
(§teknik ujian atas): SIFAR `.zpkw` melangkaui sempadan kad induknya
merentas kesemua 8 subtopik, sbb `white-space:nowrap` (bukan lebar
mutlak) yg jamin keselamatan — frasa panjang cuma berpindah SEKALI
GUS ke baris baharu, tak pernah pisah pertengahan tak kira berapa
panjang.

`pages`/`dims` yg dipulangkan drpd `_generatePages()` KEKAL bentuk
sama (array kanvas muka surat penuh + metadata mm) tak kira mod —
`_pdfPopulateSlides()`/`_savePdf()` (pratonton & muat turun) TIADA
apa-apa diubah, sbb komposisi 2-lajur berlaku SEPENUHNYA di dlm
`_generatePages()` sebelum `cb()` dipanggil.

**Bug "kotak terpotong" — `_pickPdfSplitY()` MESTI tolak SELURUH blok
yg dibelah ke muka surat/lajur seterusnya, bukan cuma cuba tetingkap
carian terhad.** Dilaporkan pengguna (tangkapan skrin `bab-2-2.html`
mod 2 lajur): kad accordion "Bill of Rights" (tajuk + ayat + 2 chip)
terbelah antara lajur kiri (chip pertama sahaja) & lajur kanan (chip
kedua terpisah, tercicir drpd kad induknya). Punca: `_pickPdfSplitY()`
asalnya cuma cari ruang putih SELAMAT dlm tetingkap terhad (36% undur
`pxPerPage` / 26% depan utk sempadan blok) sebelum jatuh balik ke
`bestAnyY` (skor kombo whiteness-tempatan terbaik, DIKIRA dlm
tetingkap 36% undur yg SAMA) — kalau blok (cth. kad accordion dgn
chip-list) lebih tinggi drpd tetingkap tu (biasa berlaku mod 2 lajur:
lebar lajur sempit → lebih byk baris wrap → kad jadi lebih tinggi
berbanding bajet tinggi `pxPerPage` yg sama), `bestAnyY` boleh jatuh
di CELAH ANTARA DUA CHIP dlm `.paper-chip-list` (nampak macam ruang
putih tempatan yg baik) walhal masih di DALAM `blockRanges` blok
induk — pisahan "selamat tempatan" tapi SEBENARNYA membelah kad.

Fix: tambah `_findBisectedBlock()` + peringkat fallback BAHARU dlm
`_pickPdfSplitY()` — kalau titik pisahan unggul (`approxY`) jatuh di
DALAM sebarang `blockRanges` (dibelah), & bahagian ATAS blok tu masih
boleh dicapai (`bisected.top > minY`), TERUS pulangkan `bisected.top`
sbg titik pisah — tolak SELURUH blok ke muka surat/lajur seterusnya
(terima jurang kosong lebih besar di penghujung muka surat semasa,
drpd potong kandungan). **Peringkat ni TIADA had jarak carian** (bukan
dibataskan 36%/26% spt peringkat lain) — sbb keutamaan MUTLAK ialah
elak potong kad, bukan jimat ruang; jarak drpd `approxY` ke atas blok
boleh jadi besar (kad yg SANGAT tinggi berbanding bajet muka surat).
Peringkat ni cuma gagal (jatuh balik ke gelagat lama) dlm kes patologi
sebenar: blok yg bahagian ATAS-nya SENDIRI tak boleh dicapai dlm bajet
muka surat semasa (`bisected.top <= minY`) — blok tu bermula terlalu
dekat dgn pisahan sebelumnya utk dielakkan langsung tanpa reka bentuk
semula pagination sepenuhnya (jarang berlaku).

Fungsi `_pickPdfSplitY()` DIKONGSI mod 1 lajur & 2 lajur (sama spt
disebut atas — "operasi atas budget tinggi generik, tak kisah lebar")
— fix ni jadi pembetulan KESAHIHAN am utk KEDUA-DUA mod, bukan khusus
2-lajur, walau kebarangkalian tercetus lagi tinggi dlm mod 2-lajur
(kad lebih kerap melebihi bajet tinggi drpd lebar lajur sempit).
Disahkan via Playwright (§teknik ujian atas, tambah panggilan balik
sementara `window.__pdfDebugCapture(blockRanges, splitPts)` selepas
`splitPts.push(canvas.height)` — DIBUANG lepas ujian, JANGAN kekal dlm
kod produksi): **SIFAR pembelahan** (`splitPts[i]` jatuh di dalam
mana-mana `blockRanges`) merentas 12 halaman skop 2-lajur (Bab 1–2)
& 8 halaman sampel mod 1-lajur (Bab 3–9), semua dgn pelbagai jumlah
blok (9–29) & pisahan (4–8) — sifar ralat JS, sifar kad terpotong.

**Susulan bug "kotak terpotong" di atas — fix tu SENDIRI cetus bug
LEBIH TERUK: kandungan HILANG TERUS (bukan sekadar ruang kosong
terbuang).** Dilaporkan pengguna (tangkapan skrin `bab-2-3.html` mod
2 lajur): lajur kiri muka surat 1 kosong besar (cuma hero, tiada
"Ringkasan 2.3" pun terlihat walhal patut muat), & item accordion
"Dr. Sun Yat Sen dan Tiga Prinsip Rakyat" **hilang terus drpd PDF**
— tiada langsung pd mana-mana muka surat, bukan cuma tersembunyi.

Punca akar: gelung bina `splitPts` asalnya kira sasaran `ideal` setiap
pisahan sbg **grid MUTLAK tetap** (`ideal = s * pxPerPage`, `s` ialah
nombor pisahan) — bukan RELATIF drpd `splitPts[s-1]` SEBENAR. Bila
peringkat "tolak seluruh blok" (fix di atas) memendekkan slice SEMASA
(sbb blok ditolak ke slice seterusnya), `ideal` utk slice SETERUSNYA
KEKAL pd kedudukan grid tetap yg SAMA — jurang (`ideal - prevY`) jadi
LEBIH BESAR drpd `pxPerPage`, bermakna slice seterusnya "berhutang"
ketinggian utk kejar balik grid asal. Tapi kanvas keluaran SETIAP
slice DITETAPKAN pd `pxPerPage` (`Math.min(srcH, pxPerPage)` dlm
gelung `slices`) — lebihan tinggi tu (bahagian "hutang") SENYAP tak
dilukis pd kanvas MANA-MANA slice (bukan slice semasa, bukan slice
seterusnya — genuinely LENYAP), sbb slice seterusnya mula SEMULA drpd
`splitPts[s]` (kedudukan asal tanpa kira lebihan yg tak sempat
dilukis). Ni bukan cuma isu ruang — KANDUNGAN PELAJAR (fakta sejarah)
hilang senyap drpd PDF muat turun, tiada amaran/ralat console langsung.

Fix: tukar `ideal` kpd **relatif** — `ideal = prevY + pxPerPage`
(`prevY` = `splitPts[splitPts.length-1]` SEBENAR, bukan `s * pxPerPage`
grid tetap). Gelung `for (s=1; s<numPages; s++)` (kiraan TETAP,
`numPages` dianggar awal drpd `Math.ceil(canvas.height/pxPerPage)`)
ditukar ke `while (splitPts[...] < canvas.height - 1)` (bilangan
DINAMIK — anggaran awal `numPages` cuma titik mula, kandungan yg byk
blok besar ditolak PERLUKAN lebih byk slice drpd anggaran, jadi
kiraan tetap tak cukup). `numPages` DIKIRA SEMULA (`splitPts.length -
1`) SELEPAS gelung siap, sbb gelung `slices` bawahnya turut bergantung
pd `numPages` yg tepat. Dgn sasaran relatif, SETIAP slice individu
(tak kira berapa byk "hutang" terkumpul drpd slice sebelumnya) jamin
tak pernah lebih tinggi drpd `pxPerPage` — jadi `Math.min(srcH,
pxPerPage)` di gelung `slices` TAK PERNAH klip apa² lagi (`srcH`
sentiasa `<= pxPerPage`).

Disahkan via Playwright (sambung teknik debug atas — kali ni turut
semak `splitPts[i+1] - splitPts[i] <= pxPerPage` utk SETIAP slice,
bukan cuma semak bisections): **SIFAR slice melebihi bajet ketinggian**
& **SIFAR pembelahan** merentas 27 halaman (12 skop 2-lajur Bab 1–2 +
15 sampel mod 1-lajur Bab 3–9) — termasuk kes asal `bab-2-3.html`
(kini 3 muka surat, dulu 2 — bilangan muka surat BERTAMBAH krn
kandungan yg dulu hilang senyap kini disusun atur betul, bukan
regresi). Semakan visual sahkan "Dr. Sun Yat Sen dan Tiga Prinsip
Rakyat" muncul penuh (tajuk + 2 ayat + 3 chip) pd muka surat 2.

**Susulan LAGI — "tolak seluruh blok" (fix pertama di atas) sendiri
boleh buang TERLALU BANYAK ruang kalau blok tu SEBENARNYA satu kad
"komposit" gergasi** (papan pengenalan + `.paper-accordion` BERSARANG
dlm `cv-unit-body` SAMA, bukan sbg abang-adik berasingan — cth.
"Nasionalisme di India" `bab-2-3.html`, 5 item accordion bersarang
dlm SATU papan ~1985px tinggi, hampir bajet SATU lajur penuh).
Dilaporkan pengguna (tangkapan skrin lanjutan): lajur/muka surat
SEBELUM kad ni jadi hampir KOSONG (cuma tajuk kecil), kad SELURUHNYA
tertolak ke lajur seterusnya — buang byk ruang walau SEBAHAGIAN
kandungan kad tu (cth. 2-3 item accordion pertama) sepatutnya muat
selesa dlm lajur semasa. Pengguna cadang: "buat satu mekanisma utk
pecahkan kad kepada beberapa bahagian".

Punca: `_collectPdfBlockRanges()` hanya lindungi kad SEBAGAI SATU
unit gergasi (elemen `.zp-board` induk) — item `.paper-accordion-item`
BERSARANG dlm badan papan yg SAMA (bukan abang-adik `.zp-section-wrap`
spt corak "Revolusi Amerika" `bab-2-2.html` yg SUDAH berfungsi baik)
TIDAK didaftar sbg blok berasingan, jadi `_pickPdfSplitY()` tiada
pilihan selain tolak SELURUH papan (termasuk bahagian yg patut muat).

Fix (BUKAN ubah algoritma pisahan — ubah PENJANAAN HTML cetak supaya
struktur DOM padan corak yg sudah berfungsi): `_renderBoard()`
(`_buildPrintHtml`) kini kesan bila `cv-unit-body` papan ada anak
LANGSUNG `.paper-accordion`, & "buka" accordion tu KELUAR drpd bekas
papan (bukan bersarang lagi) — jadikan SEBARIS (sibling) spt corak
sedia ada yg berfungsi baik. Kandungan SEBELUM accordion (cth. ayat
pengenalan) kekal dlm papan bekas asal (label/warna strip dikekalkan);
accordion pula dijana via `_renderAccordion()` yg SAMA digunakan
utk accordion abang-adik biasa — SETIAP item accordion jadi
`.zp-acc` blok dilindungi SENDIRI (padan `.zp-board, .zp-flap, .zp-acc,
.zp-tl` di `_collectPdfBlockRanges`), splitter kini BOLEH pisah
ANTARA item accordion (bukan terpaksa tolak KESELURUHAN papan).

**Bug pendua ditemui semasa ujian fix ni (bukan disebabkan fix ni,
SEDIA ADA sebelumnya — rujuk bawah)**: `_renderAccordion()` &
cawangan `.paper-accordion` dlm `_bodyHtmlNode()` (dahulunya
`_bodyHtml`) kedua-duanya guna `el.querySelectorAll('.paper-accordion-item')`
TANPA skop — padan SEMUA keturunan tanpa kira kedalaman, bukan
cuma anak LANGSUNG. Item accordion boleh ada SUB-ACCORDION bersarang
dlm panel sendiri (cth. "Penubuhan gerila Melayu oleh Force 136"
`bab-3-7.html`, 3 sub-item tarikh "Force 136" bersarang dlm satu
item) — `querySelectorAll` tanpa skop padan item bersarang tu JUGA
di peringkat accordion INDUK (sekali via pemprosesan rekursif body
item induk, sekali lagi kerana tersalah padan di situ) — pendua
kandungan dlm PDF (3 item "Force 136" muncul 2 kali). Bug ni WUJUD
SEBELUM fix "buka accordion" di atas (kedua-dua laluan lama & baharu
kongsi selector sama), cuma DITEMUI semasa audit menyeluruh lepas fix
ni (bandingkan senarai tajuk accordion sumber vs cetak, teknik baharu
tak pernah dipakai sblm ni). Fix: tukar KEDUA-DUA `querySelectorAll('.paper-accordion-item')`
kpd `querySelectorAll(':scope > .paper-accordion-item')` (anak LANGSUNG
sahaja) — sub-accordion bersarang tetap diproses BETUL (sekali sahaja)
via panggilan rekursif `_bodyHtml`/`_bodyHtmlNode` semasa memproses
badan item INDUKnya.

Disahkan via Playwright merentas **49 halaman subtopik** (semua bab
1–9): bandingkan senarai PENUH tajuk `.paper-accordion-item` sumber
(tak termasuk `.keyword-legend-wrap`) vs senarai tajuk `.zp-acc`
tercetak — **sifar hilang, sifar pendua, sifar ralat JS** pd
kesemua 49 halaman (3 drpd 49 "kelihatan" tak padan pd ujian pertama
disahkan positif-palsu — `data-cv-title` [ID pendek utk koleksi] vs
teks `.paper-accordion-title` [teks penuh dipaparkan] memang SENGAJA
berbeza pd kad tsb, cth. "Julai 1914" vs "28 Julai 1914" — kiraan
item padan tepat 13=13/20=20/18=18 pd ketiga-tiga, mengesahkan bukan
bug). Kes asal `bab-2-3.html` kini kembali ke 2 muka surat (bukan 3)
— ruang digunakan cekap tanpa hilang/potong kandungan.

**Susulan — tajuk "Bahagian N" (`.zp-section`) boleh tertinggal
YATIM di penghujung muka surat/lajur, kandungannya bermula di muka
surat/lajur SETERUSNYA tanpa tajuk.** Pengguna tunjuk tangkapan skrin
pratonton PDF `bab-3-4.html` mod 2 lajur: badge "BAHAGIAN KEEMPAT" +
tajuk "4️⃣ Bermulanya Perang Dunia Kedua di Asia Pasifik" muncul
BERSENDIRIAN di penghujung lajur kanan (ruang kosong di bawahnya,
tiada kandungan langsung), & kandungan sebenar ("Perang Dunia Kedua
di Asia Pasifik bermula apabila Jepun menyerang...") muncul di muka
surat SETERUSNYA TANPA tajuk berulang. Corak sama utk "BAHAGIAN
KELIMA" / "5️⃣ Garisan Masa..." (tajuk di penghujung lajur kiri,
kandungan timeline bermula di ATAS lajur kanan). Arahan pengguna:
"tajuk jangan dibiarkan terpisah tanpa apa apa kandungan, dan
kandungan tidak patut bermula di muka baru tanpa tajuknya."

Punca: `_collectPdfBlockRanges()` SUDAH ada mekanisme "gam" tajuk
seksyen dgn blok kandungan PERTAMA (`.zp-board`/`.zp-flap`/`.zp-acc`/
`.zp-tl` selepas tajuk dlm `.zp-section-wrap` sama) jadi SATU range
dilindungi — TAPI dihadkan `mergedDocH <= 560` (unit dok, sblm skala).
Bila blok kandungan pertama BESAR (cth. `.zp-tl` garis masa 12 kad,
atau `.zp-board` panjang), gabungan lebih drpd 560 → gam DILANGKAU,
tajuk didaftar sbg range TERASING kecilnya sendiri (~40-60px). Tajuk
kecil ni jarang kena `_findBisectedBlock` (titik pisah "ideal" jarang
jatuh TEPAT di dlm range sekecil tu), tapi JURANG selepas tajuk
(margin, sebelum range kandungan besar yg kini berasingan bermula)
nampak "ruang putih selamat" pd pengesan splitter — splitter gembira
potong situ, punca tajuk yatim.

Fix (`_collectPdfBlockRanges()`): buang had `mergedDocH <= 560` —
SENTIASA gam tajuk dgn blok kandungan pertama jadi SATU range, tak
kira besar mana blok tu. Kalau gabungan (tajuk+blok besar) SENDIRI
tak muat 1 muka surat/lajur, mekanisme SEDIA ADA "tolak SELURUH blok"
(`_findBisectedBlock` dlm `_pickPdfSplitY`, rujuk §"Bug kotak
terpotong" atas) tangani spt biasa: cubaan PERTAMA tolak SELURUH
gabungan ke muka surat/lajur seterusnya (terima jurang kosong lebih
besar drpd tajuk kecil sahaja); kalau MASIH tak muat pd cubaan kedua
(gabungan lebih tinggi drpd SATU muka surat/lajur penuh), fallback
sedia ada buat pisahan PAKSA di DALAM kandungan (bukan pd tajuk, sbb
tajuk kekal kecil & sentiasa di awal range gabungan) — mekanisme SAMA
yg dah disahkan selamat merentas 27+ halaman utk kad komposit besar,
digunakan semula tanpa ubah, cuma daftar range lebih besar drpd
sebelum ni. Tiada logik baharu ditambah.

Disahkan via Playwright: (1) suntik panggilan balik sementara
`window.__pdfDebugCapture(blockRanges, splitPts)` selepas
`splitPts.push(canvas.height)` (SAMA teknik drpd §"Bug kotak
terpotong" atas — DIBUANG lepas ujian, JANGAN kekal dlm kod
produksi), semak SIFAR `splitPts[i]` jatuh di dalam mana-mana
`blockRanges` merentas **65 halaman subtopik** (semua Bab 1–10,
termasuk 20 halaman skop 2-lajur Bab 1–3 & sampel 1-lajur Bab 4–10)
— sifar bisections, sifar ralat JS pd SEMUA halaman; (2) pratonton
visual (`bab-3-4.html`, kes asal pengguna): "BAHAGIAN KEEMPAT" kini
berpindah SEPENUHNYA (badge+tajuk+papan) ke muka surat 3 bersama
kandungannya, muka surat 2 berakhir kemas selepas kad "KEMUNCAK
KETEGANGAN" (tanpa jurang janggal); "BAHAGIAN KELIMA" turut berpindah
bersama KEDUA-DUA kad garis masa (12 kad "Garisan Masa Serangan
Jepun" + kad "Info Penting: Masa Tokyo") ke lajur kanan muka surat 3,
tiada tajuk atau kandungan yatim lagi.

**Diluaskan ke Bab 4** — `_pdfIsTwoColumnScope()` skop kini `bab-[1234]`
(WAJIB liputan `HZ_PDF_OPENMOJI_MAP` 100% konsep unik Bab 4 dulu, +23
konsep baharu drpd 114 unik digunakan, 257 kesemuanya, disahkan tiada
kes edge annotation OpenMoji kali ni). Bab 4 (Malayan Union/Persekutuan)
dedah **DUA** isu baharu tak pernah tercetus di Bab 1-3, kedua-duanya
lebih relevan drpd sekadar liputan ikon:

1. **Gelaran raja/sultan `kw-tokoh` JAUH lebih panjang drpd korpus
   sebelum ni** (cth. "Sultan Hisamuddin Alam Shah ibni Almarhum
   Sultan Alauddin Sulaiman Shah" — diukur ~508px pd 13.5px bold
   Fredoka, drpd frasa terpanjang Bab 1-3 yg cuma ~257-340px), tak
   muat sbg SATU kotak `white-space:nowrap` (WAJIB kekal, rujuk AWAS
   §"Susun Atur 2 Lajur" atas) dlm lebar lajur 2-kolum (~330px).
   **Percubaan 1** (kecilkan font-size ikut nisbah lebar): pengguna
   nyata "tak kemas" (fon jadi terlalu kecil drpd teks sekeliling,
   cth. 7.46px vs 13.5px asal) — DIBUANG. **Percubaan 2** (buang
   nowrap terus, biar wrap saiz sama): disahkan piksel+visual
   HIDUPKAN SEMULA bug LAMA html2canvas-pro yg SEBAB nowrap jadi
   wajib drpd awal — latar `.zpkw` yg wrap >1 baris dilukis SALAH,
   blob melekit merentasi SELURUH baki lebar BARIS PERTAMA (diuji
   box-decoration-break lalai `slice` & `clone` eksplisit, KEDUA-DUA
   tetap rosak, >40% kawasan smear-check tetap warna latar) — DIBUANG.
   **Percubaan 3** (gugur TERUS latar/padding/border-radius, teks
   bold berwarna tanpa kotak): BERFUNGSI (sifar smear), tapi pengguna
   cadang lebih baik — kekalkan latar drpd "kesan pen highlighter"
   (SEGI EMPAT, bukan oval/organik), yg secara semula jadi "terpotong"
   bersih bila teks wrap, sbb kesan highlighter sebenar memang segi
   empat.

   **Percubaan 4** (dibuang): `border-radius:0` (segi empat tulen) +
   `box-decoration-break:clone` (CSS uruskan kotak per-baris) — PUNCA
   SEBENAR blob bug disahkan sbg kombinasi border-radius ORGANIK
   `.zpkw` (`38% 42% 40% 44%/46% 40% 48% 42%`, gaya "sketch" tangan)
   + box-decoration-break merentas >1 baris, BUKAN latar+wrap per se
   — geometri segi empat BERSIH sepenuhnya (0.000 pinkRatio smear-
   check, drpd >40% dgn border-radius organik). TAPI pengguna jelaskan
   lagi: satu kotak highlighter patut muat TINGGI SATU BARIS sahaja,
   bukan gabung/sentuh baris ke-2 tanpa jurang (nampak macam SATU
   blok 2-baris, bukan 2 lakaran highlighter berasingan). Diuji CSS
   line-height ibu bapa besar (`2.6`) + line-height span sendiri kecil
   (`1`) — corak piawai jurang antara baris — BERJAYA dlm pelayar
   BIASA (screenshot native, tanpa html2canvas), TAPI html2canvas-pro
   ABAIKAN line-height span sendiri semasa lukis serpihan `clone`
   (guna tinggi kotak garis PENUH drpd ibu bapa, bukan tinggi teks
   sebenar span) — disahkan kekal SIFAR jurang walau line-height
   diuji sehingga `3.0`. Ni had ENJIN html2canvas-pro (bukan isu CSS),
   penyelesaian CSS semata-mata MUSTAHIL utk kes ni.

   **Fix (kekal)**: pindah drpd CSS box-decoration-break kpd kiraan
   JS terus dlm `_pdfDeboxOverlongKeywords(container)` (dipanggil
   SELEPAS kontena cetak dilekap, hanya dlm mod 2 lajur, skop KHUSUS
   `.zpkw-tokoh`/`.zpkw-tempat` — arahan pengguna eksplisit "khusus
   utk nama orang atau tempat yg sangat panjang sahaja"; kalau lebar
   nowrap melebihi ambang selamat 292px): ukur `el.getClientRects()`
   (SATU rect setiap baris SEBENAR selepas `white-space:normal`
   diaktifkan, drpd susun atur PELAYAR tulen, bukan anggaran) & lukis
   SATU `<span>` highlight BERASINGAN per baris (`position:absolute`,
   warna latar disalin via `getComputedStyle` SEBELUM latar asal `el`
   digugurkan, disisip SEBELUM `el` dlm DOM supaya urutan susun lukis
   CSS2.1 letak highlight di BELAKANG teks — `el` & highlight span
   sama-sama `position:relative` utk masuk kumpulan "positioned",
   urutan DOM tentukan lapisan), bukan bergantung pd box-decoration-
   break/clone CSS langsung — elak SEPENUHNYA had enjin di atas sbb
   setiap kotak cetakan span RATA tunggal, TIADA multi-baris/wrap-
   decoration utk html2canvas-pro salah anggar.

   Tinggi kotak setiap baris DISUSUTKAN drpd tinggi baris PENUH
   `getClientRects()` (dipusatkan menegak dlm baris) — nisbah
   `LINE_SCALE_H` diuji beberapa peringkat: 0.65 (jurang paling
   jelas, TAPI huruf ascender/descender cth. "g/y/p/j" nyaris
   tersentuh sempadan kotak — pengguna minta lebih ruang lebihan,
   "bukan tepat sama saiz dengan ketinggian huruf") → 0.88 (ruang
   selesa sekeliling huruf, TAPI jurang antara baris jadi nipis/nyaris
   hilang) → **0.78 dipilih** (imbangan terbaik: ruang lebihan jelas
   sekeliling ascender/descender, jurang antara baris kekal jelas
   kelihatan). Lebar (padX) kekal `0.3em` drpd padding `.zpkw` asal.

   Disahkan piksel+visual (crop kanvas sebenar, enjin PDF sebenar,
   ujian huruf ascender/descender "Gagap Payung Jujur"): SETIAP baris
   frasa panjang kini dpt lakaran highlighter TERSENDIRI dgn jurang
   jelas antara baris (bukan lagi 1 blok 2-baris bersambung), ruang
   lebihan selesa sekeliling huruf, SIFAR overflow keluar sempadan
   kad SEBENAR (semak vs sempadan LUAR kad — encroach ~3-4px ke dlm
   padding sedia ada kad, TAK PERNAH langgar sempadan kad kelihatan)
   merentas 7 halaman Bab 4, SIFAR regresi pagination/bisection (2
   kes sedia ada bab-4-2/bab-4-4 kekal keputusan SAMA drpd fix
   sebelum ni).

2. **Kad garis masa individu (`.zp-tl-card`) TIADA perlindungan
   berasingan drpd `_collectPdfBlockRanges()`** — hanya `.zp-tl`
   INDUK (KESELURUHAN garis masa) didaftar, bukan setiap kad. Tak jadi
   isu selagi `.zp-tl` induk muat 1 muka surat/lajur, tapi timeline
   "Kronologi Tandatangan Sultan" (bab-4-2.html, 9 negeri) & "Proses
   Penyerahan Sarawak" (bab-4-4.html) CUKUP panjang (2578-2977px)
   utk cetus fallback "tolak SELURUH blok" (`_findBisectedBlock`,
   rujuk §"Bug kotak terpotong" atas) DUA kali — cubaan PERTAMA
   berjaya (tolak SELURUH gabungan tajuk+tl), tapi cubaan KEDUA gagal
   semakan `minY` (blok induk "dah guna", top-nya SUDAH jadi prevY
   semasa) & jatuh ke heuristik whiteness/boundary generik yg TIADA
   pengetahuan sempadan kad individu — **boleh potong TEPAT tengah
   SATU kad** (border+latar terbelah dua muka surat). Disahkan
   pengguna: kad "Rang Undang-Undang Penyerahan" (bab-4-4.html)
   header di muka 2, badan+carta undian di muka 3.

   Fix: daftar setiap `.zp-tl-card` sbg range berasingan (SELALU,
   tak kira dlm/luar `.zp-section-wrap`). `_findBisectedBlock()`
   (pulang match PERTAMA ikut urutan array) DIKEKALKAN tanpa ubah
   utk cubaan pertama (still prefer blok induk gergasi dulu — jangan
   ubah gelagat sedia ada yg dah disahkan selamat 27+ halaman).
   Fungsi BAHARU `_findSmallestBisectedBlock()` (pulang range
   TERKECIL/paling dalam bersarang yg mengandungi titik) dipanggil
   sbg langkah PERANTARAAN baharu dlm `_pickPdfSplitY()` — SELEPAS
   semakan blok induk gagal (`bisected.top <= minY`), SEBELUM jatuh
   ke heuristik whiteness/boundary generik: cari range terkecil (cth.
   SATU `.zp-tl-card`) yg turut dibelah, kalau top-nya masih boleh
   dicapai (`> minY`), tolak IA sahaja (bukan blok induk gergasi
   sekali lagi) ke muka surat/lajur seterusnya. Disahkan: kad "Rang
   Undang-Undang Penyerahan" kini berpindah UTUH (header+badan+carta+
   kesimpulan) ke muka surat baharu, titik pisah bertukar drpd
   tengah-tengah kad (6859, di dalam julat kad [6799,7217]) ke
   SEBELUM kad (6798.875, di luar julat kad sepenuhnya).

   Disahkan via Playwright merentas **65 halaman subtopik** (semua
   Bab 1–10, teknik suntik `window.__pdfDebugCapture` sama drpd
   susulan tajuk yatim atas — DIBUANG lepas ujian): SIFAR bisections
   pd 63/65 halaman; 2 baki (bab-4-2.html, bab-4-4.html) disahkan via
   semakan kedudukan tambahan (bandingkan titik pisah vs SEMUA julat
   `.zp-tl-card` individu) SIFAR memotong kad SEBENAR — bisections yg
   dilaporkan cuma jatuh di dlm range INDUK kasar (`.zp-section-wrap`/
   `.zp-tl` gergasi), tak pernah di dlm kad kecil — corak DITERIMA
   (rujuk falsafah sedia ada "terima jurang kosong lebih besar drpd
   potong kandungan").

3. **Komponen carta bar undian dua pihak (`.paper-split-bar`,
   SATU-SATUNYA kejadian korpus, bab-4-4.html "Keputusan undian: 19
   menyokong / 16 menentang") TIADA cabang PDF langsung** — jatuh ke
   fallback generik `_bodyHtml(node)` yg skip nod teks terus drpd
   `<div class="paper-split-bar-seg">` (bukan `<p>`/`<img>`/kelas
   dikenali), kandungan undian (bilangan & peratus) HILANG SENYAP
   drpd PDF (ditemui semasa siasat isu #2 di atas, bukan berkaitan
   langsung). Fix: cabang baharu `paper-split-bar`/`paper-split-bar-
   labels` dlm `_bodyHtmlNode()`, render bar RATA (`.zp-splitbar-a`
   indigo `#4f46e5`, `.zp-splitbar-b` kelabu `#94a3b8` — BUKAN
   gradien spt versi laman hidup, rujuk sejarah pepijat html2canvas
   §"Eksport PDF" atas) + label peratus di bawah. Mod "Jimat Dakwat"
   turut dpt override (`.zp-splitbar-seg` → kelabu muda, padan corak
   `.zp-chip`/`.zp-step` eco sedia ada).

**Diluaskan ke Bab 5** — `_pdfIsTwoColumnScope()` skop kini `bab-[12345]`
(WAJIB liputan `HZ_PDF_OPENMOJI_MAP` 100% konsep unik Bab 5 dulu, +8
konsep baharu drpd 69 unik digunakan, 265 kesemuanya — 61/69 SUDAH
sedia ada drpd liputan Bab 1-4, tiada kes edge annotation OpenMoji
kali ni, format keycap "Keycap 10" → "keycap: 10" padan corak sedia
ada). Bab 5 (Persekutuan Tanah Melayu) TIADA komponen/isu baharu spt
Bab 4 (tiada `.paper-split-bar`/kelas lain yg belum dikendalikan) —
kad `.paper-kingdom` senarai Ahli Jawatankuasa Kerja bernombor keycap
guna corak sedia ada, semua dikendalikan tanpa kod tambahan.

Frasa `kw-tokoh`/`kw-tempat` terpanjang korpus Bab 5 ("Raja
Kamaralzaman Raja Ngah Mansur", 34 aksara) JAUH drpd ambang selamat
292px `_pdfDeboxOverlongKeywords()` (fungsi tu SUDAH generik merentas
SEMUA bab dlm skop 2-lajur sejak Bab 4, bukan khusus Bab 4 — automatik
terpakai tanpa ubah kod) — disahkan via Playwright (pintas
`window.html2canvas` sebelum capture, semak `.zpkw-tokoh`/`.zpkw-
tempat` melangkaui sempadan kad induk) SIFAR overflow merentas
kesemua 4 subtopik. Disahkan jugak: SIFAR ikon `<img class="zp-emoji">`
gagal jadi `data:` URI (`_pdfInlineImages()`), penjanaan PDF penuh
(bukan sekadar pintas capture) berjaya 2-5 muka surat setiap subtopik,
sifar ralat JS pd kesemua 4 subtopik.

**Diluaskan ke Bab 6** — `_pdfIsTwoColumnScope()` skop kini `bab-[123456]`
(WAJIB liputan `HZ_PDF_OPENMOJI_MAP` 100% konsep unik Bab 6 dulu, +35
konsep baharu drpd 146 unik digunakan, 300 kesemuanya — 111/146 SUDAH
sedia ada drpd liputan Bab 1-5. 1 kes edge annotation OpenMoji: Fluent
"Rescue workers helmet" [jamak, tiada apostrof] → annotation OpenMoji
"rescue worker's helmet" [tunggal, tanda petik lengkung ’ bukan
apostrof lurus '] — baki 34 padan terus title-case → lowercase).

Bab 6 (Ancaman Komunis/Darurat) dedah **DUA** komponen carta statistik
BAHARU (`.paper-bar-list`/`.paper-bar` & `.paper-donut-wrap`/`.paper-
donut`, tak pernah wujud Bab 1-5) **TIADA cabang PDF langsung** — jatuh
ke fallback generik `_bodyHtml(node)` yg skip nod teks TERUS drpd
`<div class="paper-bar-label">`/`<div class="paper-bar-value">`/
`.paper-donut-legend-item` (tiada kelas dikenali, bukan `<p>`/`<img>`),
data statistik (bilangan korban/peratus) HILANG SENYAP drpd PDF — SAMA
kelas bug drpd `.paper-split-bar` Bab 4 (rujuk atas), ditemui semasa
imbasan liputan komponen rutin sblm luaskan skop, bukan laporan
pengguna.

- **`.paper-bar-list`** (carta bar mendatar, perbandingan magnitud —
  cth. "Kesan serangan: Cedera parah 46 orang / Mati 4 orang"
  bab-6-2.html): fix render bar RATA (`.paper-bar-fill` sumber guna
  linear-gradient — BUKAN direplikasi, digantikan indigo rata `#4f46e5`,
  rujuk sejarah pepijat html2canvas §"Eksport PDF" atas) + label kiri +
  nilai kanan, lebar bar drpd `--bar-pct` CSS custom property sumber
  (dibaca via `style.getPropertyValue()`).
- **`.paper-donut-wrap`** (carta donat, pecahan drpd satu keseluruhan
  — cth. "Statistik orang awam yang terbunuh, tercedera dan hilang"
  bab-6-2.html): bentuk BULATAN `.paper-donut` sendiri (CSS
  `conic-gradient`, ditetapkan via custom property `--donut-gradient`)
  SENGAJA TIDAK direplikasi terus dlm PDF (gradien + geometri bulatan
  berisiko tinggi dgn html2canvas-pro, rujuk sejarah pepijat berulang
  §"Eksport PDF" atas) — digantikan **bar proporsional rata** (segmen
  warna SAMA drpd conic-gradient asal, diparse terus drpd nilai
  `--donut-gradient` via regex `/(#[0-9a-fA-F]{3,8})\s+([\d.]+)%\s+
  ([\d.]+)%/`, jadi peratus TEPAT kekal tanpa perlu kira semula drpd
  nilai berformat koma cth. "4,668" yg terdedah kpd ralat parse) +
  legenda teks (swatch rata segi empat kecil, warna diambil drpd
  `.paper-donut-swatch` inline style + label + nilai) di bawah —
  kekalkan SEMUA maklumat (jumlah + pecahan tiap kategori) tanpa
  risiko enjin. **AWAS — `.paper-donut-total` sumber guna `<br/>`
  antara nombor & label** (cth. `4,668<br/>jumlah`) — `textContent`
  terus gugurkan pemisah ni jadi "4,668jumlah" tanpa ruang (ditemui
  semasa ujian Playwright pertama); fix iterate `childNodes`, gantikan
  setiap nod `<br>` dgn ruang eksplisit sebelum gabung teks.

Kedua-dua komponen dpt override mod "Jimat Dakwat" (`.zp-bar-fill`/
`.zp-donut-seg`/`.zp-donut-swatch` → kelabu rata `#a1a1aa`, padan
corak `.zp-splitbar-seg` eco sedia ada — kehilangan keupayaan beza
kategori via warna dlm mod ni DITERIMA, sama gelagat drpd
`.zp-splitbar` yg turut jadi kelabu seragam kedua-dua bahagian dlm
mod eco, nilai teks tetap kekal sbg rujukan tepat).

Disahkan via Playwright: (1) suntik markup `.zp-bar-list`/`.zp-donut-*`
berasingan (bukan laluan `_generatePages()` penuh) terus ke
`html2canvas-pro` sebenar, zum imej 2× — SIFAR smear/blob (bar+segmen
donat kekal geometri segi empat/kapsul bersih, label+nilai kekal
tajam); (2) pintas `_bodyHtmlNode()` semasa capture sebenar
(`bab-6-2.html`) — bandingkan data bar (label/nilai/lebar peratus) &
data donat (jumlah/segmen/legenda) drpd kanvas cetak vs sumber DOM
sebenar, SEMUA 6 bar & 1 set donat (3 kategori) padan TEPAT; (3)
merentas kesemua 4 subtopik (`bab-6-1` s/d `bab-6-4`): sifar ikon
gagal, sifar `.zpkw-tokoh`/`.zpkw-tempat` overflow, sifar ralat JS,
penjanaan PDF penuh berjaya 3-6 muka surat setiap subtopik.

**Diluaskan ke Bab 7** — `_pdfIsTwoColumnScope()` skop kini `bab-[1234567]`
(WAJIB liputan `HZ_PDF_OPENMOJI_MAP` 100% konsep unik Bab 7 dulu, +10
konsep baharu drpd 96 unik digunakan, 310 kesemuanya — 86/96 SUDAH
sedia ada drpd liputan Bab 1-6, tiada kes edge annotation OpenMoji
kali ni).

**Kes disiasat tapi TERNYATA BUKAN bug — `.mini-chip-list`/`.mini-chip`
(`bab-7-4.html`, SATU-SATUNYA kejadian korpus, "sekolah yang
menggunakan bahasa Melayu"/"...bahasa Inggeris").** Imbasan awal kelas
komponen baharu (rutin sama drpd penemuan `.paper-bar-list`/`.paper-
donut-wrap` Bab 6) nampak macam corak sama — TIADA CSS `.mini-chip`/
`.mini-chip-list` langsung (disahkan `getComputedStyle`), TIADA cabang
eksplisit dlm `_bodyHtmlNode()` — cukup utk mencetuskan andaian awal
"akan jatuh ke fallback generik `_bodyHtml`, teks hilang senyap sama
kelas bug drpd `.paper-bar-list`". **Andaian ni SILAP** — fix awal
(cabang baharu render setiap `.mini-chip` sbg `<p class="zp-p">`
berasingan) DITULIS & DIUJI, tapi ujian Playwright (pintas
`html2canvas`, cari teks tepat "sekolah yang menggunakan" dlm HTML
cetak) pulangkan SIFAR — nampak macam mengesahkan andaian awal.
Siasatan lanjut (cari teks STRONG heading terdekat "dua jenis sekolah
rendah" sbg titik rujuk, baca 500 aksara SELEPASNYA) dedah teks
SEBENARNYA ADA, cuma terpisah drpd carian `indexOf` string-tepat sbb
`<span class="zpkw zpkw-istilah">` membelah rentetan "...menggunakan
bahasa Melayu" pd sempadan tag.

**Punca ketepatan (BUKAN bug)**: `.mini-chip-list` di korpus ni
SENTIASA tersarang dlm SATU `.paper-chip` (bukan child terus
`.cv-unit-body`), jadi laluan render SEBENAR ialah `_kwHtml(chipEl)`
(dipanggil drpd cabang standalone `.paper-chip-list`, BUKAN
`_bodyHtmlNode`/`_bodyHtml`) — DUA fungsi rekursi BERBEZA drpd apa
dianggap. `_kwHtml`/`_kwHtmlOne` (laluan SEBENAR) proses NOD TEKS
terus (`nodeType===3 → _escPdfHtml`), BEZA drpd `_bodyHtml` (skip nod
bukan-elemen) — jadi teks kekal walau tiada cabang kelas eksplisit.
Fix awal (cabang `mini-chip-list` dlm `_bodyHtmlNode`) DIBUANG balik
selepas disahkan — kod mati/tak boleh dicapai (laluan sebenar tak
pernah singgah `_bodyHtmlNode` utk elemen ni), mengekalkannya
melanggar disiplin minimalis codebase ni ("jangan tambah kod
spekulatif utk kes tak wujud"). **Pengajaran utk audit komponen akan
datang**: sahkan laluan RENDER SEBENAR (`_kwHtml` vs `_bodyHtmlNode`)
dulu — bukan sekadar "tiada cabang eksplisit + tiada CSS" — sebelum
tulis fix; carian `indexOf` teks-tepat dlm ujian boleh beri
POSITIF-PALSU bila kandungan span kata kunci membelah rentetan carian.

Disahkan via Playwright merentas kesemua 5 subtopik (`bab-7-1` s/d
`bab-7-5`): sifar ikon gagal, sifar `.zpkw-tokoh`/`.zpkw-tempat`
overflow, sifar ralat JS, penjanaan PDF penuh berjaya 3-5 muka surat
setiap subtopik.

**Diluaskan ke Bab 8** — `_pdfIsTwoColumnScope()` skop kini `bab-[12345678]`
(WAJIB liputan `HZ_PDF_OPENMOJI_MAP` 100% konsep unik Bab 8 dulu, +1
konsep baharu drpd 63 unik digunakan, 311 kesemuanya — 62/63 SUDAH
sedia ada drpd liputan Bab 1-7, tiada kes edge annotation OpenMoji
kali ni). Bab 8 TIADA komponen baharu — `.paper-bar-list`/`.paper-
donut-wrap` (bab-8-2.html, bab-8-3.html) guna semula pengendali PDF
sedia ada drpd fix Bab 6 tanpa kod tambahan, disahkan 24 bar + 4 item
legenda donat (bab-8-2.html) & 9 bar (bab-8-3.html) semua dikesan &
dirender betul.

Disahkan via Playwright merentas kesemua 4 subtopik (`bab-8-1` s/d
`bab-8-4`): sifar ikon gagal, sifar `.zpkw-tokoh`/`.zpkw-tempat`
overflow, sifar ralat JS, penjanaan PDF penuh berjaya 2-4 muka surat
setiap subtopik.

**Diluaskan ke Bab 9** — `_pdfIsTwoColumnScope()` skop kini `bab-[1-9]`
(regex `[1-9]` tunggal, bukan senarai `[123456789]` panjang — ELAK
padan `bab-10*` scr tak sengaja: aksara tunggal diikuti `(-\d+)?\.html$`
wajib, "1" dlm "bab-10.html" gagal padan sbb aksara SELEPAS "1" ialah
"0" bukan "-"/".html" terus, disahkan via ujian regex eksplisit
merentas kelima-lima corak laluan sebelum push). WAJIB liputan
`HZ_PDF_OPENMOJI_MAP` 100% konsep unik Bab 9 dulu, +1 konsep baharu
drpd 48 unik digunakan, 312 kesemuanya — 47/48 SUDAH sedia ada drpd
liputan Bab 1-8. 1 kes edge annotation OpenMoji: Fluent "Building"
TIADA annotation "building" langsung dlm OpenMoji (bukan emoji rasmi
berasingan) — dipetakan ke konsep Unicode yg SAMA, "office building"
(U+1F3E2), padan konteks penggunaan sumber (ikon generik institusi/
badan awam, cth. "badan awam", "Dewan Perniagaan Melayu"). **AWAS —
JANGAN keliru dgn amaran §"Ikon Emoji" atas ttg kunci `"building"`
PECAH di CDN** — amaran tu ttg SISTEM BERBEZA (`scripts/emoji_map.py`,
client-side Fluent CDN penjanaan HTML statik), bukan `HZ_PDF_
OPENMOJI_MAP` (self-host OpenMoji khusus PDF) di sini; svg disahkan
wujud & sah (`head -c 200`) sebelum push, bukan sekadar percaya nama.

Bab 9 TIADA komponen baharu — semua corak (chip/accordion/kingdom)
guna pengendali PDF sedia ada tanpa kod tambahan. Disahkan via
Playwright merentas kesemua 4 subtopik (`bab-9-1` s/d `bab-9-4`):
sifar ikon gagal, sifar `.zpkw-tokoh`/`.zpkw-tempat` overflow, sifar
ralat JS, penjanaan PDF penuh berjaya 2-3 muka surat setiap subtopik.

## Eksport PDF — Chip blok PD1/PD2 (`.bloc-chip-*`) pendua & tiada warna

Pengguna lapor (tangkapan skrin pratonton PDF `bab-3-3.html`, kad
"Ringkasan 3.3") ayat "...ialah **Kuasa Paksi** dan **Kuasa
Bersekutu**." diikuti garisan PENDUA ("Kuasa Paksi", "Kuasa
Bersekutu", "Jerman", "Kuasa Bersekutu" berulang) sbg baris polos
TANPA warna — walhal kad "PANDUAN WARNA PIHAK PERANG" sejurus di
bawah menjanjikan warna chip bezakan blok (merah=Paksi/Axis,
biru=Bersekutu/Allies).

Punca: corak HTML `.paper-chip-list > div.paper-chip.paper-chip-
sentence > span.paper-chip.bloc-chip-axis` (chip blok TERSARANG dlm
ayat penuh, rujuk §"Bug Chip Terputus Baris" atas utk struktur sama)
— DUA lapisan SAMA-SAMA padan selector CSS `.paper-chip`. Cabang
`hasSentence` dlm `_bodyHtmlNode()` (mengendalikan `.paper-chip-list`)
guna `node.querySelectorAll('.paper-chip')` (bukan `.paper-chip-
sentence`), padan KEDUA-DUA lapisan — chip blok tersarang tu dicetak
DUA KALI: sekali sbg sebahagian ayat penuh (betul, tapi TANPA warna
sbb `bloc-chip-*` bukan sebahagian sistem 11 kelas `kw-*` kanonik,
`_kwHtmlOne()` tiada pengesanan utk kelas ni), sekali lagi sbg
`<p class="zp-sentence">` BERASINGAN & polos.

**Fix pendua**: `_bodyHtmlNode()` tukar selector kpd
`.paper-chip-sentence` (bukan `.paper-chip` generik) — hanya padan
lapisan LUAR (ayat penuh). Disahkan tiada chip-list SELURUH korpus yg
campur chip ayat + chip bukan-ayat sbg adik-beradik terus (`find_all`
BeautifulSoup merentas `notes/bab-*.html`), jadi selector lebih
spesifik ni selamat digunakan tanpa risiko terlepas chip standalone.

**Fix warna**: `_kwHtmlOne()` tambah pengesanan
`bloc-chip-(central|entente|axis|allies)` (SELEPAS semakan `kw-*`
sedia ada) — bungkus dgn `<span class="zpbloc zpbloc-*">`, guna
`_kwHtml(node, {freeze:true})` (BUKAN `_escPdfHtml(textContent)`
spt kw-* — chip blok BOLEH ada anak `<img>` bendera + teks, cth.
"🇩🇪 Jerman", perlu rekursi kekalkan bendera). CSS `.zpbloc-*`
(`_getPrintCss()`) guna palet SAMA drpd `assets/css/keywords.css`
mod terang: `central`=kelabu, `entente`=hijau, `axis`=merah,
`allies`=biru — warna RATA (bukan gradien, elak risiko
keserasian html2canvas). Mod "Jimat Dakwat" (rujuk §bawah) turut
gugurkan latar `.zpbloc` (kekal teks tebal sahaja), konsisten dgn
keputusan `.zpkw` sedia ada.

Disahkan via Playwright (suntik html2canvas-pro/jspdf, pintas
`window.html2canvas`): `bab-3-3.html` kad "Ringkasan 3.3" kini papar
TEPAT 5 ayat (padan 5 `.paper-chip-sentence` sumber, bukan 5+4
pendua), 40 chip `.zpbloc` warna betul (axis=merah/allies=biru)
tersebar di seluruh halaman, sifar baris polos berulang.

**Susulan — pengguna tunjuk 4 isu SAMBUNGAN (tangkapan skrin
`bab-3-3.html` mod 2 lajur) selepas fix di atas dilancar**: "panduan
warna pihak perang tidak jelas chipnya" (bendera bersendirian tanpa
label/warna), "bendera pada nama negara blok tiada" (sebahagian drpd
isu sama), "chip negara utama tiada warna" (senarai "Negara utama:"
bawah kad Fokus Kuasa Paksi/Bersekutu papar chip kelabu neutral), &
"ada highlight kuasa paksi yang rosak dalam ringkasan" (kotak warna
"Kuasa Paksi" pecah/melimpah bila terpaksa lipat baris). Fix di atas
(dedup + pengesanan warna dlm `_kwHtmlOne()`) TAK CUKUP sbb 3 laluan
render BERASINGAN dlm fail ni tak semua lalu `_kwHtmlOne`:

1. **Kad "Panduan warna pihak perang" (`.bloc-legend-grid`)** — corak
   `.bloc-legend-item > span.bloc-legend-swatch (kosong) + span (label
   polos "Kuasa Paksi — " + chip bloc-chip tersarang)` TIADA cabang
   eksplisit dlm `_bodyHtmlNode()`, jatuh ke fallback generik
   `_bodyHtml(node)` — yg skip SEMUA nod teks terus (label "Kuasa
   Paksi — " HILANG) & tak pernah panggil `_kwHtml`/`_kwHtmlOne`
   (jadi pengesanan warna bloc-chip yg BARU ditambah tak pernah
   tercapai either) — cuma `<img>` bendera bersendirian yg terselamat
   (drpd fix IMG PR lain). Fix: cabang baharu
   `cls.indexOf('bloc-legend-grid')` proses label span (anak KEDUA
   item, lepas swatch) terus via `_kwHtml()` — laluan SAMA yg kesan
   `bloc-chip-*`, hasilkan "Kuasa Paksi — [chip merah 🇩🇪 Jerman]"
   penuh.
2. **Chip berdiri sendiri (bukan dlm ayat, cth. "Negara utama:" bawah
   kad Fokus)** — cabang ELSE `.paper-chip-list` (chip biasa, bukan
   `hasSentence`) sentiasa cetak `<span class="zp-chip">` TETAP, tak
   kira kelas asal `c`. `_kwHtml(c)` proses ANAK `c` (kandungan dalam),
   BUKAN `c` itu sendiri — jadi pengesanan `bloc-chip-*` (yg semak
   `node.className` PADA node yg dihantar terus ke `_kwHtmlOne`) tak
   pernah tercapai utk kes ni (`c` sendiri tak pernah dihantar ke
   `_kwHtmlOne`, cuma anak-anaknya). Fix: semak `c.className` TERUS
   dlm cabang ni sebelum bina wrapper, tambah `zpbloc zpbloc-*` ke
   kelas `<span>` kalau padan.
3. **Tajuk accordion (cth. "1 Kuasa Paksi")** — DUA fungsi
   `_renderAccordion()` BERASINGAN wujud dlm fail ni (satu dlm
   `_buildPrintHtml` utk accordion PERINGKAT ATAS, satu lagi dlm
   `_bodyHtmlNode` utk accordion TERSARANG dlm badan papan — evolusi
   sejarah berasingan, bukan disengajakan pendua). Yg SATU (tersarang)
   guna `_kwHtml(ttl2)` betul; yg SATU LAGI (peringkat atas — DIGUNA
   utk accordion "Kuasa Paksi"/"Kuasa Bersekutu" bab-3-3.html) guna
   `_escPdfHtml(ttl.textContent.trim())` — teks POLOS SEPENUHNYA,
   buang bloc-chip DAN sebarang `kw-*` span tersarang dlm tajuk. Fix:
   tukar fungsi KEDUA kpd `_kwHtml(ttl)` jugak, padan fungsi pertama.
4. **Kotak warna "Kuasa Paksi" pecah bila lipat baris** — `.zpbloc`
   CSS TIADA `white-space:nowrap` (fix asal terlepas ni, walau `.zpkw`
   sedia ada guna nowrap drpd awal). SAMA punca/fix drpd AWAS
   `white-space:nowrap` `.zpkw` §"Susun Atur 2 Lajur" atas — frasa
   berbilang perkataan ("Kuasa Paksi") terpisah pertengahan merentas
   baris pd lebar lajur sempit buat latar melekit/pecah dlm
   html2canvas. Tambah `white-space:nowrap` ke `.zpbloc`.

Disahkan via Playwright merentas 9 halaman (`bab-3-2` s/d `bab-3-8` +
sampel semula `bab-3-3`): legenda "Panduan warna pihak perang" papar
label+chip penuh (bukan bendera kosong), chip "Negara utama" (25
kejadian `bab-3-3.html`) semua warna betul, tajuk accordion "Kuasa
Paksi"/"Kuasa Bersekutu" kini `.zpbloc` berwarna. Baki ketidakpadanan
kiraan chip (`bab-3-4/5/6`, defisit SATU setiap satu) disahkan 100%
dijelaskan oleh pengecualian sedia ada "Soalan Utama" (`.paper-flap-
card`) DIGUGURKAN drpd PDF (§"skop kandungan SENGAJA beza" atas,
bukan bug baharu) — chip "Jepun" dlm jawapan Soalan Utama, bukan
kehilangan tak dijangka.

**Susulan — bendera pd chip blok dlm AYAT PROSA BIASA (bukan
chip-list/legenda) hilang senyap dlm PDF, walau HTML/DOM/pratonton
pelayar semua betul.** Pengguna tunjuk 2 tangkapan skrin (`bab-3-2.html`
"Latar Belakang Perang Dunia", `bab-3-3.html` "Perang Dunia Kedua"):
"bendera tak muncul di sebelah nama negara blok pada teks biasa" —
cth. ayat "Pada awalnya melibatkan **Jerman**, **Austria-Hungary**
dan 🇮🇹 **Itali**." papar highlight kelabu betul utk "Jerman"/
"Austria-Hungary" (span `.zpbloc`) TAPI TIADA bendera, walhal "Itali"
kemudian dlm ayat SAMA (span `.paper-chip` polos, TIADA kelas
`bloc-chip-*`, jadi TAK dibalut `.zpbloc`) papar bendera dgn betul.

Disahkan BUKAN isu penjanaan HTML/DOM (siasatan piksel demi piksel,
Playwright): HTML print tercetak MEMANG ada `<img>` bendera dgn
`data:image/png;base64,...` sah, `getBoundingClientRect()` pulang
saiz bukan-sifar, `getComputedStyle()` semua betul (`display`/
`visibility`/`opacity`), & screenshot DOM SEBENAR (pratonton pelayar
biasa, SEBELUM html2canvas dipanggil — teknik: `pr.style.position=
'relative'` + `transform:translateY()` gantikan scroll, sbb `#zym-pr`
`position:fixed` + modal PDF kunci scroll body) papar bendera PENUH
& JELAS. TAPI sampel piksel kawasan PENUH (bukan satu titik — elak
positif-palsu koordinat) drpd KANVAS SEBENAR yg ditangkap html2canvas
(hook `window.html2canvas`, baca `ctx.getImageData()` pd lokasi
`<img>` diskala `opts.scale`) pulang **SIFAR variasi warna** (100%
`#e2e8f0`, warna latar `.zpbloc-central` sahaja) — bermakna
html2canvas-pro GAGAL SENYAP melukis `<img>` anak, bukan isu
DOM/CSS/data-URI.

**Punca diasingkan via ujian variasi CSS satu-per-satu** (mutate
`#zym-pr-css` tepat sebelum panggilan `html2canvas` sebenar, ukur
variasi piksel selepas): `border-radius`, `white-space:nowrap`, &
`font-weight` pd `.zpbloc` — SIFAR kesan (bendera kekal hilang
kesemua variasi ni, menolak suspek awal drpd fix "Kuasa Paksi pecah"
sblm ni). Sebaliknya, MEMBUANG `background` pd `.zpbloc-central`,
ATAU menambah `position:relative`, ATAU menambah `display:inline-
block` — KESEMUA membetulkan SEPENUHNYA (variasi piksel penuh selepas).
Kesimpulan: punca ialah kombinasi `display:inline` (lalai span) +
`background-color` + anak `<img>` — html2canvas-pro nampaknya lukis
latar bagi kotak inline TANPA susun-atur "sebenar" (span polos,
bukan positioned/block) dgn urutan yg overwrite anak `<img>` selepas
latar, bukan sebelum. `.zpkw` (span kata kunci `kw-*`) TAK PERNAH
kena bug ni sbb TIADA anak `<img>` langsung (teks polos sahaja via
`_escPdfHtml`) — bug ni khusus corak "span inline berlatar + anak
`<img>`", `.zpbloc` SATU-SATUNYA kelas berkongsi corak tu.

**Fix**: tambah `display:inline-block` ke `#zym-pr .zpbloc` (dipilih
drpd `position:relative` sbb lebih konsisten dgn `.zp-chip`/dll.
sedia ada yg turut guna `inline-flex`/`inline-block` utk elemen
badge). `white-space:nowrap` (fix sblm ni) KEKAL diperlukan drpd
sebab asal (elak frasa berbilang perkataan pisah pertengahan baris)
— dua fix ni BERASINGAN, bukan pengganti satu sama lain.

Disahkan via Playwright merentas 7 halaman skop 2-lajur Bab 3
(`bab-3-2` s/d `bab-3-8`): **SIFAR bendera hilang** drpd 135 imej
chip blok (160 chip kesemuanya) — sampel variasi piksel PENUH pd
SETIAP satu (bukan cuma tiada ralat), **SIFAR** `.zpbloc` melimpah
keluar sempadan kad induk (regresi-semak fix "Kuasa Paksi pecah"
sblm ni kekal selamat). Pratonton visual (zum 250%, `bab-3-2.html`
kad "Kuasa Tengah") sahkan bendera Jerman/Austria/Hungary/Bulgaria/
Uthmaniyah kesemuanya jelas di dlm ayat prosa biasa, bukan cuma
chip-list/legenda.

## Eksport PDF — Mod "Jimat Dakwat": ikon kekal, latar kata kunci gugur

Mod eco (`isEco`/`zp-mode-eco` dlm `_getPrintCss()`) DUA keputusan
reka bentuk yg mungkin nampak berlawanan intuisi pd pandangan pertama:

- **Ikon emoji KEKAL dipapar** (dulu `display:none!important` — buang
  ikon sepenuhnya). Sebab tukar: ikon berfungsi sbg penanda visual/
  navigasi pantas walau tanpa kos dakwat penuh warna, & TIADA kod
  "nyahwarna" berasingan diperlukan — muka surat eco PENUH (termasuk
  piksel ikon dlm kanvas tertangkap) sudah ditukar ke skala kelabu
  SELEPAS capture via `_pdfGrayscaleCanvas()` (rujuk
  `_pdfCanvasToJpegDataUrl()`), jadi ikon automatik jadi kelabu sekali
  dgn keseluruhan muka surat — tiada usaha tambahan.
- **Latar/padding penyerlah kata kunci (`.zpkw`) DIGUGURKAN** (dulu
  latar kelabu `rgba(241,245,249,0.95)` — kekal berlatar, cuma tukar
  warna drpd versi berwarna). Sebab: latar di belakang SETIAP kata
  kunci sebenarnya makan LEBIH BANYAK dakwat berbanding ikon (berpuluh
  kata kunci vs beberapa ikon setiap muka surat) — bercanggah dgn
  tujuan "jimat dakwat". Teks TEBAL (`font-weight:700`) sahaja
  dikekalkan sbg isyarat visual, biar pelajar highlight sendiri ikut
  cita rasa pd kertas cetak fizikal.

**JANGAN togol balik kedua-dua keputusan ni serentak** (cth. buang
ikon DAN buang latar sekali) tanpa tanya dulu — ia keputusan reka
bentuk berasingan dgn justifikasi berasingan, bukan pasangan yg
mesti sentiasa sama status.

## Eksport PDF — skop kandungan SENGAJA beza drpd nota digital

PDF bukan gantian nota digital utk bacaan santai — ia utk bacaan
PANTAS musim peperiksaan, jadi kandungan navigasi/swa-uji SENGAJA
digugurkan drpd PDF (kekal penuh di nota digital web) supaya lebih
ringkas & jimat kertas. Skop (`_renderSubChild()` dlm `_buildPrintHtml()`,
`main.js`):

- **"Soalan Utama"** (`.paper-flap-card`) — DIGUGURKAN sepenuhnya drpd
  PDF. Nilainya swa-uji semasa bacaan santai, bukan rujukan pantas.
- **"Fokus X.Y"** (`.paper-board` dgn `data-cv-title` bermula "Fokus")
  — DIGUGURKAN. Ia navigasi dalaman ke seksyen yg sama-sama ada
  beberapa inci di bawahnya dlm PDF linear yg dah lengkap — 100%
  redundan.
- **"Ringkasan X.Y"** & **"Rumusan Besar Bab N"** (`.paper-board`,
  `data-cv-title` LAIN drpd "Fokus") — KEKAL. Format padat/senarai
  pendek ni PALING sesuai utk corak bacaan-pantas exam berbanding
  perenggan penuh dlm Bahagian.

Semakan `data-cv-title` (bukan class/kandungan) sengaja dipilih sbb
"Ringkasan"/"Rumusan Besar" & "Fokus" kedua-duanya `.paper-board` —
tiada cara lain bezakan tanpa cek atribut ni. Kalau tambah jenis
board baharu kelak, semak `data-cv-title` ia dulu sebelum anggap ia
patut kekal/gugur — jangan andaikan drpd class sahaja.

## Eksport PDF — enjin `html2canvas-pro`, & SVG WAJIB diraster dulu

Eksport PDF (`_generatePages()` dlm `main.js`) render sisi-klien via
html2canvas + jsPDF (dimuat drpd CDN atas permintaan). DUA perkara
di sini pernah makan beberapa pusingan pembetulan buta — jangan ulang:

**1. Guna `html2canvas-pro`, JANGAN balik ke `html2canvas` 1.4.1.**
Keluaran terakhir 1.4.1 ialah 2021 (tidak lagi diselenggara) & pd
Chromium moden ia melukis **TEKS ~0.62em TERLALU RENDAH** berbanding
kotak/latar elemen. Disahkan empirik (Playwright + html2canvas
tempatan, bandingkan piksel vs `getBoundingClientRect()`): latar
elemen TEPAT (ralat −0.5px) tetapi teks tersasar **+15px** (skala 2),
KONSISTEN merentas Fredoka/Arial/Patrick Hand & tak berubah walau
tukar `line-height`/`position` bekas. Ini punca SEBENAR aduan berulang
"highlight kata kunci offset drpd tulisan" — **latar betul, teks yg
jatuh**, jadi mengubah CSS `.zpkw` (padding/`vertical-align`/
`transform`/`display`) TAKKAN membetulkannya (semua 7 varian diuji,
semua tersasar sama). `html2canvas-pro` 2.3.3 betulkan sepenuhnya
(ralat teks −1px), API serupa (turut dedah `window.html2canvas`).

**2. Ikon SVG MESTI diraster ke PNG sebelum capture.** html2canvas
(kedua-dua 1.4.1 & pro) GAGAL SENYAP melukis SVG OpenMoji: ikon jadi
`data:` URI sah, `img.complete === true`, `naturalWidth === 150`,
TAPI **SIFAR piksel** terhasil dlm kanvas — tiada ralat console.
Puncanya SVG OpenMoji hanya ada `viewBox`, **TIADA atribut
`width`/`height`** pd `<svg>` root (pelayar biasa fallback 150px &
papar normal; html2canvas tidak). Ikon Fluent (PNG) TAK terjejas —
sebab tu simptomnya "fluent nampak, openmoji tiada". `_pdfInlineImages()`
kini raster SVG → PNG (canvas 96px) selepas fetch, sebelum capture.

**Nota**: `_pdfInlineImages()` juga fetch SETIAP ikon & tukar ke
`data:` URI (bukan sekadar tunggu `load`) — elak "CORS-taint" imej
silang-asal yg turut boleh sebabkan ikon kosong senyap.

**3. `sw.js` JANGAN hidangkan respons OPAQUE kpd permintaan mode
`cors`.** Ikon CDN dicache drpd `<img>` (mode `no-cors`) → respons
**opaque**. Bila penjana PDF minta semula dgn mode `cors` (fetch →
`data:` URI, & `useCORS` html2canvas), pelayar TOLAK respons opaque
utk permintaan cors → fetch gagal → ikon Fluent kosong dlm PDF
WALAUPUN CDN boleh dicapai. Simptomnya mengelirukan: "ikon OpenMoji
muncul, Fluent tiada" (OpenMoji asal-sama, tak lalu laluan cache CDN
ni langsung). Penjaga `cached.type === 'opaque'` dlm handler emoji-CDN
`sw.js` MESTI dikekalkan.

**Peta ikon PDF**: `HZ_PDF_OPENMOJI_MAP` kini liputi **100% ikon Bab 1**
(78 konsep / 507 kemunculan), **100% konsep unik Bab 2** (+88 konsep
baharu, 166 kesemuanya), **& 100% konsep unik Bab 3** (+68 konsep
baharu, 234 kesemuanya) — sengaja penuh, bukan separa, sebab
liputan separa (dulu 25 konsep = 82%) tinggalkan **campuran gaya
OpenMoji + Fluent dlm senarai yg sama** (cth. keycap 1–4 OpenMoji tapi
5–6 Fluent) yg ketara janggal. Bila luaskan ke bab lain, liputi
SEMUA konsep bab itu sekali gus. `_pdfEmojiSrc()` turut terima segmen
varian pilihan sebelum `/3D/` (cth. `/assets/Writing hand/Default/3D/`)
— tanpa itu ikon sebegini senyap terlepas drpd peta.

**Bab 3 — kekecualian audit "100%": widget "Apa pendapat anda tentang
nota ini?" (`.nota-feedback`, suntik JS setiap halaman) BUKAN sebahagian
konsep Bab 3, tapi turut ketara semasa audit liputan.** Widget ni
(reaksi emoji "Thinking face"/"Confused face" antara lain) disuntik
sbg anak LANGSUNG satu `.note-subsection` (bukan saudara sejajar spt
disangka drpd kod sisipan `insertBefore.parentNode.insertBefore(widget,
insertBefore)`), jadi `_renderSubChild()` (tiada cabang eksplisit utk
`.nota-feedback` sblm ni) jatuh ke fallback generik `_bodyHtml(child)`
— seret 2 ikon reaksi ke PDF SETIAP halaman (pra-wujud, bukan
disebabkan luaskan skop 2-lajur, cuma senyap "tersembunyi" pd bab lain
kerana ikonnya kebetulan sudah dipeta drpd konsep lain). Widget ni
UI interaktif SAHAJA (suka/kongsi/muat turun PDF/reaksi emoji), tiada
makna dlm PDF cetak — fix SEBENAR bukan tambah 2 konsep ke peta, tapi
GUGURKAN terus drpd print (cabang baharu `cls.indexOf('nota-feedback')`
dlm `_renderSubChild()`, sama corak drpd `.hero-actions` sedia ada).

**Sumber SVG utk ikon baharu**: klon cetek `git clone --depth 1
--filter=blob:none --sparse` repo `github.com/hfg-gmuend/openmoji`,
`git sparse-checkout set data color` (jimat — repo penuh besar,
sparse hanya tarik `data/openmoji.json` + `color/svg/*.svg`). Padan
nama konsep Fluent (title-case, cth. `"Anger symbol"`) ke medan
`annotation` OpenMoji (lowercase) dlm `data/openmoji.json`, salin
`color/svg/<hexcode>.svg` → `assets/openmoji/<slug>.svg`. **Bukan
semua nama konsep Fluent padan TERUS dgn `annotation` OpenMoji** —
2 kes ditemui semasa luaskan ke Bab 2: `"Keycap 7"` → annotation
`"keycap: 7"` (format keycap OpenMoji guna `:`, bukan ruang), `"Pouting
face"` → annotation `"enraged face"` (emoji SAMA, U+1F621 — Unicode
namakan rasmi "POUTING FACE" tapi OpenMoji anotasi sendiri guna
"enraged face"; vendor lain cth. Fluent ikut nama Unicode rasmi).
Klon dipadam lepas siap salin (spt corak `circle-flags` utk bendera
— `assets/openmoji/LICENSE.md` sedia ada dah cukup, CC BY-SA 4.0
sama drpd Bab 1).

**Menguji eksport PDF dlm sandbox agen**: CDN html2canvas/jsPDF
disekat, TAPI boleh `npm install html2canvas-pro jspdf --no-save`
(`node_modules/` sudah di-gitignore) & suntik via Playwright
`addScriptTag({path})` — `_ensureLibs()` langkau muat turun CDN bila
`window.html2canvas` sudah wujud, jadi **aliran PDF SEBENAR boleh
dijalankan & diperiksa piksel demi piksel**. Guna cara ni utk sahkan
perubahan rupa PDF; JANGAN teka drpd CSS semata.

## Eksport PDF — Tajuk `h1`/`h2`/`.zp-acc-ttl`/kad Soalan Utama JANGAN `display:flex`

`_getPrintCss()` (`main.js`) asalnya set `display:flex;flex-wrap:wrap`
pd `h1.zp-title`, `h2.zp-section-title`, `.zp-acc-ttl`, `.zp-flap-q`,
`.zp-flap-a` supaya ikon (`img.zp-emoji`, child pertama) & teks tajuk
(`.zp-txt-up`, child kedua) jajar menegak kemas. Ni PECAH bila tajuk
panjang perlu >1 baris: `flex-wrap` bungkus keseluruhan ITEM flex
sbg unit atom (bukan per-perkataan spt aliran teks normal), jadi bila
item ke-2 (`.zp-txt-up`) tak muat sebelah item ke-1 (ikon) pd baris
semasa, SELURUH `.zp-txt-up` berpindah ke baris baharu — tinggalkan
ikon BERSENDIRIAN di baris pertama, terpisah drpd teks tajuknya.
Disahkan pengguna (tangkapan skrin: ikon tikus/jam pasir keseorangan
di atas "Negara bangsa Alam Melayu terbina melalui empat unsur
utama") & diagnosis piksel demi piksel via `Range.getClientRects()`
(bandingkan `top` baris teks pertama vs `img.getBoundingClientRect().top`)
pd enjin PDF SEBENAR (rujuk teknik ujian §atas).

Fix: BUANG kesemua `display:flex`/`flex-wrap`/`align-items`/`gap` drpd
5 rule di atas — kekalkan aliran INLINE biasa. `.zp-emoji` (kelas
ikon, `#zym-pr .zp-emoji`) SUDAH ada `vertical-align:middle` +
`margin:0 .24em 0 0` drpd awal, cukup utk jajar ikon+teks tanpa
flexbox — aliran teks normal bungkus PER-PERKATAAN spt sepatutnya,
ikon kekal melekat pd perkataan pertama tajuk tak kira berapa baris
teks tu bungkus. **JANGAN kembalikan `display:flex` pd rule tajuk PDF
ni** melainkan turut selesaikan masalah atomic-wrap-item di atas dgn
cara lain (cth. letak ikon sbg `background-image`/`::before` bukan
`<img>` berasingan, ATAU flex HANYA pd baris pertama via teknik lain)
— sekadar tambah `flex-wrap:wrap` semula akan hidupkan semula bug ni.

## Pratonton PDF — Zum skop kandungan sahaja (bukan seluruh modal)

Pratonton PDF (`#zym-pdf-overlay`) asalnya (PR sejarah "aktifkan
pinch-zoom native dlm pratonton PDF") longgarkan `touch-action`
sejagat (`document.documentElement`/`document.body`) kpd `'auto'`
semasa modal terbuka, supaya pengguna boleh pinch-zoom native. Ni
SILAP — zum yg terhasil ialah zum SELURUH VIEWPORT/modal (termasuk
topbar butang mod/muat turun/tutup), bukan skop kandungan PDF sahaja
— disahkan pengguna (tangkapan skrin: topbar pecah/terpotong lepas
pinch, tajuk jadi besar tak seimbang). Fix GANTIKAN sepenuhnya dgn
kawalan zum MANUAL berskop-terhad:

- Sekatan zum sejagat (§"Swipe Nav" di atas — `touch-action:pan-x
  pan-y` + `gesturestart/change/end` `preventDefault()` + `touchmove`
  berbilang-jari `preventDefault()`) KEKAL AKTIF TANPA PENGECUALIAN,
  termasuk semasa modal PDF terbuka (fungsi `hzPdfPreviewIsOpen()` &
  kedua-dua tapak panggilannya DIBUANG). Pinch native PELAYAR tak
  lagi berfungsi dlm modal — digantikan kawalan +/- DAN pinch
  dua-jari SKOP-TERHAD kendiri (`_pdfInitPinch()`, rujuk bullet di
  bawah), bukan cuma butang sahaja.
- `_pdfApplyZoom()`/`_pdfZoomBy()`/`_pdfResetZoom()` (`main.js`, lepas
  `var _pdfCache = {...}`) urus tahap zum (`_pdfZoomLevel`, langkah
  0.25 butang / berterusan pinch, julat **100%–300%** — 100% ialah
  MINIMUM, bukan 50%, sbb 100% ialah "muat skrin" asal, zoom
  SELALUNYA membesar drpd situ) via kelas `#zym-pdf-pages.zp-zoomed` + `width`
  piksel eksplisit pd SETIAP `<img>` slaid (bukan CSS `transform:scale`
  atau lebar-peratus — dua-dua berisiko "lompatan saiz" pd sempadan
  100%→101% sbb saiz semula jadi zum=1 imej dikawal `max-height`
  [portrait A4], bukan `max-width`). Lebar SEBENAR imej (`getBoundingClientRect().width`)
  diukur & dicache SEKALI (`img.dataset.pdfNaturalW`) sbg asas
  penskalaan piksel eksplisit semua tahap zum seterusnya — jamin
  saiz berterusan tanpa lompatan.
- **AWAS — lebar-semula-jadi MESTI diukur SEBELUM togol kelas
  `zp-zoomed`, bukan selepas.** Kelas `zp-zoomed` buang had
  `max-width`/`max-height` drpd `<img>` (perlu, supaya imej boleh
  tumbuh lepas lebar wrap semasa zum). Kalau diukur SELEPAS togol
  (susunan asal versi awal ciri ni), `getBoundingClientRect()`
  pulangkan saiz INTRINSIK PENUH imej (piksel kanvas raster sebenar,
  cth. 1587px) bukan saiz muat-CSS sepatutnya (cth. 302px) — punca
  lompatan zum DRASTIK (>500%) pd klik zum PERTAMA sahaja (klik
  seterusnya guna cache yg sudah rosak, kekal salah). Disahkan via
  ujian Playwright enjin PDF SEBENAR (§teknik ujian atas) — bandingkan
  `getBoundingClientRect().width` SEBELUM/SELEPAS setiap klik zum.
  `_pdfApplyZoom()` kini ukur/cache lebar utk imej yg belum ada
  `dataset.pdfNaturalW` DALAM gelung berasingan SEBELUM
  `pagesEl.classList.toggle('zp-zoomed', ...)` dipanggil.
- `.zym-pdf-page-canvas-wrap` (bekas imej) jadi viewport BERSAIZ TETAP
  (`max-height` SAMA nilai drpd had lama `<img>`, `overflow:auto`) —
  bekas TAK membesar bila zum, imej yg lebih besar diseret/ditatal DI
  DALAMnya. `#zym-pdf-pages.zp-zoomed .zym-pdf-page-canvas-wrap` tukar
  `align-items`/`justify-content` drpd `center` kpd `flex-start` —
  kandungan overflow YG DIPUSATKAN sebahagian TAK BOLEH dicapai via
  tatal (bug CSS terkenal), `flex-start` elak isu ni.
  `#zym-pdf-zoom-ctrl` (pil terapung `position:absolute`, bawah
  tengah viewport, SAMA corak dgn butang carousel prev/next sedia
  ada) papar label peratus + butang `−`/`+` (`disabled` pd julat
  had). Markup pil zum diletak sbg SAUDARA `#zym-pdf-pages` (BUKAN
  anak di dlmnya) dlm templat `#zym-pdf-pages-viewport` — kekal
  hidup merentas `pagesDiv.innerHTML=''` (reset slaid semasa jana
  semula/tukar mod). `_pdfApplyZoom()` dipanggil di hujung
  `_pdfPopulateSlides()` (semua 4 tapak panggilan) supaya tahap zum
  semasa terpakai semula pd slaid baharu (jana semula/tukar mod TAK
  reset zum pengguna).

**Pinch dua-jari skop-terhad + swipe tukar muka surat HANYA pd
100%** — susulan maklum balas pengguna: butang +/- sahaja (versi
awal ciri ni) tak semula jadi, gerak isyarat cubit lagi biasa drpd
kebiasaan pinch-zoom peranti. `_pdfInitPinch()` (`main.js`, lepas
`_pdfResetZoom()`) pasang `touchstart`/`touchmove`/`touchend`/
`touchcancel` pd `#zym-pdf-pages-viewport` SAHAJA (elemen kekal, tak
direset oleh `pagesDiv.innerHTML=''`) — BUKAN pd `document` spt
pinch native lama yg dibuang. Bila 2 jari dikesan, kira jarak antara
titik sentuh (`_pdfTouchDist()`, Pythagoras), skala zum drpd nisbah
jarak-semasa/jarak-mula × zum-mula, clamp 100%–300%, panggil
`_pdfApplyZoom()` terus setiap `touchmove` (bukan hanya di hujung
gerak isyarat) utk maklum balas visual masa nyata. **Kenapa handler
skop ni TETAP jalan walau sekatan sejagat `touchmove`
`preventDefault()` semua sentuhan berbilang-jari kekal aktif** —
event touch bubble drpd ELEMEN SASARAN ke ATAS (target → ... →
document), jadi listener pd `#zym-pdf-pages-viewport` (lebih dalam
drpd `document`) SENTIASA jalan DULU sebelum listener sejagat pd
`document` sempat `preventDefault()` — pinch skop kita kekal
berfungsi, sekatan sejagat cuma pastikan pinch NATIVE PELAYAR (yg
zoom seluruh viewport) tak tercetus serentak.

Swipe tukar muka surat (carousel `#zym-pdf-pages`, native
`overflow-x:auto` + `scroll-snap-type:x mandatory`) kini **HANYA
aktif pd 100%** — rule CSS `#zym-pdf-pages.zp-zoomed{overflow-x:
hidden;scroll-snap-type:none}` lumpuhkan carousel sepenuhnya bila
di-zum (togol serentak dgn kelas `zp-zoomed` yg sama drpd
`_pdfApplyZoom()`, tiada logik berasingan perlu). Sebabnya: bila
di-zum, seret mendatar/menegak PATUT panning imej besar di dlm
`.zym-pdf-page-canvas-wrap` (viewport dalaman `overflow:auto`
berasingan, sedia ada) — dua gerak isyarat (pan imej vs swipe
carousel) berlanggar kalau kedua-dua aktif serentak pd seretan
mendatar yg sama. Butang carousel `‹`/`›` (klik eksplisit, bukan
seret) TETAP berfungsi walau di-zum — `element.scrollLeft` set
programatik tak terjejas `overflow-x:hidden` (cuma sekat
scroll/seret DIPACU PENGGUNA), jadi navigasi jelas via butang tetap
tersedia tanpa gantung pd status zum.

**AWAS — `overflow:auto` pd `.zym-pdf-page-canvas-wrap` MESTI skop
`.zp-zoomed` sahaja, JANGAN letak dlm rule ASAS.** Versi awal ciri
zum letak `overflow:auto` + `overscroll-behavior:contain` terus pd
rule asas `.zym-pdf-page-canvas-wrap` (bukan sekadar rule `.zp-zoomed`
yg sedia ada) — nampak tak berbahaya (bekas tiada overflow SEBENAR pd
zoom=100%, imej muat penuh dlm `max-height`), tapi PECAHKAN swipe
carousel SEPENUHNYA walau pd 100%. Puncanya: `overflow:auto` sahaja
(tanpa overflow sebenar) dah cukup tandakan elemen tu "boleh tatal"
kpd pelayar, & `overscroll-behavior:contain` SEKAT rantaian tatal
(scroll chaining) drpd bekas dalaman ni ke carousel induk
(`#zym-pdf-pages`) — gerak isyarat swipe mendatar "ditelan" senyap
oleh bekas dalaman (yg tiada apa utk ditatal) sebelum sempat sampai
ke carousel utk tukar muka surat. Dilaporkan pengguna: "swipe sentuh
di pdf masih tak boleh alih ke page lain walaupun dah 100%" — disahkan
via Playwright + CDP `Input.dispatchTouchEvent` (simulasi swipe
sejari sebenar, BUKAN klik butang carousel — ujian klik butang
`scrollLeft` terus via JS TAK dedah bug ni, sbb `element.scrollLeft`
programatik tak terjejas `overscroll-behavior`, cuma gerak isyarat
sentuh SEBENAR yg terjejas): `scrollLeft` KEKAL 0 lepas swipe
sebelum fix, berubah betul (0→390) lepas `overflow:auto`/
`-webkit-overflow-scrolling:touch`/`overscroll-behavior:contain`
dipindah drpd rule asas ke rule `#zym-pdf-pages.zp-zoomed
.zym-pdf-page-canvas-wrap` SAHAJA (bekas kekal `overflow:visible`
lalai pd 100%, jadi swipe mendatar terus sampai ke carousel tanpa
disekat). **Nota ujian**: guna teknik simulasi sentuhan sebenar
(CDP `Input.dispatchTouchEvent` dgn urutan touchStart/touchMove/
touchEnd, BUKAN `page.click()` pd butang carousel) utk sahkan ciri
swipe — ujian berasaskan klik akan TERLEPAS kelas bug scroll-chaining
sebegini sepenuhnya.

## Eksport PDF — Bendera Negara guna OpenMoji, PDF SAHAJA (bukan nota digital)

Pengguna cadang bendera dlm PDF tukar drpd circle-flags (bulat, sumber
sedia ada §"Bendera Negara" atas) kpd OpenMoji (sepadan gaya ikon
OpenMoji lain dlm eksport PDF), gaya lencana ditukar dari bulat ke
segi empat "sketchy". **Skop DIHADKAN KETAT kpd PDF sahaja** — nota
digital (`notes/*.html`, `assets/flags/*.svg`, `.flag-icon` CSS dlm
`fluent-shell-emoji.css`) KEKAL circle-flags bulat TANPA DIUBAH
langsung (pengguna sahkan eksplisit selepas percubaan awal tersalah
skop site-wide: "tukar kepada bendera openmoji di pdf saja. bukan
nota digital"). Aset OpenMoji bendera BAHARU (45 fail, drpd hexcode
Unicode regional-indicator dikira drpd kod ISO2 — `0x1F1E6 +
(huruf-'A')` setiap huruf) disimpan BERASINGAN di
`assets/openmoji/flags/<kod-iso2>.svg` (bukan gantikan
`assets/flags/`), diliputi lesen sedia ada `assets/openmoji/
LICENSE.md` (CC BY-SA 4.0, sama drpd 166 ikon OpenMoji lain).

**Pemetaan & CSS PDF-sahaja** (`assets/js/main.js`): `_pdfFlagSrc()`
(lepas `_pdfEmojiSrc()`) petakan `/assets/flags/<kod>.svg` →
`/assets/openmoji/flags/<kod>.svg`. `_kwHtmlOne()`'s cabang IMG semak
`isFlag = /\/assets\/flags\//.test(src)` pd src ASAL SEBELUM sebarang
pemetaan (bukan lepas), sbb laluan pemetaan TUKAR src — semakan lewat
akan gagal padan corak asal. Kelas `flag-icon` sendiri TAK dikekalkan
dlm output PDF (semua `<img>` jatuh ke `class="zp-emoji"` tunggal),
jadi pengesanan MESTI drpd corak src, bukan className. `<img
class="zp-emoji zp-flag">` (kelas tambahan bila isFlag) dpt CSS
`object-fit:cover` nisbah 1.375:1 (lebar:tinggi) + border-radius +
box-shadow berlapis (rujuk `_getPrintCss()`) — SVG OpenMoji bendera
semua kongsi struktur SAMA (viewBox 72×72, jalur bendera sebenar pd
rect x=5,y=17,w=62,h=38, padding sekeliling drpd grid emoji Unicode),
jadi nisbah crop 1.375:1 ni universal merentas kesemua 45 bendera
tanpa perlu ubah SVG sumber satu-satu.

**Tiada kod rasterisasi/CORS tambahan diperlukan** — pipeline sedia
ada `_pdfInlineImages()` (fetch setiap `<img class="zp-emoji">` →
`data:` URI, raster SVG→PNG 96px) beroperasi generik atas SEMUA
`.zp-emoji`, jadi bendera (yg SENTIASA bawa kelas `zp-emoji` SERTA
`zp-flag`, bukan ganti) automatik ikut laluan sama tanpa kod baharu —
disahkan empirik (`src` akhir kesemua bendera cetak ialah
`data:image/png;base64,...`).

**Bug SEBENAR ditemui semasa sahkan ciri ni**: `_bodyHtmlNode()`
(fungsi laluan KEDUA drpd `_kwHtmlOne()` — dipakai bila `<img>`
tersarang dlm bekas pembalut generik yg tak dikenali mana-mana
cabang, cth. `<div class="bloc-legend-grid">` dlm kad "Panduan warna
pihak perang" bab-3-2.html/bab-3-3.html) TIADA cabang IMG langsung
sblm ni — `<img>` yg sampai ke fallback terakhirnya (`h +=
_bodyHtml(node)`) pulang STRING KOSONG (img tiada anak nod), bendera
hilang senyap drpd PDF. Ni bug SEDIA ADA (bukan disebabkan ciri
bendera ni — akan jejaskan ikon emoji biasa jugak kalau tersarang
serupa), ditemui secara kebetulan semasa audit menyeluruh (bandingkan
kiraan `img.flag-icon` sumber vs kiraan `.zp-flag` PDF merentas 12
halaman, disahkan Playwright + monkey-patch `window.fetch`/
`html2canvas`). Fix: tambah cabang `if (tag === 'IMG') { h +=
_kwHtmlOne(node); }` di awal `_bodyHtmlNode()` — delegasi ke logik
IMG SAMA drpd `_kwHtmlOne` (termasuk pengesanan bendera), elak
duplikasi.

**Kiraan bendera "kurang" yg BAKI (5 halaman diuji, `bab-2-3`,
`bab-2-4`, `bab-3-2`, `bab-3-3`, `bab-6-1`) SELEPAS fix di atas — SEMUA
dah disahkan bukan bug, drpd pengecualian sedia ada TAK berkaitan
bendera langsung**: (1) bendera dlm kad "Fokus X.Y"
(`.paper-kingdom`) — kad Fokus SELURUHNYA digugurkan drpd PDF
(§"skop kandungan SENGAJA beza" atas, dokumentasi sedia ada); (2)
bendera dlm `.paper-accordion-no` (ikon di HADAPAN tajuk pencetus
accordion) — header accordion cetak HANYA tarik teks
`.paper-accordion-title`, bukan seluruh kandungan pencetus (gelagat
generik SEDIA ADA, bukan khusus bendera — ikon lain yg diletak sana
pun sama nasib). Disahkan via klasifikasi Playwright penuh
(`img.closest('.paper-kingdom')`/`.closest('[data-cv-title^=Fokus]')`
& `.closest('.paper-accordion-no')`) merentas kelima-lima halaman:
kiraan "OTHER" (bukan Fokus, bukan accordion-no) SAMA PERSIS/lebih
drpd kiraan cetak sebenar pd setiap halaman & setiap kod negara —
SIFAR kehilangan bendera sebenar yg tak dijangka selepas fix.

## Pratonton PDF — Header/Footer WAJIB kongsi teks SAMA dgn PDF sebenar

Pengguna lapor (tangkapan skrin) header/footer dlm pratonton "tak
sepadan dgn pdf sebenar... menutup bahagian yg penting di sempadan
kertas" — diagnosis dedah dua bug SEBENAR pd `_pdfPopulateSlides()`
(pratonton HTML) berbanding `_savePdf()` (PDF jsPDF sebenar), yg
sebelum ni ditulis BERASINGAN & senyap lari (drift) drpd satu sama
lain:

1. **Tajuk header dipotong "…" dlm pratonton walau PDF sebenar TAK
   PERNAH memotongnya.** CSS lama (`white-space:nowrap;text-overflow:
   ellipsis`) paksa tajuk jadi SATU baris terpotong. `_savePdf()`
   pula guna `pdf.text(title,...,{maxWidth})` — jsPDF TAK memotong,
   ia LIPAT (wrap) ke baris baharu bila perlu. Disahkan (jsPDF
   `splitTextToSize` pd tajuk terpanjang seluruh korpus, ~70 aksara)
   tajuk SENTIASA muat SATU baris pd 7pt dlm `maxWidth` sebenar —
   bermakna PDF muat turun SENTIASA papar tajuk PENUH, tapi pelajar
   nampak versi TERPOTONG dlm pratonton. "Menutup bahagian penting"
   = maklumat (tajuk penuh) TERSEMBUNYI drpd pratonton walau ia AKAN
   tercetak penuh — bukan pertindihan visual literal (disahkan DOM:
   header/footer SENTIASA blok bertindan tegak dgn imej kandungan,
   TAK PERNAH `position:absolute` bertindih).
2. **Footer pratonton hilang "© 2026 ZymNotes" & kedudukan nombor
   muka surat berbeza.** `_savePdf()` footer PUNYA 3 bahagian (kiri
   `zymnotes.com`, TENGAH `i / total`, kanan `© 2026 ZymNotes`) —
   pratonton lama cuma 2 (`zymnotes.com` kiri, `i/total` KANAN, tiada
   hakcipta). Pelajar nampak footer BERBEZA drpd apa yg sebenarnya
   dimuat turun.

**Fix**: fungsi kongsi `_pdfHeaderFooterParts(title, pageIdx,
totalPages)` (lepas `_pdfPopulateSlides`) jana SEMUA teks header/
footer (hdrL/hdrR/ftrL/ftrC/ftrR) — dipanggil OLEH KEDUA-DUA
`_pdfPopulateSlides()` (bina HTML) DAN `_savePdf()` (lukis jsPDF),
elak dua laluan tulis teks berasingan lagi. Footer pratonton kini 3
lajur (`.zym-pdf-page-ftr-l/-c/-r`) padan struktur PDF sebenar tepat.

**Titik lipat baris tajuk pratonton dikira via `_pdfTitleLines()`**
(lepas `_pdfHeaderFooterParts`) — panggil `jsPDF.splitTextToSize()`
SAMA font/saiz/`maxWidth` (`helvetica` 7pt, `dims.cW*0.6`) drpd
`_savePdf()`, hasil disisip sbg `<br>` eksplisit dlm HTML (bukan
serah bulat-bulat kpd CSS auto-wrap) — jamin TITIK lipat pratonton
sepadan PDF sebenar bila PDF sebenar SEBENARNYA perlu lipat (kes
masa depan, tajuk lebih panjang drpd korpus semasa). CSS
`.zym-pdf-page-hdr-r` (max-width:60%, padan nisbah `dims.cW*0.6`
sebenar drpd 55% asal) kekal sbg jaring keselamatan visual — fon web
(Fredoka) kadangkala perlukan lebih ruang drpd metrik Helvetica dlm
PDF (AFM dalaman jsPDF, bukan bergantung fon OS/pelayar dipasang),
jadi bilangan baris VISUAL dlm pratonton kadang lebih byk drpd PDF
sebenar (cth. tajuk 70 aksara terpanjang korpus: 1 baris dlm PDF
sebenar, ~3 baris dlm pratonton HTML kerana fon lebih lebar) — TAPI
`overflow-wrap:break-word` (bukan `nowrap`/`hidden`) jamin TIADA
maklumat PERNAH hilang lagi, cuma paparan lebih tinggi drpd 1 baris.
**Percubaan padankan `font-family` chrome header/footer kpd
Helvetica/Arial (cuba kurangkan lipatan berlebihan) DIBUANG balik**
— tak beri kesan ketara dlm ujian (Helvetica lazimnya tiada dipasang
pd OS bukan-Apple, fallback pelbagai merentas peranti pengguna sebenar
tak boleh diramal), jadi dikekalkan Fredoka (konsisten dgn UI lain,
kebolehbacaan skrin lebih dipercayai drpd cuba padan metrik PDF cetak
kecil 7pt yg memang direka utk kertas, bukan skrin).

Disahkan via Playwright (suntik html2canvas-pro/jspdf tempatan,
klik "Muat turun", pintas `jsPDF.API.text`/`.save` utk baca teks
sebenar TANPA muat turun fail): tajuk PENDEK (`bab-2-3.html`,
34 aksara) kini papar PENUH SATU baris pratonton (sblm ni terpotong
"…"), footer 3-bahagian sepadan PERSIS teks `_savePdf()`; tajuk
TERPANJANG korpus (`bab-9-3.html`, 70 aksara) papar PENUH (tiada
potongan) walau lebih byk baris drpd PDF sebenar (had fon, dijangka
& diterima — bukan bug hilang maklumat).

**Susulan — keputusan "kongsi teks" di atas DITARIK BALIK, header/
footer HTML pratonton DIBUANG SEPENUHNYA.** Pengguna lapor (tangkapan
skrin, pinch-zoom 300%) header/footer `.zym-pdf-page-hdr`/`.zym-pdf-
page-ftr` (baris teks HTML berasingan, saiz fon TETAP) kekal pd saiz
asal semasa imej kandungan (`<img>`, discale via `_pdfApplyZoom()`)
membesar 3× — muka surat pratonton nampak "terpisah-pisah" bila
di-zum (header/footer tak turut membesar bersama kandungan spt SATU
muka surat fizikal patut berkelakuan). Arahan pengguna eksplisit:
"saya nak buang header dan footer itu seluruhnya. hanya a4 pdf statik
saja yang ditunjukkan sama macam preview pdf di mana mana."

**Kenapa fix ni SELAMAT (bukan regresi drpd fix "kongsi teks" atas)**:
header/footer HTML pratonton (`_pdfPopulateSlides()`) SENTIASA
berasingan drpd PDF muat turun SEBENAR (`_savePdf()`) — dua laluan
render BERBEZA drpd awal (satu bina elemen HTML flex utk paparan
modal, satu lukis teks vektor `pdf.text()` terus ke fail PDF via
jsPDF). `_pdfHeaderFooterParts()` (sumber teks kongsi) & fungsi
`_savePdf()` itu sendiri KEKAL TIDAK DISENTUH — muat turun PDF
SEBENAR masih ada header/footer penuh (kiri "ZymNotes/zymnotes.com",
kanan tajuk/hakcipta, tengah nombor muka surat), sbb teks tu teks
vektor SEBENAR dlm PDF (bukan overlay HTML), jadi ZUM native
mana-mana pembaca PDF akan skalakannya bersama kandungan secara
semula jadi — cuma paparan MODAL PRATONTON dlm laman (sebelum muat
turun) yg dipermudahkan. `_pdfTitleLines()` (fungsi pengiraan titik
lipat baris tajuk HTML, khusus utk header pratonton yg kini dibuang)
turut dibuang sbg kod mati — tiada pemanggil lain tinggal.

**Fix**: `_pdfPopulateSlides()` kini bina `.zym-pdf-page-outer` dgn
HANYA SATU anak (`.zym-pdf-page-canvas-wrap` berisi `<img>` kandungan)
— tiada lagi elemen `.zym-pdf-page-hdr`/`.zym-pdf-page-ftr` dicipta
langsung. Rule CSS berkaitan (`.zym-pdf-page-hdr*`, `.zym-pdf-page-
ftr*`, & `.zym-pdf-page-num` yg didapati kod mati sedia ada semasa
audit ni) dibuang sekali. Bajet tinggi `.zym-pdf-page-canvas-wrap`
(`max-height`) dilonggarkan drpd `min(72vh,calc(100dvh - 210px))` kpd
`min(78vh,calc(100dvh - 170px))` — ruang tambahan yg terbebas drpd
buang 2 baris header/footer diberi balik kpd imej kandungan supaya
muka surat pratonton nampak lebih besar/jelas.

Disahkan via Playwright (suntik html2canvas-pro/jspdf tempatan,
`bab-2-2.html`): `.zym-pdf-page-hdr`/`.zym-pdf-page-ftr` kiraan DOM
= 0 selepas buka pratonton, `.zym-pdf-page-outer` kini cuma SATU anak
(`.zym-pdf-page-canvas-wrap`); pratonton pd 100% & 300% (lapan klik
`#zym-pdf-zoom-in`) kedua-duanya papar HANYA kad putih berisi imej
kandungan — SATU unit tegar yg zum seragam, tiada baris teks
terpisah di atas/bawah lagi. Muat turun PDF SEBENAR (`_savePdf`,
pintas `jsPDF.API.text`) disahkan MASIH lukis teks header "ZymNotes"
spt sebelum ni — fungsi tu tidak diubah, cuma paparan modal pratonton
yg dipermudahkan.

**Susulan LAGI — "buang seluruhnya" di atas SILAP faham arahan
pengguna.** Pengguna tunjuk tangkapan skrin PDF sebenar (2 muka surat,
header "ZymNotes" + tajuk kanan, footer "zymnotes.com | 1/2 | © 2026
ZymNotes" kelihatan JELAS pd setiap muka surat) & jelaskan: "saya nak
paparan preview sama dengan pdf sebenar seperti gambar ini. ada
header dan footer yang statik supaya preview 100% sama seperti apa
yang akan mereka download dan print." Maksud sebenar arahan asal
("buang header dan footer... fleksibel") BUKAN "buang terus drpd
paparan" — tapi "buang versi FLEKSIBEL (baris HTML berasingan yg tak
turut zum) & gantikan dgn versi STATIK (terbenam terus dlm imej muka
surat, sama macam PDF sebenar)". Fix "buang seluruhnya" (PR #647)
terlalu literal — hilangkan maklumat header/footer terus drpd
pratonton walhal pengguna sebenarnya mahukannya KEKAL, cuma dlm
bentuk yg betul.

**Fix (menggantikan PR #647)**: `_pdfPopulateSlides()` kini panggil
fungsi BAHARU `_pdfComposePreviewPage(pc, dims, parts)` yg bina SATU
kanvas muka surat PENUH (bukan sekadar imej kandungan `pc` mentah) —
lukis latar putih saiz A4 penuh (`dims.pageW × dims.pageH` pd
`pxPerMm` yg sama drpd imej kandungan), letak imej kandungan pd
kedudukan `(mLeft, mTop)`, kemudian LUKIS TERUS teks header/footer
via Canvas 2D `ctx.fillText()` pd kedudukan/warna/saiz fon SAMA drpd
apa `_savePdf()` lukis via jsPDF vektor (rujuk §"Header/Footer WAJIB
kongsi teks SAMA" atas utk kedudukan asal: garis 0.3mm `#d4d4e8`,
`hdrL` bold 9pt `#6060a0` kiri, `hdrR` normal 7pt `#b0b0cc` kanan
[balut baris via `_pdfWrapCanvasText()`, anggaran greedy `ctx.
measureText()` — bukan `splitTextToSize()` jsPDF sebenar, tapi cukup
baik utk pratonton visual], `ftrL/C/R` normal 7pt `#9090b8`/`#b0b0cc`/
`#b8b8d0`). Sumber teks (`_pdfHeaderFooterParts()`) KEKAL dikongsi
kedua-dua laluan (canvas 2D di sini, jsPDF vektor pd `_savePdf`) —
prinsip "satu sumber kebenaran" drpd fix asal tak berubah, cuma
laluan LUKIS bertukar drpd HTML flex kpd canvas 2D terbenam.

Kanvas komposit ni jadi SATU-SATUNYA `<img>` yg dipaparkan pd setiap
slaid pratonton — muka surat kini SATU unit raster tegar, jadi zum
(pinch/butang) automatik skala header+kandungan+footer SERAGAM (tiada
lagi baris teks HTML berasingan yg boleh "tertinggal" saiz asal).
`_pdfCanvasToJpegDataUrl()` (yg grayscale SELURUH kanvas dlm mod eco)
SENGAJA TIDAK dipakai utk kanvas komposit ni — sebab `_savePdf()`
sebenar TAK PERNAH grayscale teks header/footer (vektor jsPDF, cuma
imej JPEG kandungan yg jadi kelabu via `_pdfGrayscaleCanvas` dlm mod
eco). `_pdfComposePreviewPage()` grayscale HANYA imej kandungan (`pc`)
SEBELUM dilukis ke kanvas komposit (`dims.grayscalePdf ?
_pdfGrayscaleCanvas(pc) : pc`), header/footer teks SENTIASA lukis
PENUH WARNA tak kira mod — padan tepat gelagat PDF sebenar dlm KEDUA-
DUA mod, bukan cuma mod penuh.

Disahkan via Playwright (suntik html2canvas-pro/jspdf tempatan)
merentas 3 senario: `bab-2-2.html` (skop 2-lajur) pd 100% & 300%
zum — header "ZymNotes"+tajuk & footer 3-lajur kelihatan terbenam
dlm imej, skala SERAGAM bersama kandungan semasa zum (dibandingkan
piksel dgn bug asal di mana header kekal saiz kecil tetap semasa
kandungan membesar 3×); mod "Jimat dakwat" (`bab-2-2.html`) — imej
kandungan bertukar kelabu, header "ZymNotes" KEKAL warna asal
(`#6060a0`); `bab-9-3.html` (skop 1-lajur, luar julat 2-lajur) —
kanvas komposit turut berfungsi betul (geometri margin/dims sama
struktur tak kira mod lajur). Sifar ralat JS pd kesemua senario.
Muat turun PDF sebenar TIDAK terjejas — `_pdfPageCanvases`/`_pdfDims`
(dipakai `_savePdf()`) kekal imej kandungan MENTAH tanpa header/
footer terbenam (elak lukis dua kali dlm fail PDF akhir).

## Sub-tajuk `.paper-strip.strip-sub` dlm accordion — pendua DIGUGURKAN (PDF & laman hidup)

Pengguna lapor (tangkapan skrin pratonton PDF `bab-2-3.html`) item
accordion "Dahagi India 1857" papar tajuk "Dahagi India 1857" DUA
KALI berturutan (sekali di header accordion, sekali lagi kad kecil
sejurus di bawahnya) & satu ikon bendera 🇮🇳 "terputus" — muncul
bersendirian pd baris sendiri tanpa apa-apa teks bersama.

Punca: corak HTML sedia ada (`.paper-accordion-item > .paper-accordion-
panel > .cv-unit-body > .paper-strip.strip-sub`) letak sub-tajuk
"recap" (selalunya teks SAMA/singkatan drpd tajuk accordion tu
sendiri, kadang + bendera) sbg anak PERTAMA badan panel — bermakna
bila accordion dibuka di laman hidup, pembaca nampak semula tajuk +
konteks (munasabah, sbb accordion boleh collapse/expand, pembaca
mungkin lupa tajuk bila scroll dlm panel panjang). Tapi `_bodyHtmlNode()`
(penjana PDF) TIADA cabang utk kelas `.paper-strip` — jatuh ke
fallback generik `_bodyHtml(node)` yg (a) skip SEMUA nod teks terus
(bukan dibalut tag dikenali) & (b) — SELEPAS fix `.bloc-legend-grid`
sblm ni (tambah cabang IMG) — KEKALKAN sebarang `<img>` tersarang di
situ. Kombinasi ni pulangkan: teks "Dahagi India 1857" HILANG (spt
biasa), TAPI bendera (skrg terselamat drpd fix IMG) KEKAL bersendirian
tanpa konteks — nampak "emoji terputus". Dlm PDF LINEAR (semua
kandungan sentiasa "terbuka", tiada collapse/expand), sub-tajuk recap
ni jadi 100% PENDUA drpd tajuk accordion yg SUDAH tercetak (`.zp-acc-
ttl`, drpd `.paper-accordion-title`) — bukan sekadar bug render, TAPI
pendua ketara pd konsepnya.

Disahkan menyeluruh (regex `.cv-unit-body > .paper-strip.strip-sub`
langsung, merentas SEMUA `notes/bab-*.html`): **77/79** kejadian
berada DALAM `.paper-accordion-panel` & teksnya SAMA/singkatan drpd
tajuk accordion sendiri (cth. "Gerakan Sosioagama Awal" vs tajuk
accordion "Gerakan sosioagama awal" — beza case sahaja) — pendua
tulen. **2/79** (`bab-8-3.html`, "Komposisi Ahli MPP 1948"/"1955")
berada LUAR accordion (label unik carta bar `.paper-bar-list`,
BUKAN pendua — satu-satunya label utk data tu).

Fix (`_bodyHtmlNode()`): tambah cabang `cls.indexOf('paper-strip')`
— jika elemen ADA `.closest('.paper-accordion-panel')` (dlm accordion),
GUGURKAN terus (kembalikan `h` tanpa diubah); jika TIADA (di luar
accordion, cth. kes bar-chart bab-8-3), cetak spt biasa via `_kwHtml`
(sama corak `stripHtml` `_renderBoard`, kekalkan teks + bendera/ikon).
Disahkan via Playwright (suntik html2canvas-pro/jspdf, pintas
`window.html2canvas` baca `#zym-pr` sblm capture) merentas 6 halaman
(`bab-2-3`, `bab-2-4`, `bab-3-3`, `bab-3-4`, `bab-6-1`, `bab-8-3`):
SIFAR `<img class="zp-emoji">` bersendirian sbg anak langsung
`.zp-acc-body` (dulu berlaku, kini 0 pd semua halaman), teks
"Komposisi Ahli MPP 1948/1955" (bab-8-3, kes LUAR accordion) KEKAL
tercetak penuh. Bilangan `.zp-acc-ttl` tercetak (title accordion
SEBENAR, bukan sub-tajuk recap yg digugurkan) konsisten `sourceCount
- 1` merentas KESEMUA 6 halaman berbanding `.paper-accordion-title`
sumber — satu-satunya beza dikesan (`"Warna kata kunci"`, accordion
legenda kata kunci) SUDAH digugurkan drpd PDF sebelum fix ni lagi
(gelagat sedia ada tak berkaitan, bukan regresi fix ni).

**Susulan — pengguna tunjuk tangkapan skrin LAMAN HIDUP (bukan PDF)**
lepas fix di atas: sub-tajuk pendua "Dahagi India 1857" ni turut
kelihatan di laman hidup sendiri (kad hijau berulang tajuk yg SAMA
persis dgn header accordion sejurus di atasnya), minta digugurkan
terus drpd HTML sumber — "biar accordion saja jadi tajuk", bukan
sekadar ditapis semasa eksport PDF.

**Ketepatan skop PENTING**: bukan SEMUA 77 kejadian ni pendua tulen.
Audit lanjut (bandingkan kedudukan — adakah sub-tajuk ANAK PERTAMA
`.cv-unit-body`, atau muncul KEMUDIAN selepas kandungan lain) dedah
**1 kekecualian SAH**: `bab-3-3.html` "Kegagalan Operasi Menawan
Rusia" — muncul SELEPAS satu perenggan lain dlm accordion "B.
Keberkesanan Strategi Serangan Balas", ikon "Snowflake" (bukan
bendera), teks LANGSUNG BERBEZA drpd tajuk accordion (bukan
singkatan/case-beza spt 76 kes lain) — ini penanda PERALIHAN topik
SAH di tengah badan accordion, BUKAN pendua tajuk. Kedudukan "anak
PERTAMA `.cv-unit-body`" (bukan sekadar "di dalam accordion mana-
mana") ialah pembeza tepat: 76/77 kejadian ADA di kedudukan ni
(disahkan BeautifulSoup, `cvbody.children` pertama === strip node),
1/77 (Rusia) TIADA.

**Fix (HTML sumber, `notes/*.html`)**: regex sepadan corak PERSIS
`<div class="paper-accordion-panel"...><div class="cv-unit-body">\n
[ruang pilihan]<div class="paper-strip strip-sub">...</div>\n` (anak
pertama SEBAIK panel/body dibuka) & buang SELURUH baris strip-sub tu
(kekalkan `<div class="cv-unit-body">` & baris seterusnya tanpa
diubah) — regex TAK PADAN corak "Rusia" (ada kandungan LAIN antara
`cv-unit-body` & strip tu), jadi kes SAH tu automatik terselamat
tanpa senarai pengecualian manual. **76 kejadian dibuang merentas 12
fail** (`bab-2-2`×8, `bab-2-3`×8, `bab-2-4`×18, `bab-2-6`×2, `bab-2-7`
×11, `bab-2-8`×10, `bab-8-1`×3, `bab-8-2`×2, `bab-9-1`×2, `bab-9-2`×3,
`bab-9-3`×6, `bab-9-4`×3) — perhatikan senarai fail ni BERBEZA drpd
senarai 6 halaman diuji semasa fix PDF asal di atas (`bab-2-3`,
`bab-2-4`, `bab-3-3`, `bab-3-4`, `bab-6-1`, `bab-8-3`) — corak pendua
ni jauh lebih meluas drpd sampel awal, hanya ketara selepas audit
SEPENUH korpus (`notes/bab-*.html`, bukan sampel manual). Disahkan
selepas buang: `.paper-accordion-title` kekal padan `.paper-
accordion-panel` (bilangan sama) pd SEMUA 12 fail, `<div>`/`</div>`
seimbang (kiraan grep sama), `python3 scripts/check-zh-coverage.py`
kekal 100% (elemen dibuang TIADA `data-zh-unit-id` langsung — teks
sub-tajuk ni sentiasa polos, bukan unit ZH berasingan).

Bendera negara pd sub-tajuk yg dibuang (cth. `in.svg` India) TAK
hilang drpd laman hidup — accordion tu SENDIRI (di `.paper-accordion-
no`, slot ikon sebelah kiri header) SUDAH papar bendera SAMA (rujuk
§"Bendera Negara" atas, corak "ikon dlm `.paper-accordion-no`" +
".paper-strip.strip-sub` sepadan" — dua tempat memang sengaja papar
bendera SAMA drpd awal, ni yg buat sub-tajuk jadi pendua penuh, bukan
separa). Kesan sampingan: PDF pun turut kehilangan laluan sub-tajuk
ni (sumber utama bendera muncul dlm PDF linear, sbb `.paper-
accordion-no` sendiri dikecualikan drpd cetak — rujuk §"Bendera
Negara... PDF SAHAJA" — accordion-no flags SUDAH sedia dikecualikan
drpd PDF sblm ni) — DITERIMA sbb konsisten dgn gelagat `.paper-
accordion-no` yg SUDAH pun tak muncul dlm PDF, bukan regresi baharu.

**Fix (JS PDF, `_bodyHtmlNode()`)**: laluan skip lama (semak SAHAJA
`.closest('.paper-accordion-panel')`, tanpa kira kedudukan) tersalah
gugurkan "Kegagalan Operasi Menawan Rusia" jugak drpd PDF (regresi PR
#636). Diketatkan kpd `node.previousElementSibling === null &&
node.parentElement.classList.contains('cv-unit-body') &&
.closest('.paper-accordion-panel')` — SAMA kriteria "anak pertama"
drpd regex HTML di atas, jamin dua laluan (buang drpd sumber & tapis
PDF) sentiasa SEPAKAT. Lepas fix HTML sumber, cabang JS ni jadi
jaring keselamatan (should never trigger lagi, sbb 76 kejadian dah
tiada terus drpd DOM) — tapi kekal berguna kalau kandungan masa depan
tersilap ulang corak pendua ni.

Disahkan (Playwright, ulang teknik suntik html2canvas-pro/jspdf)
merentas 13 halaman (12 halaman disunting + `bab-3-3` kes
kekecualian): sifar `unexpectedMissing` (bandingkan `.paper-
accordion-title` sumber vs `.zp-acc-ttl` cetak, kecuali "Warna kata
kunci" legenda yg sedia dikecualikan), `orphanCount` (imej
bersendirian dlm `.zp-acc-body`) SIFAR pd SEMUA halaman, & teks
"Kegagalan Operasi Menawan Rusia" disahkan HADIR semula dlm PDF
`bab-3-3.html` (pulih drpd regresi PR #636).

## Eksport PDF — entri dlm menu FAB sparkle (ciri kekal tersembunyi)

Sebelum ni satu-satunya laluan cetuskan pratonton PDF ialah butang kecil
`.nota-feedback-pdf-btn` dlm widget "Apa pendapat anda tentang nota ini?"
di PENGHUJUNG halaman subtopik — pengguna nyata ciri PDF "tidak begitu
menonjol sedangkan ia boleh menjadi ciri yang berharga", minta ditambah
ke menu FAB sparkle (butang bulat terapung, sentiasa kelihatan tanpa
scroll ke bawah).

`setupNoteFeatures()` (`assets/js/main.js`) kini tambah item "Muat turun
PDF" (ikon `HZ_ICONS8_SPARKLE.pdfDownload`, URL SAMA drpd `PDF_DL_SRC`
sedia ada — nilai terpaksa DIDUPLIKASI sbg entri regisrti baharu, bukan
rujuk terus, sbb `PDF_DL_SRC` diisytihar dlm IIFE eksport PDF BERASINGAN
[baris ~3189+] yg tak boleh diakses drpd IIFE `setupNoteFeatures()`)
digerbangkan `hzZymnotesIsSubtopicNotePathname(_p)` — SAMA fungsi semak
yg sedia ada dipakai gerbang keseluruhan menu FAB, jadi item ni HANYA
muncul pd halaman subtopik nota (bukan hab bab/`index.html`/kuiz — laman
tu tiada ciri PDF langsung).

**Klik-kan butang tersembunyi sedia ada, JANGAN panggil `openPdfPreview()`
terus.** Fungsi `openPdfPreview()` PRIVAT dlm closure IIFE PDF (tak
didedah `window`), jadi item FAB baharu guna
`document.querySelector('.nota-feedback-pdf-btn').click()` — cetus
pipeline sedia ada tanpa perlu ubah/dedah fungsi privat tu. Ini SELAMAT
drpd isu timing (elemen tak wujud lagi) sbb IIFE PDF (yg bina & sisip
`.nota-feedback-pdf-btn` ke DOM) TIADA gerbang `DOMContentLoaded`
sendiri — ia jalan segerak semasa skrip dimuat, jauh SEBELUM pengguna
sempat berinteraksi dgn FAB (buka menu FAB perlukan klik pengguna,
mustahil berlaku sebelum skrip habis jalan).

**Item baharu guna corak listener BERASINGAN (spt item `settings` sedia
ada), BUKAN router klik delegasi `itemsContainer` (yg cuma kendali
`nav`/`audio`/`lab`)** — router delegasi semak `data-sparkle-type` tapi
tiada cabang `pdf`, jadi klik pd item ni jatuh melalui router tanpa
kesan (tiada konflik double-fire), listener sendiri (dilekap terus pd
elemen item, IIFE sama corak `settingsEl.addEventListener(...)`) yg
tutup panel FAB (`wrap.classList.remove('is-open')`) & cetus klik.

Disahkan via Playwright (suntik html2canvas-pro/jspdf tempatan,
`_ensureLibs()` langkau CDN bila lib dah wujud) merentas 4 jenis
halaman: item "Muat turun PDF" MUNCUL pd halaman subtopik (`bab-4-2.html`,
klik → `#zym-pdf-overlay` bertukar `is-open` = betul, pratonton PDF
sebenar terjana), TIADA item pd hab bab (`bab-4.html`), indeks nota
(`notes/index.html`), & halaman kuiz (`quiz/bab-4-2.html`) — sifar
ralat JS pd keempat-empat jenis halaman.

