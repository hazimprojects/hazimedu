# ZymNotes — Panduan Agen

Laman statik (HTML/CSS/JS vanilla, tiada framework/build step JS) untuk nota
ulang kaji KSSM pelajar Malaysia. Deploy ke GitHub Pages (domain custom
`zymnotes.com` via `CNAME`, `.nojekyll` — serve terus dari root repo, `docs/`
bukan folder Pages, ia dokumentasi dalaman). Rujuk `README.md` untuk
senarai ciri & struktur penuh — fail ni fokus pada apa yang perlu tahu
supaya tak tersalah anggap senibina sedia ada.

**Fail ni ringkas drpd asal (2026-08-14) — 3 topik paling besar/kompleks
dipecah ke `docs/` (rekod penuh punca/fix/pengesahan setiap pepijat),
fail ni kekal ringkasan AWAS kritikal + pautan:**
`docs/pdf-export-engineering.md` (eksport & pratonton PDF),
`docs/infographic-gallery.md` (galeri infografik/teaser SEO/FAB Suka),
`docs/country-flags.md` (bendera negara). Baca fail berkaitan PENUH
sebelum ubah kod dlm skop tu — ringkasan dlm `CLAUDE.md` cukup utk
elak silap biasa, tapi bukan pengganti konteks penuh.

## Fokus Semasa

**Kemas kini (2026-08-11): sekatan lama di bawah DIMANSUHKAN.** Kandungan
sedia ada (Bab 1–10 Sejarah T4, sistem kuiz, eksport PDF, dll.) kini
dianggap cukup stabil oleh pengguna. `docs/project-strengths-audit.md`
sebelum ni catat "cadangan ciri baharu ditutup sementara" — status tu
tak lagi berkuat kuasa. Boleh cadang & bina ciri baharu (cth. gambar/
peta sejarah bercerita — dibincang eksplisit, belum dilaksana lagi,
rujuk isu lesen/self-hosting/PDF sebelum mula) secara proaktif bila
nampak bernilai, bukan sekadar tunggu diminta.

Walau begitu, disiplin sedia ada dlm fail ni KEKAL wajib utk ciri
baharu jugak — bukan lesen utk kurangkan ketelitian: sahkan ikon/aset
baharu benar2 berfungsi sebelum push (§"Ikon Emoji"), uji via
Playwright sebelum ship (bukan teka drpd CSS/kod semata), ikut
struktur HTML/kelas kata kunci kanonik sedia ada, kemas kini
dokumentasi (fail ni) bila corak baharu diperkenal, & jalankan
semakan penuh (`seo-audit.py`, `check-zh-coverage.py`, `npm run lint`)
sebelum commit.

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

**AWAS — laluan ikon dlm `scripts/emoji_map.py` BUKAN bukti ia
berfungsi.** Sekurang-kurangnya satu kunci (`"building"` →
`Building/3D/building_3d.png`) didapati PECAH di CDN sebenar walaupun
"betul" ikut fail tu — hanya ketara selepas PR dah merge, drpd
screenshot pengguna nampak ikon kosong. **Sebelum guna laluan ikon
BAHARU (belum pernah dipakai) dlm kandungan**, sahkan ia benar-benar
berfungsi via salah satu:
- `grep -rl --include=*.html -F "<laluan-penuh-ikon>" notes/` dan
  pastikan COUNT > 0 (ikon tu dah dipakai & render betul di halaman
  lain yg dah live) — cara paling pantas & selamat.
- Kalau ikon betul-betul baharu (tiada di mana-mana lagi), sahkan
  wujud terus di CDN sebelum commit (cth. `curl -sI` URL penuh, jangkakan
  `200`) — JANGAN percaya sahaja ejaan/format nama dlm `emoji_map.py`.

**AWAS — nama fail ikon majmuk KEKALKAN sengkang, jangan tukar semua
ke underscore bila jana laluan secara program.** Skrip `slugify()`
ringkas (`name.replace('-', '_')`) pecahkan nama fail spt
`globe_showing_asia-australia_3d.png` (BUKAN `..._asia_australia_...`)
& `globe_showing_europe-africa_3d.png` (BUKAN `..._europe_africa_...`)
— sengkang dlm "asia-australia"/"europe-africa" KEKAL sebahagian nama
fail SEBENAR CDN, bukan pemisah perkataan spt "%20" utk ruang. Kalau
jana laluan ikon secara program (bukan taip manual), SENTIASA sahkan
laluan yg terhasil (grep count>0 §atas) sebelum push — 3 laluan pecah
camni ditemui & dibetulkan lepas jana 70 ikon baharu secara pukal
(rujuk PR "Tambah ikon tema kedua yg hilang pd 70 item Fokus X.Y").

## Bendera Negara — self-hosted (`assets/flags/`), BUKAN CDN luar

Fluent Emoji (pembekal ikon utama) sengaja TIADA bendera negara. Pembekal
rasmi ZymNotes ialah **`circle-flags`** (MIT, SVG bulat) — **self-hosted**
dlm `assets/flags/<kod-iso2>.svg` (BUKAN CDN luar, sbb (1) sandbox/rangkaian
tertentu sekat domain baharu, (2) elak isu offline-cache, (3) set kecil &
tetap). Kelas `.flag-icon` (`fluent-shell-emoji.css`) SENTIASA digunakan
BERSAMA `fluent-3d-emoji openmoji--inline` (bukan ganti).

**Skop semasa: 46 negara** (rujuk `assets/flags/`) merentas 14+ halaman —
chip (`.paper-chip`), kad kingdom bernombor keycap (`.paper-kingdom`),
item accordion (`.paper-accordion-item`/`.paper-accordion-no`), &
point-heading/point-line yg namakan SATU negara berdaulat sbg fokus.

**WAJIB tanya user dulu (`AskUserQuestion`) sebelum tambah bendera pd
entiti berikut** — bukan keputusan mekanikal:
- Czechoslovakia, Yugoslavia (dah pupus, >2 negara pengganti, tiada 1
  bendera "betul").
- Manchuria, Hong Kong (bukan negara berdaulat — negara boneka/jajahan).
- Korea era 1910-an (berpecah 2 negara moden sejak 1948) — user PERNAH
  ditanya & pilih tambah `kr.svg` sbg rujukan lazim, tapi kes serupa
  akan datang KEKAL perlu tanya, bukan auto-guna keputusan lama.
- Chip di mana negara sekadar PENYERANG/aktor sepintas lalu dlm naratif
  TEMPATAN kita (cth. "Serangan Jepun terhadap Negara Kita") — KEKAL
  DIKECUALIKAN (fokus naratif tetap Malaysia/tempatan, bukan negara asing).

4 entiti dikecualikan (Czechoslovakia/Yugoslavia/Manchuria/Hong Kong) guna
SATU lencana glob generik (kunci `"globe"` dlm `emoji_map.py`) + kelas
`.flag-icon` supaya ritma visual konsisten tanpa palsukan makna "negara
berdaulat".

**Hanya** ganti/tambah ikon pd teks yg **tepat** nama negara atau
"NEGARA – ringkasan pendek" — JANGAN pd ayat prosa yg sekadar SEBUT nama
negara di tengah (cth. "British bertindak mengekang..."). Ikon 🌐
"Globe with meridians" KEKAL generik utk label >1 negara/istilah
abstrak/komuniti etnik dlm Tanah Melayu/deskriptor bahasa — bukan semua
🌐 patut ditukar bendera, semak konteks case-by-case.

Rekod penuh (setiap pusingan audit, 89→66 kejadian 🌐 diklasifikasi,
senarai lengkap fail/chip diedit): **`docs/country-flags.md`**.

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

## Struktur Kandungan — Kad "Kesimpulan" & "Rumusan Besar Bab N"

**Kad "Kesimpulan" setiap subtopik (`class="paper-board summary-paper
conclusion-paper cv-unit"`) WAJIB ada `paper-chip-list`, bukan cuma
ayat `point-line` berturutan.** Corak piawai (disahkan konsisten di
36/39 subtopik Bab 1–7 semasa audit; Bab 7.1–7.4 & Bab 8.1–8.4 dulu
tersasar drpd corak ni sebelum dibetulkan — rujuk PR "Selaraskan
konsistensi visual & struktur kad Kesimpulan Bab 7 & Bab 8"):

1. 1 ayat pembuka (`point-line`) diakhiri `:` merumus pencapaian/kesan
   topik tersebut.
2. `paper-chip-list` — 2–3 chip PENDEK (frasa, bukan ayat penuh),
   ambil drpd fakta/statistik yg SUDAH tertulis dlm Bahagian
   sebelumnya pd halaman sama (bukan kandungan baharu, sekadar
   pecahan visual poin sedia ada).
3. 1–2 ayat penutup (`point-line`) reflektif tentang kepentingan/kesan
   lebih besar (kaitan dgn kemerdekaan, demokrasi, perpaduan, dll.).

Kad "Rumusan Besar Bab N" (`class="paper-board master-summary-paper
reveal-on-scroll cv-unit"`, ikon "Globe showing asia-australia")
ikut corak SAMA (intro + chip-list + penutup, kadang berulang
beberapa pusingan — rujuk `bab-7-5.html` utk contoh 4 pusingan), tapi
letaknya BEZA drpd Kesimpulan biasa: **hanya pada subtopik TERAKHIR
sesebuah bab** (cth. `bab-8-4.html` utk Bab 8, bukan `bab-8.html` hub),
sbg kad penutup keseluruhan bab sebelum bar navigasi akhir.

**Nota class `summary-paper`**: modifier ni SECARA VISUAL tak beri
kesan (di-override rule lebih spesifik `themes.css` — `body.note-
reading-app.page-theme-notes .paper-board`) tapi KEKALKAN dlm markup
setiap kad Kesimpulan/Rumusan Besar utk konsisten dgn corak sedia ada
merentas korpus — jangan alih keluar ikut sangkaan ia "tak berguna".

**`<h2>` "tesis" (ayat besar/tebal, child PERTAMA `.cv-unit-body`) —
WAJIB pada SEMUA kad Kesimpulan, bukan pilihan.** Selain 3 bahagian
di atas, kad Kesimpulan asal (rujuk `bab-2-2.html`, tangkapan skrin
pengguna) turut ada SATU ayat tesis besar (`<h2>`, font tebal ~21px,
warna gelap) SEBELUM ayat pembuka `point-line`/`point-heading` —
merumus keseluruhan topik dlm SATU ayat pendek. Audit dedah corak ni
TIDAK konsisten merentas bab: Bab 1 (3/4), Bab 2 (8/8) & Bab 4 (7/7)
ADA h2 tesis, tapi Bab 3, 5, 6, 7, 8, 9 (31 subtopik) LANGSUNG TIADA
— nampak spt drift bertahap (ciri asal Bab 1–2, terlepas Bab 3, muncul
semula Bab 4, hilang kekal drpd Bab 5 seterusnya) berbanding keputusan
reka bentuk sengaja. Dibetulkan (rujuk PR "Tambah h2 tesis yg hilang
pd 31 kad Kesimpulan Bab 3 & Bab 5–9") — h2 baharu dikarang berdasarkan
kandungan chip-list/point-line SEDIA ADA pd kad sama (bukan fakta
baharu), gaya sepadan contoh sedia ada (1 ayat pendek, declaratif,
~10–20 patah perkataan, diakhiri noktah).

**JANGAN tambah `data-zh-mode`/`data-zh-unit-id` pd h2 baharu** —
h2 tesis SEDIA ADA (Bab 1/2/4) guna corak BERCAMPUR (sesetengah ada
`data-zh-unit-id="bab-X-Y-orph-h2[-N]"` dgn entri JSON sepadan dlm
`data/zh-units/`, sesetengah tiada langsung, cth. `bab-1-1.html`).
H2 baharu (31 kad) SENGAJA TIADA atribut zh langsung — skrip audit
(`scripts/check-zh-coverage.py`) hanya semak elemen yg ADA
`data-zh-unit-id`, jadi elemen tanpa atribut tu automatik tak
terjejas/tak perlu liputan (disahkan 100% coverage kekal lepas
tambah 31 h2). Kalau nak tambah terjemahan ZH utk h2 baharu ni kelak,
rujuk `docs/zh-mode-editorial-guideline.md` dulu (tugas berasingan,
BUKAN sebahagian pembetulan struktur visual ni).

## Kad "Fokus X.Y" — MESTI padan bilangan & tajuk Bahagian sebenar

**Kad "Fokus X.Y" (`data-cv-title="Fokus X.Y"`, grid `compact-kingdom-
grid` berisi `.paper-kingdom` bernombor keycap) ialah PRATONTON
struktur "Bahagian Pertama/Kedua/..." halaman yg sama — bilangan &
tajuk item MESTI padan tepat dgn label `<div class="paper-label
small">Bahagian N</div>` sebenar di bawahnya.** Bila subtopik disunting
kemudian (Bahagian ditambah/digabung/disusun semula), kad Fokus SERING
"tertinggal" pd struktur lama kalau tak dikemas kini serentak — 8
subtopik (bab-2-5, bab-3-5, bab-3-7, bab-4-2, bab-4-3, bab-4-5, bab-5-1,
bab-6-3) ditemui & dibetulkan (rujuk PR "Betulkan kad Fokus X.Y yang
ketinggalan drpd Bahagian sebenar"). **Lepas sunting mana-mana Bahagian
dlm subtopik sedia ada, SENTIASA semak semula kad Fokus X.Y padanan
di atasnya** — bandingkan bilangan item & tajuk terus dgn label
Bahagian sebenar, jangan andaikan ia masih betul.

Setiap item `.paper-kingdom` dlm Fokus bernombor keycap MESTI ada
**DUA** ikon: keycap (`Keycap N`) DIIKUTI ikon tema (lepas teks) —
konsisten dgn corak "keycap + teks + ikon" merentas korpus. 70 item
di 25 fail ditemui cuma ada keycap tanpa ikon tema (pra-wujud, tak
ketara sblm pembetulan `.paper-kingdom` di bawah — rujuk PR "Tambah
ikon tema kedua yg hilang pd 70 item Fokus X.Y"). Ikon tema baharu
patut diambil (ikut keutamaan): ikon sedia ada pd tajuk "Bahagian N"
berkenaan dlm fail sama (bila item Fokus padan Bahagian), atau ikon
accordion/body berkaitan dlm fail sama, atau ikon bertema sesuai yg
disahkan wujud merentas korpus (rujuk disiplin grep §"Ikon Emoji").

**JANGAN keliru dgn corak BERBEZA** yg turut guna `.paper-kingdom`:
senarai contoh rata (cth. senarai nama kerajaan purba Funan/Champa/
Kedah Tua di bab-1-1, senarai pejuang individu di bab-2-5) SENGAJA
guna SATU ikon sahaja (ikon tema di HADAPAN teks, bukan keycap) —
bukan pecahan Bahagian bernombor, jadi tak perlu/patut ditambah ikon
kedua. Bezakan ikut: keycap-led (`Keycap N` sbg ikon PERTAMA) = perlu
2 ikon; ikon-tema-led (bukan keycap) = 1 ikon sudah betul.

**`.paper-kingdom` MESTI `flex-direction: column`** (paper.css) — row
(lalai flex) + `align-items: center` jadikan keycap/teks/ikon TIGA
item flex berasingan dlm SATU baris, so ikon terpusat MENEGAK
berbanding TINGGI KESELURUHAN baris. Utk tajuk pendek okay, tapi
tajuk panjang (item Fokus yg padan penuh tajuk Bahagian, > 1 baris)
menyebabkan ikon "terapung" di tengah paragraf (bukan di atas/lepas
teks) — pepijat visual sebenar (disahkan tangkapan skrin pengguna +
ujian layout sintetik). `flex-direction: column` betulkan (keycap
baris atas, teks tengah, ikon tema baris bawah) — JANGAN tukar balik
ke row tanpa faham sebab ni; kesan sejagat (SEMUA 45 fail guna
`.paper-kingdom`), bukan boleh disunting per-fail.

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
kedua-dua syarat: `bab-2-4` "Isu Kasut", `bab-5-1` "hartal").

**Cip mandiri (`.kw-glossary-standalone-chip`) — fallback bila TIADA
kemunculan lain di halaman langsung.** Pengguna tunjuk tangkapan skrin
kad "Golongan Mandarin" (bab-2-4.html) MASIH kad penuh walau dah lulus
penapis label+tanda ayat, minta semakan menyeluruh ("masih ada lagi
info kecil yang tak diberi popover"). Kajian PERTAMA (silap — lihat
pembetulan di bawah) sangka 7/19 kad LULUS kelayakan tapi istilahnya
tiada langsung kemunculan lain — fix asal (versi ni SUDAH DIGANTI):
GANTI kad penuh dgn CIP PADAT (`<button class="kw-glossary-standalone-chip">`)
yg jadi pencetus SENDIRI bila `!target` (tiada kemunculan lain jumpa)
— cip klik terus buka popover SAMA persis (scrim+klon+popover), guna
`activateTrigger()` fungsi SAMA yg dikongsi dgn pencetus `.kw`/tajuk
biasa. **Kod fallback cip ni KEKAL** (masih perlu utk kes SEBENAR
tiada kemunculan lain — cth. `bab-3-9` "Teluk Intan", lihat di bawah),
tapi PUNCA masalah sbnrnya BUKAN "tiada kemunculan lain" — carian
CALON asal (`.kw` + `.paper-strip.strip-sub` sahaja) TERLALU SEMPIT.

**Pembetulan (susulan)**: pengguna tunjuk BUKTI "golongan mandarin"
SEBENARNYA wujud sbg **TEKS POLOS** (bukan span `.kw`) dlm accordion
"Perubahan kepimpinan" — carian asal terlepas kemunculan ni sbb HANYA
semak `.kw` (padanan tepat) & `.paper-strip.strip-sub` (tajuk seksyen,
substring). Kajian menyeluruh (regex cari SEMUA kemunculan case-
insensitive tiap istilah, bandingkan dgn context HTML sekeliling)
dedah **6 drpd 7** kad "cip mandiri" tu SEBENARNYA ADA kemunculan
lain SAH — cuma dlm bentuk yg carian asal tak liputi: ayat biasa
(`.point-line`/`.point-heading`), tajuk accordion (`.paper-accordion-title`,
kelas BERBEZA drpd `.paper-strip.strip-sub`), & cip pendek
(`.paper-chip`, cth. `<div class="paper-chip"><img/> Giyu Gun</div>`).

**Fix (kekal)**: luaskan senarai `candidates` drpd `.kw, .paper-strip.strip-sub`
kpd `.kw, .paper-strip.strip-sub, .paper-accordion-title, .point-line,
.point-heading, .paper-chip` — SEMUA jenis SELAIN `.kw` disemak via
padanan SUBSTRING (`wrapTermInHeading()`, fungsi generik yg dah wujud
utk tajuk, kini dipakai lebih meluas — nama fungsi kekal drpd asal
tapi kini bukan khusus tajuk). **Struktur gelung diubah PENTING**:
cubaan `wrapTermInHeading()` kini berlaku SERTA-MERTA dlm gelung
(bukan lepas gelung tamat) — kalau wrap GAGAL (istilah tu SEBENARNYA
terkurung dlm span `.kw` bersarang, cth. "Persekutuan" di dlm
"Persekutuan Tanah Melayu 1948" yg dah bertag), gelung TERUS cari
calon SETERUSNYA (bukan `return`/abai terus spt versi lama) — elak
bug "textContent nampak padan tapi nod teks langsung xde padanan
sebenar (istilah tersembunyi dlm anak bersarang)". `wrapTermInHeading()`
sendiri SUDAH selamat drpd awal (cuma semak `childNodes` nodeType===3,
takkan turun ke span bersarang) — cuma gelung PANGGIL-nya yg perlu
dibetulkan supaya GAGAL SATU calon bukan bermakna GAGAL SEMUA.

**Hasil (selepas kedua-dua fix)**: 19/40 kad dpt popover (bilangan
SAMA, tapi 6/7 drpd kad tadinya guna cip mandiri kini guna teks
SEDIA ADA dlm ayat/tajuk/cip — lebih semula jadi, cip mandiri jadi
fallback TULEN bukan default). **Hanya `bab-3-9` "Teluk Intan" KEKAL
guna cip mandiri** — disahkan genuin: SATU-SATUNYA kemunculan lain
"Teluk Intan" di halaman tu (2 kali) kedua-duanya dlm `.point-line`
YG SAMA kad glosarinya sendiri (kad tu ada 4 `.point-line` — mini-
naratif), jadi TERKECUALI oleh `.closest(".glossary-paper", ...)`
sedia ada, betul-betul tiada titik lekat luar.

**Lencana ikon (`.kw-glossary-badge`) — SELEPAS pengguna nyata semua
kandungan popover BUKAN sekadar hiasan yg selamat dilangkau** (kajian
kandungan penuh 40 kad dedah kebanyakan istilah/fakta berpotensi
relevan peperiksaan, bukan trivia semata), pengguna bimbang garis
putus-putus sahaja terlalu senyap/mudah terlepas pandang, cadang
lencana ikon SELEPAS perkataan pencetus. Fix (`activateTrigger()`,
`assets/js/main.js`): tambah `<img class="kw-glossary-badge">` sbg
anak TERAKHIR setiap pencetus (guna `iconSrc` SAMA drpd label kad
sumber — buku utk "Glosari", kaca pembesar utk "Info", dll. — SAMA
ikon yg muncul di kepala popover, konsisten). Cip mandiri
(`.kw-glossary-standalone-chip`) DILANGKAU (`if
(!target.classList.contains("kw-glossary-standalone-chip"))`) sbb dah
ada ikon sendiri di HADAPAN, elak ikon berganda. CSS
(`keywords.css`): saiz `em` (bukan `px` tetap) supaya skala ikut
konteks fon (tajuk lebih besar drpd perenggan biasa),
`vertical-align: middle` (bukan `-0.05em` custom — percubaan pertama
duduk terlalu tinggi berbanding baseline teks, `middle` lebih
seimbang secara visual, disahkan via ukuran `getBoundingClientRect()`
lencana vs pencetus).

**Nota persekitaran ujian**: Playwright dlm sandbox ni TIADA akses
CDN (`cdn.jsdelivr.net` — sama isu `ERR_TUNNEL_CONNECTION_FAILED`
didokumenkan sblm ni utk semua ikon emoji laman, BUKAN isu baharu
khusus lencana ni) — imej ikon (termasuk ikon SEDIA ADA di kepala
popover) TAK boleh disahkan visual dlm sandbox, cuma geometri/DOM
(saiz kotak, kedudukan, `src` betul ikut label) boleh disahkan.
Produksi (CDN sebenar boleh dicapai) patut render normal — SAMA CDN
yg dah berfungsi utk beribu ikon lain di seluruh laman.

**Susulan — lencana ikon `.kw-glossary-badge` & cip mandiri
`.kw-glossary-standalone-chip` DIGUGURKAN drpd eksport PDF.**
Pengguna tunjuk tangkapan skrin berpasangan (pratonton PDF
`bab-3-3.html` vs laman hidup): tajuk accordion "Fasisme 📖 di Itali"
papar ikon buku lencana selepas "Fasisme" dlm KEDUA-DUA versi — betul
di laman hidup (isyarat "boleh klik, ada popover"), TAPI janggal &
tiada fungsi dlm PDF (dokumen linear, tak boleh klik). Pengguna
jelaskan definisi glosari/info dlm PDF SUDAH pun disertakan sbg kad
berasingan tak boleh klik (gelagat sedia ada — rujuk nota
`display:none` di atas: kad asal yg disembunyi popover TETAP masuk
PDF sbb penjana tak semak `display`), jadi lencana pd istilah dlm
PDF jadi berlebihan/mengelirukan.

Fix (`assets/js/main.js`, dua tempat):
- `_kwHtmlOne()` (IMG branch): skip terus `<img class="kw-glossary-
  badge">` (kembali `''`) SEBELUM logik pemetaan bendera/emoji biasa
  — lencana ni disisip SELEPAS istilah dlm tajuk/ayat (via
  `activateTrigger()`), jadi bila `_kwHtml` rekursif proses tajuk cth.
  `.paper-accordion-title`, ia terjumpa lencana sbg anak biasa & akan
  dicetak spt ikon lain kalau tak ditapis eksplisit.
- `_bodyHtmlNode()` DAN `_renderSubChild()` (dua laluan, sama corak
  drpd skip `.hero-actions`/`.nota-feedback` sedia ada): tambah cabang
  `kw-glossary-standalone-chip` yg skip TERUS (kembali `h` tanpa
  diubah). Cip mandiri (`<button>`, fallback bila istilah TIADA
  kemunculan lain di halaman — cth. "Teluk Intan" bab-3-9.html)
  disisip sbg SAUDARA `card.parentNode.insertBefore(chip, card)`,
  jadi ia sampai ke laluan block-level (bukan `_kwHtml` inline) —
  tanpa cabang ni, jatuh ke fallback generik `_bodyHtml(node)` yg (a)
  KEKALKAN ikon (betul, via cabang IMG sedia ada) TAPI (b) HILANGKAN
  label teksnya senyap (`_bodyHtml` cuma proses nod ELEMEN, span
  label cip tu cuma ada SATU nod teks anak — jatuh fallback lagi,
  nod teks tak pernah sampai `_kwHtml`) — hasil: ikon terapung tanpa
  label dlm PDF. Kad `.glossary-paper` sumber (masih disertakan
  berasingan, tak berubah) sudah ada label+definisi penuh, jadi cip
  pencetus (fungsi KLIK sahaja) tiada nilai tambah dlm dokumen linear
  — digugurkan terus, bukan cuba papar teksnya.

Disahkan via Playwright merentas **25 halaman** (semua halaman
`notes/*.html` yg ada `.glossary-paper`): kira `.kw-glossary-trigger`/
`.kw-glossary-standalone-chip` PADA LAMAN HIDUP (selepas JS
popover-kan jalan) vs kira baki `kw-glossary-badge`/`kw-glossary-
standalone-chip` dlm HTML print tertangkap (`window.html2canvas`
dipintas, baca `el.innerHTML` sblm capture sebenar) — **SIFAR baki**
pd SEMUA halaman (termasuk `bab-3-3.html` 2 trigger & `bab-3-9.html`
1 trigger + 1 cip mandiri), **SIFAR ralat JS**. Semakan kandungan
(`bab-3-3.html`): tajuk accordion tercetak bersih "Fasisme di Itali"
(teks penuh KEKAL, cuma lencana tergugur), kad glosari sumber
("Ringkasan 3.3" & lain-lain label papan) kekal disertakan spt biasa.

## Eksport PDF & Pratonton PDF

Enjin eksport PDF (`_generatePages()` dll., `assets/js/main.js`) render
sisi-klien via html2canvas + jsPDF. Bahagian PALING kompleks & byk sejarah
pepijat dlm codebase ni — **baca `docs/pdf-export-engineering.md` PENUH
sebelum ubah mana-mana fungsi `_pdf*`/`_zp*`/`_kwHtml*`/`_bodyHtml*`**.
AWAS paling kritikal (ringkasan sahaja, bukan penuh):

- **Guna `html2canvas-pro` 2.3.3, JANGAN `html2canvas` 1.4.1** — versi lama
  melukis teks ~0.62em tersasar drpd latar/kotak.
- **SVG WAJIB diraster ke PNG dulu** (`_pdfInlineImages()`) — SVG OpenMoji
  tiada `width`/`height` root, html2canvas gagal SENYAP (0 piksel, tiada
  ralat).
- **`sw.js` JANGAN hidangkan respons `opaque` kpd permintaan mode `cors`**
  — punca ikon Fluent (bukan OpenMoji) kosong senyap dlm PDF.
- **`white-space:nowrap` pd `.zpkw`/`.zpbloc` WAJIB kekal** (mod 2 lajur) —
  buang ni hidupkan semula bug blob/smear html2canvas-pro bila kata kunci
  berbilang perkataan terbelah pertengahan baris.
- **`display:flex` DILARANG pd tajuk PDF** (`h1.zp-title`, `h2.zp-section-
  title`, `.zp-acc-ttl`, `.zp-flap-q/-a`) — flex-wrap bungkus ikon+teks sbg
  SATU unit atom, ikon "terapung" berasingan bila teks >1 baris.
- **Splitter (`_pickPdfSplitY`) MESTI tolak SELURUH blok yg dibelah**
  (`_findBisectedBlock`/`_findSmallestBisectedBlock`) ke muka
  surat/lajur seterusnya, bukan potong tengah kad/kad garis masa/tajuk
  seksyen — sejarah 4+ pusingan bug (kotak terpotong → kandungan hilang
  senyap → tajuk yatim → kad garis masa terpotong) sblm stabil.
- **Header/footer pratonton kini DIBAKAR TERUS ke kanvas komposit**
  (`_pdfComposePreviewPage()`, Canvas 2D `fillText`) — BUKAN elemen HTML
  berasingan (regresi lama: header/footer HTML tak turut skala bila zum).
  Muat turun sebenar (`_savePdf`) lukis teks vektor jsPDF berasingan,
  sumber teks (`_pdfHeaderFooterParts()`) DIKONGSI kedua-dua laluan.
- **Komponen carta baharu (`.paper-split-bar`/`.paper-bar-list`/`.paper-
  donut-wrap`) PERLUKAN cabang PDF eksplisit** dlm `_bodyHtmlNode()` —
  fallback generik SKIP nod teks tak dikenali, data statistik (bilangan/
  peratus) hilang SENYAP tanpa ralat. Semak setiap komponen HTML baharu
  ada cabang PDF sebelum anggap ia "automatik terkendali".
- **Skop 2-lajur semasa: `bab-[1-9]`** (regex tunggal, elak padan
  `bab-10*`). Bila luaskan skop bab, WAJIB liputan `HZ_PDF_OPENMOJI_MAP`
  100% konsep unik bab tu SERENTAK (elak campur gaya OpenMoji/Fluent).
- **Mod "Jimat Dakwat"**: ikon KEKAL (dinyahwarna via
  `_pdfGrayscaleCanvas()` selepas capture), tapi latar `.zpkw` DIGUGUR
  (teks tebal sahaja) — JANGAN togol kedua-duanya serentak tanpa tanya.
- **Skop kandungan PDF sengaja beza drpd nota digital**: "Soalan Utama"
  (`.paper-flap-card`) & "Fokus X.Y" DIGUGURKAN; "Ringkasan"/"Rumusan
  Besar" KEKAL — semak `data-cv-title`, bukan class.
- **Uji dlm sandbox agen**: `npm install html2canvas-pro jspdf --no-save`
  + Playwright `addScriptTag` (CDN sebenar disekat) — JANGAN teka drpd CSS
  semata-mata, `_ensureLibs()` langkau muat turun CDN bila lib dah wujud.
- **Logo header PDF guna `icons/icon-512.png` (PNG), BUKAN `icon.svg`**
  (elak isu rasterisasi SVG html2canvas) — dimuat SEKALI di parse-time
  (`_pdfLogoImg`/`_pdfLogoDataUrl`), lukis di KEDUA-DUA laluan
  (`_pdfComposePreviewPage` canvas 2D & `_savePdf` jsPDF `addImage`)
  guna pemalar saiz/kedudukan DIKONGSI (`PDF_LOGO_*_MM`) — degradasi
  selamat (teks sahaja) kalau imej belum load.

Rekod penuh (setiap pepijat: punca, fix, pengesahan Playwright per-bab
Bab 1–10): **`docs/pdf-export-engineering.md`**.

## Infografik Galeri, Teaser SEO & FAB Suka

Ciri carousel infografik (gaya "Instagram carousel") + teaser SEO statik +
FAB reaksi "Suka" — rujuk **`docs/infographic-gallery.md`** sebelum ubah
`setupInfographicGallery()`/`HZ_INFOGRAPHIC_PAGES`/`setupSukaFab()` dlm
`assets/js/main.js`. AWAS paling kritikal:

- **Digerbangkan ikut WUJUD DATA dlm `HZ_INFOGRAPHIC_PAGES`**, bukan
  senarai laluan berasingan — tambah subtopik baharu = SATU entri data.
- **Imej self-hosted** `assets/infographics/<slug>/`, cache TERSENDIRI
  `MEDIA_CACHE` dlm `sw.js` (BUKAN `CACHE` app-shell yg di-wipe tiap PR).
  **Bila GANTI kandungan fail imej sedia ada (nama sama), WAJIB naikkan
  `imgVersion`** — URL `?v=N` je yg cipta entri cache baharu.
- **Modal skrin-penuh (carousel & teaser) WAJIB keydown fasa CAPTURE +
  `stopPropagation()`** — shortcut sejagat "← →" (fasa bubble) akan
  senyap navigasi keluar halaman kalau tak dihalang.
- **FAB galeri & FAB Suka ikut penjuru FAB sparkle via `MutationObserver`**
  (pantau kelas `.note-sparkle-wrap`), BUKAN gandingan terus dgn logik
  seret sparkle — kekal IIFE berasingan.
- **Teaser SEO**: `<img>` STATIK (cover sahaja) dlm HTML mentah (bukan
  JS-injected) supaya Googlebot index — imej BERWATERMARK, fail
  BERASINGAN drpd slaid 1 galeri, turut perlukan `?v=<imgVersion>` sendiri
  (tiada auto-sync drpd `buildOverlay()`).
- **FAB Suka**: satu sumber kebenaran `ZymStore`, sync 3 lokasi (FAB/
  widget bawah/stat bar) via event custom `zym-suka-changed` — JANGAN
  panggil fungsi IIFE lain terus (skop tertutup).
- **Butang "Kongsi slaid ini" (`#zym-ig-share-btn`) kongsi IMEJ SLAID
  SEMASA** (Web Share API `files`, bukan cuma pautan) — kekal di zon
  "chrome" topbar (bukan atas ilustrasi), indeks slaid dikira SAMA
  formula drpd `updateNav()` (jgn simpan state berasingan). Ikon `<svg>`
  DALAMAN (3 titik bersambung, `IG_SHARE_ICON_SVG_PATH`) — BUKAN icons8
  CDN, elak pergantungan rangkaian luar utk ikon ni sepenuhnya.
- **Butang tutup (`#zym-ig-close-btn`) HANYA desktop** (`display:none`
  lalai, `@media (min-width: 1024px)` — sama corak `.hz-toc` Desktop
  Floating TOC) — mudah alih jimat ruang topbar, tutup kekal via
  tap-luar/Escape/back. Elemen KEKAL dlm DOM pd mudah alih, cuma
  tersembunyi CSS.
- **`og:image`/`twitter:image` halaman berinfografik guna `seo-
  thumbnail.webp` halaman tu sendiri** (bukan `assets/og-image.png`
  generik) — supaya preview "Kongsi Pautan" (WhatsApp/Telegram/FB baca
  tag OG, bukan `navigator.share()`) papar cover sebenar. **TAK
  automatik** — bila tambah subtopik ke `HZ_INFOGRAPHIC_PAGES` atau
  naikkan `imgVersion`, WAJIB kemas kini 5 tag `og:image*`/
  `twitter:image*` di `<head>` halaman tu SERENTAK (dims sebenar
  `1376×841`, bukan `1200×630` OG piawai — turut kemas kini `<img
  height>`/`og:image:height` kalau imej teaser dijana semula, rujuk
  `scripts/generate-teaser-thumbnail.py` di bawah).
- **SETIAP slaid carousel (bukan cuma `seo-thumbnail.webp`) WAJIB
  watermark menegak** (`scripts/watermark-infographic-slides.py`, sudut
  kanan-bawah, "zymnotes.com", **teks slate-800 opacity ~39%, TIADA
  garis luar** — versi awal putih+stroke hitam dilaporkan "spt sticker",
  digantikan gaya subtle) — menu "Download image"/"Share image" natif
  peranti ambil fail `src` TERUS, langkau overlay CSS/JS, jadi watermark
  MESTI dibakar ke piksel. Jalankan skrip ni SEBELUM daftar subtopik
  baharu ke `HZ_INFOGRAPHIC_PAGES`, & naikkan `imgVersion` (cache-bust
  auto via `buildOverlay()`, TAK perlu sunting HTML manual — beza drpd
  teaser SEO). **Skrip `overwrite in-place`, TIADA salinan asal** — utk
  ubah gaya pd fail yg DAH bertera air, ambil fail ASAL (pra-watermark)
  drpd sejarah git, JANGAN cuba "kurangkan" watermark sedia ada.
- **`scripts/generate-teaser-thumbnail.py`** jana `seo-thumbnail.webp`
  drpd ilustrasi SUMBER (belum ada watermark) — jalur footer KEKAL
  KECIL (~72px, logo 36px, fon 30px; versi awal ~150px dilaporkan
  "terlalu besar"). Guna skrip ni (bukan karang jalur baharu manual)
  bila cover subtopik baharu/diganti — output kanvas `1376×841`.
- **Teaser SEO TIADA lagi kotak CTA gradien** (dibuang — "menganggu",
  asing drpd bahasa visual laman) — gantinya tajuk gaya "Bahagian N"
  sedia ada (`.section-heading.note-infographic-heading`, label pil
  "Infografik" + `<h2>Lihat Infografik X.Y</h2>`, ikon Bar chart)
  SEBELUM imej. Guna corak NI bila tambah teaser subtopik baharu.

Rekod penuh (evolusi gaya ilustrasi, kedudukan FAB, pengesahan Playwright):
**`docs/infographic-gallery.md`**.

## Sambung Membaca — kad "teruskan baca" pd laman utama (2026-08-12)

Laman utama (`index.html`) sebelum ni **100% statik** (sama utk semua
pelawat, tiada personalisasi). Ciri ni ciri PERTAMA yg suntik kandungan
peribadi (ikut peranti, bukan akaun — tiada backend) ke laman utama via
JS. Dua IIFE berasingan dlm `main.js` (letak lepas 2 IIFE "CTA subtopik
terakhir/pertama"):

1. **Tulis** (jalan pd SETIAP halaman subtopik nota, `hzZymnotesIsSubtopicNotePathname`)
   — simpan `{url, ts}` ke `ZymStore.getApp('lastRead')`
   (`zym.app` — kunci generik sedia ada, BUKAN kunci baharu). Simpan
   LALUAN sahaja (bukan tajuk) — elak staleness kalau tajuk subtopik
   disunting kemudian.
2. **Baca** (gerbang guna kewujudan `.home-brand-hero` dlm DOM, bukan
   pathname — `.home-brand-hero` HANYA wujud pd laman utama) — padan
   `lastRead.url` dgn `ZYMNOTES_NAV.chapters[].subtopics[]` utk dapat
   tajuk/nombor/warna TERKINI, suntik kad `.home-continue-card` lepas
   `.home-brand-hero` via `insertAdjacentElement('afterend', ...)`.
   **TIADA apa-apa disuntik kalau tiada rekod** (pelawat pertama kali
   kekal nampak laman asal, tiada "kotak kosong").

**Warna aksen bab HANYA pd elemen kecil (eyebrow/anak panah)** — CSS
custom property `--cr-accent` disuntik JS drpd `chapter.color.accent`
(rujuk `ZYMNOTES_NAV`), TAPI latar kad sendiri guna token
`--page-surface-bg`/`--page-surface-border`/`--page-surface-shadow`
sedia ada (SAMA persis drpd `.home-brand-hero`) — BUKAN warna pastel
bab (`chapter.color.bg`) sbg latar penuh, sbb warna tu direka utk mod
CERAH sahaja & akan nampak tak sepadan mod gelap (sama isu/fix drpd
`--mm-ch-bg` pd overlay mindmap, cuma di situ diterima sbg had sbb
badge kecil bulat, bukan kad lebar). Ikut corak ni bila tambah UI baharu
guna warna bab dinamik — jangan letak warna pastel terus jadi latar
kad besar.

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

## Bab Baharu — Senarai Semak Scaffold (bukan sekadar tambah subtopik)

Tambah **subtopik baharu** dlm bab sedia ada (cth. `bab-8-3.html`)
cuma perlukan 1 fail HTML + entri ZH. Tapi tambah **BAB baharu**
(cth. Bab 9) perlukan scaffold navigasi/carian merentas ~10 fail lain
yg SENYAP gagal (halaman "nampak siap" tapi navigasi/carian pincang)
kalau terlepas. Guna senarai ni penuh, bukan sebahagian:

1. **`notes/bab-N.html`** — kad hub (rujuk `notes/bab-8.html` sbg
   templat): hero + lead, kad "Sinopsis" (`paper-chip-sentence` x5-6),
   grid `bab-card` utk setiap subtopik.
2. **`notes/bab-N-1.html` … `bab-N-M.html`** — stub "Akan datang" utk
   tiap subtopik (rujuk sejarah git `bab-8-3.html` SEBELUM diisi, cth.
   `git show <commit-lama>:notes/bab-8-3.html`), nav Kembali/Seterusnya
   penuh antara subtopik (termasuk hab).
3. **`notes/index.html`** — blok baris + panel `<div class="nota-row-
   item">...<div id="panel-bab-N">` (ikut corak bab sebelumnya), PLUS
   breadcrumb `JSON-LD` posisi seterusnya di hujung fail.
4. **`assets/js/main.js`** — TIGA struktur data berasingan, semua
   kena dikemas kini:
   - `HZ_NOTES_SEARCH_PAGES` (sumber carian — hub + tiap subtopik)
   - `ZYMNOTES_NAV.chapters` (tambah entri `num: N` + skema warna +
     senarai `subtopics`)
   - Regex/guard CTA "Seterusnya: Bab N" (2 tempat: fungsi
     `hzZymnotesIsBabHubPathname` & guard `chNum >= 1 && chNum <= N`
     dlm blok IIFE "CTA indeks bab induk seterusnya") — kalau
     terlepas, subtopik terakhir bab SEBELUMNYA takkan auto-tunjuk
     "Seterusnya: Bab N" (btn kekal "Kembali ke Bab N-1").
5. **`assets/css/base.css`** (2 blok: tint rata + gradien vibrant,
   masing² light+dark) **& `assets/css/shell-openmoji.css`** (light+
   dark) — tambah `.nota-row-icon-N` di KEEMPAT-EMPAT tempat. Kalau
   `bab-theme-N` dah pra-sedia dlm `themes.css` (semak dulu — beberapa
   bab akan datang mungkin dah disediakan awal), guna
   `--theme-accent-rgb` sedia ada tu supaya warna ikon padan tema bab.
6. **`sw.js`** — tambah laluan `bab-N*.html` dlm `PRECACHE_URLS`.
   Nombor versi `CACHE` const TAK perlu disentuh manual di sini (rujuk
   §"Aliran Kerja Versioning Aset" di atas).
7. **`data/zh-units/bab-N.json`** (unit sinopsis hub) + daftar dlm
   `data/zh-units/index.json` SERENTAK dgn penciptaan fail (elak isu
   fail ZH tak didaftar — rujuk §"Mod Bahasa Cina" di bawah).
8. **`README.md`** & **`index.html`** (root) — kemas kini teks skop
   "Bab 1 hingga Bab N-1" → "Bab 1 hingga Bab N".
9. **`sitemap.xml`** — jana semula via
   `python3 scripts/generate-updates.py` (auto-discover
   `notes/bab-*.html` via glob, tak perlu edit manual) — TAPI abaikan/
   `git checkout --` balik perubahan `data/updates.json` yg skrip sama
   turut jana (fail tu diselenggara automasi CI selepas merge, bukan
   sebahagian kerja bab baharu).

Sahkan siap dgn `python3 scripts/seo-audit.py` (kena lulus, termasuk
semua fail baharu dlm sitemap) + uji fungsian Playwright CTA "Seterusnya"
pd subtopik terakhir bab sebelumnya (sahkan href/teks btn berubah
selepas load JS).

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

**Tak perlu tunggu/semak CI sebelum merge** — user dah nyatakan ni
BERKALI-KALI (arahan berulang, bukan sekali sahaja, jadi kekal berkuat
kuasa merentas sesi/PR akan datang, JANGAN anggap ia luput lepas satu
PR). Lepas pengesahan manual dah lulus (`python3 scripts/seo-audit.py`,
`npm run lint`, semak diff/tag-balance dll ikut jenis perubahan),
squash-merge PR TERUS tanpa tunggu keputusan check GitHub Actions
(`seo-audit.yml`/`lint.yml`) — JANGAN `send_later`/`ScheduleWakeup`
semata² utk tunggu CI lulus dulu sebelum merge. Ni khusus repo
`zymnotes` (satu cabang produksi, bukan aliran staging→main
`idariq-system`) — pengesahan manual tempatan dah cukup, CI cuma
lapisan kedua/rekod, bukan get merge.
