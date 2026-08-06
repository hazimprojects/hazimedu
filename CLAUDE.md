# ZymNotes — Panduan Agen

Laman statik (HTML/CSS/JS vanilla, tiada framework/build step JS) untuk nota
ulang kaji KSSM pelajar Malaysia. Deploy ke GitHub Pages (domain custom
`zymnotes.com` via `CNAME`, `.nojekyll` — serve terus dari root repo, `docs/`
bukan folder Pages, ia dokumentasi dalaman). Rujuk `README.md` untuk
senarai ciri & struktur penuh — fail ni fokus pada apa yang perlu tahu
supaya tak tersalah anggap senibina sedia ada.

## Fokus Semasa

`docs/project-strengths-audit.md` catat: **cadangan ciri baharu sengaja
ditutup buat masa ini — fokus kekal penstabilan kandungan sedia ada**
(prestasi, kebolehpercayaan, kualiti kandungan Bab 1–8 Sejarah T4).
Jangan cadang/tambah ciri baharu secara proaktif melainkan diminta;
utamakan kerja jenis bug-fix/prestasi/kestabilan.

## Realiti "Sistem Build" — content/*.yaml TIDAK aktif

`scripts/build.py` (content/*.yaml → notes/*.html) wujud, tapi **SEMUA**
53 fail dalam `content/*.yaml` masa ini bertanda `passthrough: true` —
bermakna build.py **skip** generation utk semuanya (`0 built, 53
passthrough` bila dijalankan). Realitinya: `notes/*.html` &
`quiz/*.html` ialah SUMBER SEBENAR, diselenggara terus (tangan atau
skrip one-off dalam `scripts/`), BUKAN dijana drpd YAML. Jangan edit
`content/*.yaml` sambil sangka `python3 scripts/build.py` akan
propagate perubahan ke HTML — ia takkan buat apa-apa selagi
`passthrough: true` kekal. Edit `notes/*.html`/`quiz/*.html` terus.

(`build.py` masih berguna utk satu perkara: `update_sw_precache()` —
auto-sync senarai `/notes/bab-*.html` dlm `sw.js` PRECACHE_URLS bila
bab baharu ditambah.)

## Ikon Emoji — satu sumber, CDN luar

Setiap halaman nota boleh ada 50–150+ `<img class="fluent-3d-emoji ...">`
(emoji Fluent 3D Microsoft, ditarik dari `cdn.jsdelivr.net`). Penjanaan
HTML statik (dlm `scripts/html_generator.py` via `content/`, walau
jarang dipakai memandangkan passthrough) datang dari **satu tempat**:
`scripts/emoji_map.py` (`get_emoji_img`/`get_chip_img`). Penjanaan sisi
klien (sparkle menu, badge bab) ada salinan setara dlm
`assets/js/main.js` (`hzFluentSparkleImg`/`hzFluentImgHtml`/dll) —
kekalkan kedua-dua SEGERAK bila ubah format tag ikon.

Semua ikon emoji ni **kena** `loading="lazy"` (kecuali: nav bar bawah —
sentiasa nampak; & `_kwHtmlOne` dlm `main.js` — penjana eksport PDF,
lazy-load boleh sebabkan ikon kosong dlm PDF sebab html2canvas capture
sebelum imej load). `sw.js` cache ikon dari `cdn.jsdelivr.net` &
`img.icons8.com` secara cache-first (rule eksplisit dlm fetch handler)
supaya ikon still render dlm mod offline PWA — JANGAN buang rule ni
tanpa gantikan strategi cache offline yg setara.

## Bendera Negara — self-hosted (`assets/flags/`), BUKAN CDN luar

Fluent Emoji (pembekal ikon utama) sengaja TIADA bendera negara (isu
neutraliti politik Microsoft). Pembekal rasmi bendera ZymNotes ialah
**`circle-flags`** (github.com/HatScripts/circle-flags, MIT, SVG bulat
minimal) — dipilih drpd Icons8 sbb Icons8 wajib pautan-balik atribusi
utk tier percuma, `circle-flags` tidak. Beza drpd ikon emoji: bendera
**di-self-host** dlm `assets/flags/<kod-iso2>.svg` (cth. `de.svg`,
`jp.svg`), BUKAN dirujuk terus dari CDN luar — sebab (1) sandbox/
rangkaian tertentu boleh sekat domain CDN baharu yg belum "dipercayai",
(2) elak ulang isu offline-cache yg pernah timbul dgn ikon emoji CDN,
(3) set yg diperlukan kecil & tetap (bukan >400 bendera penuh), jadi
self-host lebih ringkas drpd urus rule cache tambahan dlm `sw.js`.

- Tambah bendera baharu: salin fail SVG relevan dari repo
  `circle-flags` (`flags/<kod>.svg`) ke `assets/flags/`, KEKALKAN
  `assets/flags/LICENSE.md` (keperluan MIT — teks lesen mesti disertakan
  bersama salinan).
- Kelas CSS `.flag-icon` (dlm `assets/css/fluent-shell-emoji.css`)
  tambah ring putih/gelap + shadow supaya nampak macam lencana,
  digunakan BERSAMA `fluent-3d-emoji openmoji--inline` (bukan ganti) —
  kekalkan kedua-dua kelas bila tambah bendera baharu.
- **Hanya** ganti/tambah ikon pada chip yg teksnya **tepat** nama
  negara (cth. `Jerman`, bukan `Adolf Hitler – pemimpin Jerman`) — elak
  bendera muncul pada chip nama tokoh/ayat yg sekadar sebut negara.
  Skop semasa: 36 negara (rujuk senarai kod ISO dlm `assets/flags/`)
  merentas 13 halaman — bab-3-2, bab-3-3 s/d bab-3-8 (PD1/PD2),
  bab-4-6, bab-5-1, bab-5-2, bab-6-1, bab-6-3, bab-7-5. Entiti sejarah
  yg SENGAJA dilangkau (bukan negara berdaulat moden yg bersih; perlu
  keputusan ketepatan sejarah, bukan padanan mekanikal) — JANGAN tambah
  bendera utk ni tanpa tanya user dulu:
  - Czechoslovakia, Yugoslavia — dah pupus, >2 negara pengganti,
    tiada 1 bendera "betul" (beza drpd Austria-Hungary yg guna 2
    bendera sbg petunjuk — Czechoslovakia/Yugoslavia lagi teruk,
    bukan 2 entiti asal yg jelas).
  - Manchuria, Hong Kong — bukan negara berdaulat (negara boneka
    Manchukuo & jajahan British), bendera akan mengelirukan makna
    "bendera = negara berdaulat".

  Kesemua 4 entiti di atas guna **satu** lencana glob bulat (emoji
  Fluent sedia ada, kunci `"globe"` dlm `emoji_map.py` — "Globe showing
  asia-australia", BUKAN "Globe with meridians" yg gaya wayar-grid)
  + kelas `.flag-icon` (ring+bayang sama) supaya ritma visual konsisten
  dgn chip berbendera sebenar tanpa palsukan makna "negara berdaulat".
  JANGAN biar >1 ikon bertindan (cth. Czechoslovakia/Yugoslavia asalnya
  ada 2-3 glob "meridians" bertindan — dah dinormal ke 1).

## Bug Chip Terputus Baris — combinator `.paper-chip-list .paper-chip`

**Elak selector CSS bentuk `.paper-chip-list .paper-chip` (descendant,
ruang kosong) — guna `.paper-chip-list > .paper-chip` (child, `>`).**

Punca: `<span class="paper-chip bloc-chip-*">` (chip negara/blok PD1/
PD2 dlm ayat, cth. `bab-3-2.html`–`bab-3-8.html`) selalu tersarang DUA
lapis dlm `.paper-chip-list` (`.paper-chip-list > div.paper-chip.
paper-chip-sentence > span.paper-chip.bloc-chip-axis`). Selector
descendant `.paper-chip-list .paper-chip` (dlm `responsive.css`, mod
mudah alih ≤760px) terkena BUKAN sahaja `div.paper-chip-sentence`
(anak terus — betul, patut `display:block`) tapi JUGA `span.paper-chip`
tersarang jauh di dlm ayat (salah — patut kekal `inline-block` ikut
rule `span.paper-chip`). Sebab dua kelas (`.paper-chip-list .paper-chip`)
kalahkan satu-kelas-satu-elemen (`span.paper-chip`) dlm spesifisiti CSS
tanpa kira urutan fail, chip dlm ayat jadi block — sebab tu ayat macam
"...ialah [Kuasa Paksi] dan [Kuasa Bersekutu]." pecah jadi setiap kata/
chip/noktah baris berasingan pd skrin mudah alih.

Dah dibetulkan (`.paper-chip-list > .paper-chip`, dsb.) — kekalkan
combinator `>` tu bila sunting `responsive.css` seksyen chip-list.
Kalau tambah selector `.paper-chip-list`-berkaitan baharu yg set
`display`, SENTIASA guna `>` melainkan sengaja nak terkena keturunan
jauh (jarang berlaku).

## Palet Kata Kunci — KANONIK, jangan tambah kelas baharu ikut bab

Sistem warna kata kunci ialah janji kpd pembaca: **satu kelas = satu
makna = satu warna, sama pada SEMUA bab**. Dulu setiap bab cipta set
sendiri (19 variasi legenda berbeza; `kw-tahun` vs `kw-masa` utk konsep
sama) — ini sengaja dihapuskan. 11 kelas kanonik sahaja:

`tokoh` · `masa` · `tempat` · `peristiwa` · `pertubuhan` · `gerakan` ·
`kerajaan` · `pentadbiran` · `perjanjian` · `istilah` · `karya`

- Label rasmi tiap kelas ada dlm `KEYWORD_LABELS`
  (`scripts/html_generator.py`) — guna label tu, jangan karang sendiri.
- JANGAN cipta kelas `kw-*` baharu utk bab tertentu. Kalau kandungan
  baharu betul-betul tak muat mana-mana 11 ni, bincang dulu — menambah
  warna ke-12 mengurangkan keupayaan pembaca bezakan yg sedia ada.
- Kelas LAMA yg dah dimansuhkan (jangan hidupkan semula):
  `kw-tahun`/`kw-tarikh` → guna `kw-masa`; `kw-konsep` → guna `kw-istilah`.
- Warna ditakrif di **EMPAT** tempat yg mesti KEKAL SEGERAK:
  `assets/css/keywords.css`, `assets/css/base.css` (salinan),
  `assets/css/print.css` (senarai selektor), dan penjana PDF dlm
  `assets/js/main.js` (kelas `zpkw-*` + regex `kw-(...)`).
- Ketepuan/kecerahan latar SERAGAM (HSL L86/S85) — ini yg buat warna
  boleh dibeza. Dulu alpha berbeza-beza (0.45–0.72) melunturkan latar
  sampai ΔE 3 antara pasangan yg muncul serentak. Jangan ubah satu-satu.

**Legenda dijana per halaman, ikut penggunaan SEBENAR** —
`finalize_keyword_legend()` (`html_generator.py`) mengisi penanda
`<!--KEYWORD_LEGEND-->` dgn HANYA jenis yg wujud pd halaman itu; kalau
tiada langsung, legenda digugurkan. Jangan hardcode senarai legenda
(dulu hardcoded 8 jenis → 68 entri "hantu" & 5 warna tanpa penjelasan).

## Legenda Kata Kunci — Struktur Accordion (Collapse Lalai)

Analisis ruang skrin (viewport mobile 390px) dedah hero setiap halaman
subtopik makan **~936px SEBELUM nota sebenar** — lebih tinggi drpd satu
skrin penuh (844px). Penyumbang terbesar: legenda kata kunci (277px,
sentiasa terbuka penuh) walaupun palet dah kanonik sejagat (pembaca
kembali tak perlu baca semula tiap halaman).

`finalize_keyword_legend()` (`html_generator.py`) jana legenda sbg
**satu accordion item** (guna semula mekanisme `paper-accordion` sedia
ada — bukan komponen togol baharu), **collapse lalai**:
`.paper-accordion.keyword-legend-accordion > article.paper-accordion-
item.keyword-legend-wrap > button.paper-accordion-trigger + div.
paper-accordion-panel`. Jimat ~150-175px setiap halaman (+ ~26px
tambahan drpd pemadatan trigger — lihat commit "padatkan trigger").

**SEMUA 50 halaman `notes/*.html`** (+ kedua-dua `_templates/nota-
bab.html` & `_templates/nota-subtopik.html`) kini guna struktur ni —
migrasi drpd struktur lama (kad rata `<div class="keyword-legend-
wrap"><p class="keyword-legend-title">...</p><div class="keyword-
legend-grid">`) SIAP sepenuhnya (prototaip `bab-3-2.html` → 44
halaman subtopik + 8 halaman ringkasan bab, PR susulan). CSS
(`assets/css/keywords.css`) dah dibersihkan — rule box/padding/
border-radius/shadow LAMA (khusus struktur rata) dibuang sepenuhnya
sebab kini diwarisi terus drpd `.paper-accordion-item` (paper.css);
`.keyword-legend-wrap` kekal sbg kelas penanda kosong utk skop rule
trigger padat (`> .paper-accordion-trigger`) sahaja. Jika nampak
struktur rata lama di mana-mana halaman baharu, itu regresi — tukar
ikut struktur di atas (rujuk `notes/bab-1-1.html` atau `_templates/
nota-subtopik.html` sbg contoh).

**TIADA auto-scroll bila togol** — handler klik accordion sejagat
(`assets/js/main.js`, delegasi pada `document.body`) skrol-ke-posisi
scroll-into-view secara lalai bila accordion lain dibuka (supaya
kandungan panjang di bawah lipatan kekal kelihatan). Legenda kata
kunci SENGAJA dikecualikan drpd tingkah laku ni — semak
`currentItem.classList.contains("keyword-legend-wrap")` di awal
handler, guna `setAccordionState()` terus tanpa `window.scrollTo`/
stabilisasi. Sebabnya: legenda selalu dekat bahagian atas hero (dlm
pandangan sedia ada), skrol paksa jadi tak perlu & mengganggu.
JANGAN buang semakan ni bila ubah handler accordion sejagat.

## Swipe Nav — seret `<main>` ke subtopik sebelum/selepas

`assets/js/main.js` (blok "SWIPE NAV") seret `main.note-reading-main`
ikut jari secara langsung (`transform: translateX()`, 1:1, TIADA
`requestAnimationFrame` — pembalut rAF pernah cuba tapi cetus race:
touchmove seterusnya boleh batal rAF tertunda sebelum sempat render,
transform kekal `0px` walau dah seret jauh, disahkan via ujian
Playwright) semasa gerak isyarat aktif, snap/navigasi lepas lepas jari
— diinspirasi carousel scroll-snap `idariq-system/src/App.jsx`, tapi
diselaraskan utk ZymNotes: setiap subtopik fail HTML BERASINGAN
(bukan pane SPA), jadi tiada carousel track/pratonton sebenar — hanya
`<main>` semasa diseret, lepas commit terus `window.location.href`.

**AWAS — `.js-enhanced main { animation: hz-page-in ... both; }`
(base.css) "pegang" `transform` scr kekal** (animation menang drpd
inline style dlm cascade CSS, walau lepas animasi tamat, sbb
`fill-mode: both`) — `beginDrag()` MESTI set `main.style.animation =
"none"` sebelum cuba tulis `transform` inline, jika tidak seretan
takkan kelihatan langsung (transform inline "kalah" senyap, tiada
ralat console). Ni PUNCA SEBENAR bug awal semasa bina ciri ni (bukan
isu rAF/timing spt disyaki mula-mula).

**AWAS — sejarah `layout.css` catat**: "Page transition animation
removed — it caused stacking context / compositing bugs on mobile
that broke accordion panel rendering." (komen baris 1, sejak fail ni
dipisah PR #507). Animasi transisi HALAMAN PENUH (site-wide, setiap
navigasi) yg dimaksudkan tu BEZA skop drpd ciri swipe ni (transform
hanya aktif SEMENTARA drpd gerak isyarat, bukan kekal), tapi mekanisme
risiko SAMA (transform pd `<main>` cipta stacking context baharu utk
semua descendant, boleh pecahkan `position: fixed` bersarang/
z-index). Disahkan (Playwright, seret aktif + settle-back +
functional re-check) TIADA kerosakan render accordion setakat ni —
sebabnya semua UI `position: fixed` (FAB sparkle, sheet tetapan,
toast, overlay) SENGAJA dilekap pd `document.body` terus (bukan dlm
`<main>`), bukan kebetulan. **JANGAN lekap UI fixed baharu dlm
`<main>`** — kekalkan konvensyen `document.body.appendChild(...)` sedia
ada, jika tidak berisiko hidupkan semula bug sejarah ni.

**Skop: SEMUA halaman `notes/*.html` yg ada nav bawah** (subtopik +
ringkasan bab) — swipe-nav TIDAK digerbangkan ikut fail/kelas body,
cuma bergantung pd wujud `.note-subsection .hero-actions` dlm DOM,
jadi automatik aktif di mana-mana pautan Kembali/Seterusnya wujud
(main.js dikongsi semua halaman). `notes/index.html` (senarai bab,
tiada `<main class="note-reading-main">`) & `quiz/*.html` (tiada
`.note-subsection`) automatik TAK aktif.

**Nyahaktif zoom (pinch + double-tap) TERIKAT kpd syarat aktif SAMA**
(dlm blok IIFE swipe-nav, lepas confirm `prevHref`/`nextHref` wujud),
BUKAN kelas body — cubaan awal guna rule CSS
`body.note-reading-app:not(.quiz-page)` TERLEPAS halaman ringkasan bab
(`body.bab-hub-page`, kelas body BERBEZA drpd halaman subtopik
`body.note-reading-app`, walhal dua-dua ada nav bawah & patut
nyahaktif zoom). **JANGAN kembali guna rule CSS berasaskan kelas body
utk ni** — akan tak segerak semula drpd syarat sebenar bila struktur
halaman berubah.

**TIGA lapisan nyahaktif zoom** (satu lapisan sahaja — touch-action +
gesturestart — TERBUKTI TAK CUKUP, pengguna masih boleh pinch;
disahkan perlu tambah lapisan ketiga):
1. `touch-action: pan-x pan-y` pd `document.documentElement` DAN
   `document.body` (CSS piawai, TAK diabaikan spt meta viewport).
2. Listener `gesturestart/change/end` (event proprietari WebKit) +
   `preventDefault()` — tambahan Safari/WebKit lama.
3. **Listener `touchmove` SEJAGAT (`document`), `preventDefault()`
   bila `ev.touches.length > 1`** — teknik JS PALING dipercayai
   merentas pelayar (Android Chrome DAN iOS Safari), tak bergantung pd
   sokongan `touch-action` pelayar. Lapisan PALING penting/robust drpd
   tiga-tiga — jangan buang walau nampak berlebihan drpd lapisan 1&2.

Meta viewport (`maximum-scale=1.0, user-scalable=no`) turut ditambah
pd semua halaman berkenaan sbg petunjuk sekunder (Android Chrome
lama), tapi Safari iOS 10+ sengaja ABAIKAN atribut meta tu utk
kebolehcapaian (a11y) — JANGAN bergantung padanya sahaja, tiga lapisan
JS/CSS di atas ialah mekanisme SEBENAR.

**Swipe TIADA pengecualian elemen interaktif** (a/button/kad
subtopik/pencetus accordion) di `touchstart` — cubaan awal kecualikan
elemen ni (elak konflik dgn klik/tap normal) sebenarnya PECAHKAN ciri
sepenuhnya pd halaman ringkasan bab (`bab-N.html`), sbb halaman tu
hampir sepenuhnya kad & accordion — nyaris tiada "ruang kosong" utk
mula swipe. Axis-lock (`AXIS_LOCK_DISTANCE`, 8px) + `preventDefault()`
HANYA dipanggil bila `phase === "dragging"` (bukan di `touchstart`)
dah cukup bezakan tap tulen (gerakan kecil, `preventDefault` tak
pernah dipanggil, klik/tap asli jalan spt biasa) drpd swipe sebenar
(gerakan mendatar ketara, `preventDefault` sekat klik asli & navigasi
guna logik seret sebaliknya) — disahkan Playwright (`.tap()` native
pd kad subtopik & pencetus accordion kekal berfungsi normal; swipe
mendatar bermula drpd atas kad/accordion yg sama BETUL navigasi ke
halaman sebelah, bukan ikut href kad tu).

## Glosari Popover — kad "Glosari" digantikan popover (prototaip)

`assets/js/main.js` (blok "GLOSARI POPOVER") jana popover kecil drpd
kad `.glossary-paper` sedia ada (bukan struktur HTML baharu) —
diinspirasi perbincangan "Info box → popover" awal, tapi dipakai pd
glosari sbb definisi glosari pendek (1 ayat) & dah ada titik cetus
semula jadi (istilah `.kw` dlm ayat).

**Logik (per kad `.glossary-paper`)**: ambil istilah (teks span `.kw`
pertama dlm `.point-line` kad) + definisi penuh (teks `.point-line`).
Cari calon PERTAMA (ikut susunan DOKUMEN — `querySelectorAll(".kw,
.paper-strip.strip-sub")` jamin susunan dokumen walau selector
gabungan) di LUAR `.glossary-paper`, `.lead` (intro hero) &
`.master-summary-paper` (meliputi "Ringkasan X.X" & "Rumusan Besar
Bab N" — sama kelas) — arahan pengguna: kemunculan di intro/ringkasan
TAK dikira, sbb bahagian tu selalu dibaca berulang, trigger di situ
kurang berguna drpd dlm kandungan penuh. DUA jenis calon disemak
serentak (satu senarai tersusun, mana jumpa dulu menang):
- **Span `.kw`** — padanan TEPAT (case-insensitive) teks penuh span.
- **Tajuk seksyen `.paper-strip.strip-sub`** — padanan SEBAHAGIAN
  teks (case-insensitive `indexOf`), sbb istilah selalunya sbhg drpd
  tajuk lebih panjang (cth. "Kuasa Imperialis" dlm tajuk "A.
  Persaingan Kuasa Imperialis") — BUKAN span `.kw` berasingan.
  `wrapTermInHeading()` cari nod teks dlm tajuk yg mengandungi
  istilah, PECAHKAN kpd 3 (sebelum/padanan/selepas), bungkus HANYA
  bahagian padanan dgn `<span class="kw-glossary-trigger">` baharu
  (guna `document.createDocumentFragment()`, gantikan nod teks asal
  via `replaceChild`) — teks lain (cth. "A. Persaingan ") KEKAL di
  luar span, tak terjejas.

Kalau jumpa (mana-mana jenis): tanda `.kw-glossary-trigger` +
`tabindex`/`role=button` (klik/Enter/Space buka popover, dicetus drpd
`document.body.appendChild`, kedudukan dikira drpd
`getBoundingClientRect()` + clamp tepi viewport), kad asal
`display:none`. **Kalau TAK jumpa** (istilah tu tak muncul di
mana-mana selain intro/ringkasan/kad glosari sendiri), kad asal
DIKEKALKAN tanpa transformasi — degradasi selamat, bukan ralat.

Popover sendiri ada 2 bahagian (`showPopover()` bina via
`document.createElement`/`appendChild`, bukan `innerHTML` — konsisten
dgn corak sedia ada codebase ni): tajuk mini `.kw-glossary-popover-head`
(ikon 3D "Open book" Fluent + label "Glosari", padanan visual dgn
`.paper-strip.strip-glossary` asal — gradien ungu, `keywords.css`) +
badan `.kw-glossary-popover-body` (teks definisi). Ditambah selepas
pengguna minta popover "ada tajuk glosari dan ikon macam sebelum ini"
supaya kekal konsisten dgn identiti kad asal yg digantikan.

**AWAS — JANGAN tambah listener `scroll` utk tutup popover.**
Trigger ada `tabindex="0"`; klik sebenar (Playwright `.click()`,
jenis sama dgn tap peranti sebenar) bagi FOKUS asli pd elemen, yg
kadang cetus pelayar auto-scroll SEDIKIT (bawa elemen fokus dlm
pandangan penuh) SEBAIK SAHAJA popover terbuka. Scroll asal pelayar
tu (bukan gerakan tatal pengguna) akan tutup popover SERTA-MERTA
dlm gerakan yg SAMA — bermakna popover kelihatan terbuka+tertutup
serentak, tak pernah nampak langsung. Ni bug SEBENAR (bukan artifak
ujian) ditemui semasa bina — disahkan via Playwright `.click()`
(bukan `dispatchEvent` sintetik, yg TAK cetus fokus/scroll natif jadi
tersembunyi drpd ujian sintetik awal). Klik-luar & Escape dah cukup
utk tutup, tak perlukan scroll-close.

**AWAS — kedudukan/lebar popover kena ukur via `offsetWidth`/
`offsetHeight`, BUKAN `getBoundingClientRect()`.** Popover ada animasi
masuk CSS (`kw-glossary-pop-in`, `scale(0.96)→scale(1)`) — panggilan
`getBoundingClientRect()` sejurus lepas `appendChild` berlaku SEMASA
animasi tu MASIH berjalan (transform belum sampai `scale(1)`), jadi
lebar/tinggi yg diukur SEDIKIT terkurang drpd saiz sebenar akhir.
Kiraan `maxLeft`/kedudukan tepi guna nilai "kurang tepat" tu punca
BUG SEBENAR dilaporkan pengguna: popover nampak "terlalu lebar dan
keluar dari kad utama" (bocor ke ruang kelabu sisi) — sbb kedudukan
`left` dikira drpd lebar-semasa-animasi yg lebih kecil drpd lebar
akhir, jadi selepas animasi selesai (kembali ke saiz penuh), tepi
kanan popover melangkaui tepi kad. Fix: `el.offsetWidth`/
`el.offsetHeight` (layout box, TAK terjejas `transform`) utk ukur
saiz, `getBoundingClientRect()` kekal utk KEDUDUKAN pencetus (elemen
biasa, tiada animasi). Popover juga kini clamp lebar/kedudukan kpd
KAD INDUK (`.paper-board`/`.paper-flap-card`/`.cv-unit` via
`.closest()`), bukan viewport penuh — sebelum ni `max-width:
min(320px, 100vw-24px)` boleh jadi lebih lebar drpd kad yg
mengandungi pencetus (terutama kad sempit di tengah senarai kad).

**Mod fokus (scrim + klon terapung)** — lepas laporan pengguna popover
"kelihatan agak padat" pd halaman berkandungan banyak, `showPopover()`
kini juga: (1) cipta `.kw-glossary-scrim` (`position:fixed; inset:0`,
latar gelap lutsinar + `backdrop-filter: blur(2px)` ringan) menutup
SELURUH viewport termasuk header/nav bawah/FAB — pudarkan semuanya
KECUALI istilah yg ditekan & popover; (2) cipta `.kw-glossary-clone`
— SATU SALINAN nod istilah asal (`trigger.cloneNode(true)`),
`position:fixed` terapung DI ATAS scrim pd kedudukan/saiz sama persis
dgn istilah asal (`getBoundingClientRect()`), supaya kelihatan JELAS
walau istilah SEBENAR (di dlm `<main>`) turut terlindung/pudar oleh
scrim.

**KENAPA klon, bukan naikkan istilah SEBENAR guna z-index sahaja**:
`<main class="note-reading-main">` (base.css, `.js-enhanced main {
animation: hz-page-in ... both; }`) SUDAH bentuk stacking context
sendiri (mana-mana elemen dgn `animation` yg berpotensi jejas
opacity/transform automatik bentuk stacking context baharu, spt
dijelaskan §"Swipe Nav" di atas). Ini bermakna z-index MANA-MANA anak
di dlm `<main>` HANYA bersaing dlm stacking context tempatan tu —
`<main>` itu sendiri (kotak keseluruhan, `position:static`) sentiasa
dilukis PADA tahap "kandungan susunan-dokumen" drpd `<body>`
(SEBELUM/DI BAWAH mana-mana anak `<body>` yg positioned+z-index
positif, spt scrim kita), tak kira nilai z-index anak dlm-dalamannya.
Jadi istilah asal TAK PERNAH boleh dinaikkan atas scrim ni via
z-index — SATU-SATUNYA cara "kelihatan jelas" ialah salinan berasingan
yg dilekat TERUS pd `<body>` (di luar `<main>`), sama corak dgn
keperluan sedia ada "semua UI `position:fixed` MESTI dilekat pd
`document.body`" (§"Swipe Nav").

**Gaya klon**: disalin drpd `getComputedStyle(trigger)` (bukan warisi
semula drpd konteks `<body>` baharu) utk `fontSize`/`fontWeight`/
`color`/`backgroundColor`/`padding`/dll. — elak "font-size: inherit"
(`.kw`, keywords.css) tersasar kpd saiz asas `<body>` bukan saiz
sebenar dlm perenggan/tajuk asal. Klon `pointer-events:none` (murni
visual, ketukan di situ jatuh terus ke scrim di bawahnya → tutup
popover, sama spt ketukan di luar) + `aria-hidden="true"` (elak
pembaca skrin umum dua kali — elemen ASAL kekal dlm DOM utk
keakksesan, klon murni visual).

**AWAS — istilah dlm TAJUK (`.paper-strip.strip-sub`, substring wrap
via `wrapTermInHeading`) PERLUKAN latar cip fallback, span `.kw`
TIDAK.** Span `.kw` (cth. "Deklarasi 14 Perkara") dah ada latar warna
sendiri drpd kelas `kw-*` (keywords.css) — cukup jelas terapung atas
scrim tanpa apa-apa tambahan. TAPI istilah dlm tajuk (cth. "Kuasa
Imperialis" dlm "A. Persaingan Kuasa Imperialis") ialah span POLOS
TIADA latar sendiri — warna latar yg nampak sebelum ni datang drpd
GRADIEN TAJUK INDUK (`.paper-strip.strip-sub`), bukan span tu sendiri.
Bila diklon berasingan drpd tajuk (`getComputedStyle().backgroundColor`
= `rgba(0, 0, 0, 0)`), teks jadi HAMPIR TAK JELAS atas scrim gelap
(warna teks gelap dirancang utk latar TERANG asal, kontra lemah atas
scrim) — dilaporkan pengguna dgn tangkapan skrin: "perkataan yang
berada di tajuk masih tak jelas". Fix: semak
`triggerStyle.backgroundColor` — kalau `rgba(0, 0, 0, 0)`/`transparent`
(tiada latar sendiri), beri latar cip fallback (`var(--paper)` + sedikit
padding/border-radius/shadow, PADANAN gaya cip `.kw` semula jadi) pd
klon SAHAJA (bukan istilah asal). Padding baharu tu "dibayar balik" via
`offsetX`/`offsetY` (kurangkan drpd `left`/`top`) supaya TEKS kekal pd
kedudukan asal — kotak klon tumbuh KE LUAR, bukan teks tersasar.

**Istilah dlm ACCORDION TERTUTUP — TAK diskip, berfungsi dgn betul.**
Carian calon (`.kw`, `.paper-strip.strip-sub`) sejagat merentas SELURUH
DOM tanpa kira status buka/tutup accordion (`.paper-accordion-panel`
guna `max-height:0; overflow:hidden` bila tertutup — BUKAN
`display:none` — jadi `querySelectorAll` tetap jumpa, `getBoundingClientRect()`
tetap sah). Disahkan empirik: 6 drpd 23 halaman ada pencetus di dlm
accordion tertutup lalai (`bab-2-4` "Isu Kasut" — jenis tajuk pula,
`bab-3-2` "enakmen", `bab-3-3` "Blitzkrieg", `bab-3-8` "Kakeo Kokokai",
`bab-5-1` "hartal", `bab-5-2` "dekolonisasi") — diuji ALIRAN SEBENAR
pengguna (buka accordion DULU, br klik pencetus) utk kedua-dua
"hartal" & "Isu Kasut" (gabungan tajuk+accordion), scrim+klon+popover
semua betul. (Nota ujian: klik SINTETIK pd pencetus SEBELUM accordion
dibuka turut "berjaya" via Playwright kerana `getBoundingClientRect()`
elemen di dlm panel `overflow:hidden` tetap pulangkan geometri sah —
tapi ni BUKAN aliran sebenar pengguna, sbb pencetus scr visual tak
boleh dicapai/tekan sehingga accordion dibuka dulu; tak perlu risau.)

Popover sendiri turut ditukar drpd `position:absolute` (+ `scrollY`)
kpd `position:fixed` (kedudukan terus drpd `getBoundingClientRect()`,
tiada `scrollY` lagi) — konsisten dgn scrim+klon yg turut `fixed`,
supaya keseluruhan "mod fokus" kekal terkunci pd viewport (bukan
hanyut ikut tatal halaman di sebalik scrim).

`display:none` (bukan buang drpd DOM) SENGAJA — disahkan penjana PDF
(`_bodyHtml` dlm main.js) berjalan berasaskan struktur DOM/kelas
(`el.childNodes.forEach`), TIADA semakan `display`/visibility, jadi
kandungan kad tetap disertakan dlm eksport PDF walau disembunyi drpd
paparan biasa.

**Skop: SELURUH LAMAN** (semua halaman `notes/*.html` yg ada
`.glossary-paper` — 23 halaman, 40 kad glosari kesemuanya). Prototaip
asal dibina & disahkan di `bab-3-2.html` sahaja (keempat-empat istilah
glosari halaman tu dpt popover — "Kuasa Imperialis" & "Pakatan
Ketenteraan" via tajuk seksyen `.paper-strip.strip-sub`, "Deklarasi 14
Perkara" via span `.kw` dlm perenggan penjelasan, "Enakmen" via span
`.kw kw-istilah` ditambah pd ayat "British turut meluluskan tiga
enakmen penting semasa perang:" khusus utk beri kemunculan sah drpd
kad glosarinya). Logiknya sendiri SUDAH sejagat drpd awal (`main.js`
dikongsi SEMUA halaman, `querySelectorAll(".glossary-paper")` tak
terikat halaman tertentu) — "luaskan" bermakna SAHKAN ia berfungsi
betul merentas kesemua 23 halaman, bukan tulis kod baharu. Disahkan
via Playwright (audit automatik semua 23 halaman): 10/40 kad dpt
popover (label jalur SEBENAR "Glosari" + kemunculan sah drpd kad
glosari sendiri), 30/40 kekal kad asal (degradasi selamat ATAU bukan
kad "Glosari" sebenar — lihat "Penapis label" di bawah), SIFAR ralat
JS, kiraan `trigger + kad-kekal = jumlah-kad` KONSISTEN pd SETIAP
halaman, setiap halaman berpencetus diuji buka+tutup penuh (scrim+
klon+popover) berjaya.

**Nota**: `.glossary-paper`/`.paper-strip.strip-glossary` TAK semestinya
bermaksud kad "istilah: definisi" ringkas spt bab-3-2.html — cth.
`bab-1-1.html` ada kad `.glossary-paper` berlabel "Info Tambahan"
(pecahan makna kata, cth. "Sri = bercahaya" + "Vijaya = kemenangan")
dgn struktur berbeza (span `.kw` PERTAMA dlm `.point-line` ialah FRASA
definisi itu sendiri, bukan nama istilah). Degradasi selamat sedia ada
(pencarian gagal jumpa kemunculan lain drpd frasa panjang tu) sudah
kendalikan kes ni betul TANPA kod tambahan — kad kekal kad asal
sepenuhnya, tiada ralat. JANGAN anggap semua `.glossary-paper` sama
bentuk bila debug/kembangkan ciri ni lagi.

**Penapis label — WAJIB semak teks jalur SEBENAR sebelum popover-kan
kad, popover PAPAR LABEL+IKON SEBENAR kad (bukan hardcode "Glosari").**
Kelas CSS `.glossary-paper`/`.strip-glossary` (gaya jalur ungu + ikon)
DIKONGSI SEMULA merentas laman utk PELBAGAI jenis kad kandungan, bukan
eksklusif definisi istilah — disahkan via audit teks jalur SEBENAR +
kandungan PENUH (semua `.point-line`, bukan cuma yg pertama) pd
kesemua 40 kad: label sebenar termasuk "Glosari" (10 kad — definisi
istilah tulen), "Info" (14 kad — CAMPURAN fakta tunggal berdiri
sendiri DAN pengenalan senarai/chip-list berasingan), "Info Tambahan"/
"Info Penting"/"Petikan Penting"/"Petikan Surat..." /tajuk custom cth.
"Rayuan Anthony Brooke" (16 kad — naratif berbilang ayat/petikan/
senarai bergantung chip-list).

Versi awal ciri ni (PR #529–532) popover-kan SEBARANG kad
`.glossary-paper` (tanpa semak label) drpd hanya kewujudan span `.kw`
PERTAMA dlm `.point-line` — dilaporkan pengguna dgn tangkapan skrin
("Isu Kasut"/"Anthony Brooke" muncul dgn tajuk popover "Glosari"
walhal BUKAN takrifan istilah). PR #534 (fix pertama) MENGETATKAN
kpd label EXACT "Glosari" sahaja (10/40) — TERLALU KETAT, buang
kad "Info" yg sebenarnya SESUAI (cth. "Isu Kasut", "Hartal" — format
sama spt Glosari: "Subjek ialah/→ penerangan", cuma label berbeza).
Pengguna minta kajian semula: "sebahagian bukan glosari juga sesuai
dijadikan popover dengan label yang betul".

**Peraturan KELAYAKAN semasa** (`glossaryCards.forEach`,
`assets/js/main.js`) — DUA syarat, kedua-dua MESTI lulus:
1. Label jalur SEBENAR (`.paper-strip.strip-glossary` textContent)
   MESTI "Glosari" ATAU "Info" (exact match) — label lain (Info
   Tambahan/Info Penting/Petikan.../tajuk custom) `return` awal,
   TIADA pengecualian (disahkan via kajian: SEMUA contoh label lain
   ni ialah naratif/petikan/senarai bergantung chip-list, tiada
   satu pun kad fakta tunggal berdiri sendiri).
2. Teks `.point-line` PERTAMA (bakal jadi `defText` popover) TAK
   BOLEH tamat dgn `:` (regex `/:\s*$/`) — tanda ayat tu cuma
   PENGENALAN kpd senarai/chip-list BERASINGAN yg TAK disertakan dlm
   popover (popover guna SATU `.point-line` sahaja); disahkan
   merentas SEMUA 40 kad — corak ni 100% membezakan "fakta tunggal
   berdiri sendiri" (tamat `.`) drpd "pengenalan senarai" (tamat `:`)
   tanpa kecuali, termasuk dlm kad berlabel "Info" yg CAMPURAN
   kedua-dua jenis (cth. bab-5-1.html ada 4 kad label "Info" — 2
   fakta tunggal LULUS penapis [Persekutuan, Hartal], 2 pengenalan
   senarai DITAPIS [Istilah radikal, protes]).

Popover kini papar LABEL+IKON kad SUMBER SEBENAR (bukan hardcode) —
`showPopover(trigger, defText, labelText, iconSrc)` terima parameter
baharu, `iconSrc` diambil terus drpd `stripEl.querySelector("img").src`
kad sumber (cth. kad "Info" guna ikon "Magnifying glass tilted left"
🔍, BUKAN ikon buku 📖 "Glosari") — popover jadi JUJUR cerminkan jenis
kandungan sebenar, bukan panggil semuanya "Glosari".

**Hasil semasa: 12/40 kad dpt popover** (10 "Glosari" + 2 "Info" lulus
kedua-dua syarat: `bab-2-4` "Isu Kasut", `bab-5-1` "hartal"). Nota:
sesetengah kad "Info" yg LULUS penapis label+tanda ayat (cth.
"Golongan Mandarin", "Persekutuan", "Teluk Intan") TETAP kekal kad
asal — BUKAN sbb ditapis di sini, tapi sbb mekanisme SEDIA ADA
("cari kemunculan sah calon SELAIN kad glosari sendiri" — lihat
bahagian atas) gagal jumpa kemunculan lain istilah tu di luar kad
sendiri (degradasi selamat, tiada kaitan dgn fix ni).

## Aliran Kerja Versioning Aset (WAJIB lepas ubah CSS/JS/sw.js)

Sumber kebenaran versi: `data/asset-versions.json`. Lepas ubah
mana-mana `assets/css/*.css`, `assets/js/*.js`, `sw.js`,
`offline.html`, atau `manifest.json`:

```bash
python3 scripts/bump-versions.py --files <fail-yg-berubah>
python3 scripts/sync-asset-versions.py
```

Ini bump nombor versi berkaitan (cth. `main_js`, `sw_cache`) &
propagate `?v=N` ke semua rujukan HTML + `CACHE` const dlm `sw.js` +
`navigator.serviceWorker.register()` dlm `main.js`. Terlupa langkah ni
= cache browser tak invalidate = pengguna dapat aset lapuk. Ada
`.githooks/pre-commit` yg auto-jalankan skrip ni utk fail staged
(install sekali: `git config core.hooksPath .githooks`), tapi dlm sesi
agen (clone segar, hooks tak configured), jalankan skrip di atas
SECARA MANUAL sebelum commit.

## Semakan Sebelum Commit

- `python3 scripts/seo-audit.py` — audit meta tags/struktur SEO
  merentas semua halaman (mesti "passed"). Jalankan CI (`seo-audit.yml`)
  pada setiap PR/push ke `main` jugak.
- `npm run lint` (ESLint utk `assets/js/*.js`/`sw.js`/`scripts/*.mjs`,
  Stylelint utk `assets/css/*.css`) — gate CI (`lint.yml`). Konfig
  SENGAJA longgar (`eslint:recommended` + `stylelint-config-recommended`,
  bukan `standard`) supaya tangkap ralat sebenar (var tak wujud, CSS tak
  sah, dll.) tanpa paksa tulis semula 11k+ baris CSS/JS sedia ada dgn
  peraturan gaya. `no-unused-vars` sengaja "warn" (bukan "error") —
  byk fungsi/param sedia ada memang unused (kod dead/reserved), tak
  patut block PR. Tiada test framework — sahkan perubahan JS/HTML lain
  scr manual (baca diff, run local server bila perlu:
  `python3 -m http.server 8080`).
- Elak edit terus `data/updates.json` & `sitemap.xml` — dijana automatik
  oleh workflow `update-status.yml` (`scripts/generate-updates.py`) bila
  push ke `main`; perubahan tangan akan overridden/conflict.

## Mod Bahasa Cina (ZH Mode)

Kandungan dwibahasa (`data/zh-units/`, `data/zh-glossary.json`) ada
garis panduan editorial khusus — rujuk `docs/zh-mode-editorial-guideline.md`
& `docs/zh-glossary-editorial-guideline.md` SEBELUM ubah istilah/unit ZH.
Skrip audit (`scripts/check-zh-*.py`, `scripts/audit-zh-units.mjs`) wujud
utk sahkan liputan & konsistensi istilah — jalankan lepas ubah data ZH.

## Bahasa

Tulis commit message, dokumentasi, & balasan dlm **Bahasa Melayu**
(konvensyen sedia ada — README, docs/, & semua commit history repo ni
dlm BM).

## Cawangan & PR

Repo ni guna satu cabang produksi (`main`, deploy terus via GitHub
Pages) — tiada aliran staging/main berasingan macam projek Vercel lain
dlm ekosistem Idariq. Kerja pada cabang berasingan & push macam biasa;
JANGAN auto-cipta PR selepas push melainkan diminta eksplisit (beza
drpd repo `idariq-system` yg ada automasi PR→staging tersendiri).
