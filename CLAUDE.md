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

## Swipe Nav — seret `<main>` ke subtopik sebelum/selepas (prototaip)

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

Skop semasa: `bab-3-2.html` sahaja (prototaip, tunggu pengesahan
pengguna sblm luaskan ke semua 44/45 halaman subtopik + nyahaktifkan
zoom sejagat).

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
