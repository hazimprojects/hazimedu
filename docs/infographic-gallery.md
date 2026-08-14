# Infografik Galeri, Teaser SEO & FAB Suka — Sejarah & Disiplin Penuh

> Dipecahkan drpd `CLAUDE.md` (2026-08-14). Rujuk fail ni sebelum ubah
> `setupInfographicGallery()`, `HZ_INFOGRAPHIC_PAGES`, teaser SEO
> statik, atau `setupSukaFab()` dlm `assets/js/main.js`. Ringkasan
> AWAS paling kritikal kekal dlm `CLAUDE.md` — fail ni ialah rekod
> penuh keputusan reka bentuk & pengesahan Playwright.

## Infografik Galeri — FAB berasingan, carousel skrin penuh

Ciri BAHARU (2026-08-11): kad infografik gaya carousel media sosial
(imej cerita ilustrasi bergaya "Instagram carousel", diselang-selikan
dgn kandungan teks nota sedia ada) — utk pelajar visual & guru
membentang via projektor kelas. **Skop semasa: 2 subtopik (`bab-1-1`,
`bab-1-2`), 10 slaid setiap satu, KEDUA-DUA guna SATU gaya ilustrasi
seragam** (latar rata krim + tipografi headline besar + label penanda
highlight, ilustrasi isometrik sbg elemen sokongan bukan latar penuh).

**Sejarah ringkas gaya (kekal sbg rujukan, bukan keadaan semasa)**:
`bab-1-1` dibina 2026-08-11 guna gaya painterly/fotorealistik asal,
`bab-1-2` menyusul 2026-08-12 gaya sama (mengesahkan corak
`HZ_INFOGRAPHIC_PAGES` generalize bersih ke subtopik kedua tanpa ubah
kod). 2026-08-13: `bab-1-1` diganti ke gaya BAHARU ni; `bab-1-2` mula-
mula DIGUGURKAN sementara (elak 2 gaya bercampur, entri+fail WebP lama
dibuang sepenuhnya) sehingga versi gaya baharu bab-1-2 disediakan &
diaktifkan semula hari yg sama — laman kini seragam SATU gaya merentas
kedua-dua subtopik. Gaya baharu mampat jauh lebih kecil drpd gaya lama
(~100-130KB/slaid, ~1.1MB utk 10 slaid, BANDING ~150-230KB/slaid &
~2.2MB gaya lama — hampir separuh, sbb latar rata mampat lebih cekap
drpd lukisan penuh detail). **Peluasan ke subtopik BAHARU mana-mana pun
WAJIB guna gaya baharu ni** — jangan ulang gaya painterly lama.

**Keputusan reka bentuk (dibincang dgn pengguna dulu, rujuk sejarah
perbualan)**: FAB BERASINGAN (bukan item dlm menu sparkle sedia ada,
beza drpd corak "Muat turun PDF" §atas) — sbb ciri ni "bukan ciri
kecil", perlu SENTIASA kelihatan tanpa buka menu dulu (kegunaan
projektor kelas perlukan akses satu-klik). **Digerbangkan ikut WUJUD
DATA, bukan senarai laluan** — `HZ_INFOGRAPHIC_PAGES` (`main.js`,
sebelum IIFE `setupNoteFeatures`) ialah objek `{ 'bab-X-Y': {title,
slides:[...]} }`; FAB (& carousel) HANYA muncul pd subtopik yg ada
kunci sepadan. Nak tambah infografik utk subtopik lain: (1) proses
imej ke WebP (rujuk langkah di bawah), (2) tambah SATU entri baharu ke
`HZ_INFOGRAPHIC_PAGES` — TIADA tempat lain perlu disunting (bukan
senarai laluan berasingan drpd data).

**Storan imej**: `assets/infographics/<slug>/<01-nama-slaid>.webp` —
self-hosted (BUKAN CDN luar, sbb kandungan spesifik-subtopik, bukan
ikon kongsi meluas macam bendera/emoji). Sumber asal (PNG ~2.3MB
setiap satu, 852×1846) dimampatkan via Pillow (`Image.save(...,
"WEBP", quality=80, method=6)`) → ~150-230KB setiap satu (~1.9MB utk
10 slaid) — imbangan kualiti teks (masih tajam pd zum biasa) vs saiz
muat turun. **AWAS — sahkan turutan slaid padan turutan BAHAGIAN
sebenar pd halaman** (rujuk `notes/bab-X-Y.html`, cari `paper-label
small` utk senarai "Bahagian Pertama/Kedua/..."), BUKAN turutan
muat naik/tempel imej drpd pengguna — turutan asal (ikut ID muat naik)
utk `bab-1-1` didapati TERSILAP (imej "Empat Unsur" & "cover" tertukar
kedudukan berbanding kandungan sebenar) semasa prototaip ni dibina;
dibetulkan dgn baca SETIAP imej sumber satu-satu (bukan anggap drpd
urutan paste dlm chat) & padan dgn struktur `data-cv-title`/
`paper-label small` halaman sebenar sebelum mampat & simpan.

**TIADA precache `sw.js`** (sengaja, sama corak drpd audio naratif
`.mp3` yg turut tak dipracache) — imej ni "berat, per-halaman, opt-in"
(pelajar/guru yg tak pernah buka galeri tak patut tanggung muat turun
~1.9MB percuma). Imej automatik ter-cache lepas kali PERTAMA dibuka
(online), tersedia offline lepas tu.

**AWAS — imej infografik guna cache TERSENDIRI (`MEDIA_CACHE = 'zym-
media-v1'` dlm `sw.js`), BUKAN cache app-shell biasa (`CACHE`)** — isu
skala ditemui 2026-08-12: `activate()` `sw.js` padam SEMUA cache lama
tiap kali `CACHE` naik versi (berlaku SETIAP PR ubah CSS/JS, kerap).
Kalau imej infografik dicache di bawah `CACHE` biasa (asalnya guna
peraturan generik "Same-origin non-document GET: cache-first"), pelajar
yg dah buka galeri terpaksa muat turun SEMULA ~2MB stiap kali app-shell
dikemas kini — defeat tujuan cache offline. Fix: laluan
`/assets/infographics/` dilayan cabang berasingan dlm fetch handler,
simpan ke `MEDIA_CACHE` yg DIKECUALIKAN drpd senarai padam `activate()`.
Match kena EXACT URL (bukan `{ ignoreSearch: true }` spt cache-first
assets lain) — tiada wipe automatik di sini utk paksa versi baharu,
jadi cache-busting kandungan imej individu bergantung SEPENUHNYA pd
`?v=<imgVersion>` (rujuk atas) mencipta entri URL baharu, bukan padam
entri lama. Naikkan nombor `zym-media-v1` → `v2` MANUAL hanya kalau
STRATEGI caching sendiri berubah — JANGAN naikkan bila kandungan imej
bertukar (tu kerja `imgVersion`). **Bila tambah jenis media "berat,
per-halaman, opt-in" baharu (cth. video, audio besar), guna corak
MEDIA_CACHE ni drpd awal** — jangan letak di bawah `CACHE` app-shell yg
di-wipe kerap.

**Overlay dibina LEWAT** (`buildOverlay()`, hanya bila FAB diklik kali
PERTAMA — bukan semasa `DOMContentLoaded`) — slaid pertama `loading=
"eager"`, baki 9 `loading="lazy"`, jadi 10 imej TAK dimuat turun
sekaligus kalau FAB tak pernah diklik. Struktur (topbar + track
scroll-snap-x + butang prev/next + kiraan "N / M") sengaja MENIRU
corak pratonton PDF sedia ada (`#zym-pdf-overlay`/`#zym-pdf-pages`,
rujuk §"Pratonton PDF" atas) utk konsisten estetik modal skrin-penuh
di laman ni — BUKAN guna semula kod PDF terus (IIFE berasingan
sepenuhnya, rujuk sebab di bawah).

**AWAS — IIFE `setupInfographicGallery()` sengaja BERASINGAN drpd
`setupNoteFeatures()`** (bukan tambah sbg item dlm sparkle FAB) — elak
gandingan dgn logik seret/snap-penjuru sparkle FAB yg sedia ada rapuh
(rujuk §"Swipe Nav" & sejarah sparkle FAB atas). FAB galeri ni kekal
kedudukan TETAP (tak boleh diseret), letak guna
`--floating-bottom-offset-avoid-sparkle` sedia ada (dicipta asalnya
utk `zh-disclaimer-toast`/`audio-notice-sheet`, nilai +4.25rem drpd
offset FAB sparkle biasa — SAMA nilai tepat utk "susun di atas FAB
sparkle" di sini, tiada nombor piksel baharu dikarang). Tak
corner-aware (kalau pengguna seret FAB sparkle ke penjuru lain via
`ZymStore.getPref('fabCorner')`, FAB galeri kekal kanan-bawah lalai)
— DITERIMA sengaja, sama had drpd `zh-disclaimer-toast` sedia ada yg
turut tak corner-aware.

**Ikon FAB galeri (`HZ_ICONS8_SPARKLE.gallery`) guna Icons8 "Photo
Gallery" (3D Fluency), `https://img.icons8.com/3d-fluency/94/stack-of-
photos.png`.** Cubaan PERTAMA (CDN Fluent, `hzFluent3dAsset('Framed
picture', 'framed_picture_3d.png')`) tak dpt disahkan dlm sandbox agen
(CDN Icons8 DAN jsdelivr KEDUA-DUANYA disekat proksi sandbox — `curl
-sI` pulang 403 utk kedua-dua, disahkan `$HTTPS_PROXY/__agentproxy/status`
ialah sekatan dasar proksi, BUKAN 404 ikon sebenar) — DIGANTIKAN
selepas pengguna sendiri layari `icons8.com` di peranti sebenar (luar
sandbox), cari "home"/gallery, & salin laluan CDN SEBENAR terus drpd
panel "Link (CDN)" laman tu (tangkapan skrin ditunjuk dlm perbualan).
Ini bentuk pengesahan LEBIH kukuh drpd disiplin grep/curl biasa
§"Ikon Emoji" atas (pengguna sendiri confirm URL wujud & berfungsi di
luar sandbox, bukan tekaan nama ikuti konvensyen sahaja) — **laluan
Icons8 baharu spt ni yg pengguna bekalkan terus BOLEH dipercayai tanpa
verifikasi curl/grep tambahan**, drpd tekaan slug/nama sendiri yg
WAJIB verifikasi dulu.

**AWAS — pepijat SEDIA ADA (bukan disebabkan ciri ni) ditemui semasa
uji ciri ni: keyboard shortcut sejagat "← →" (IIFE "Keyboard Shortcuts:
← → prev/next on note pages", `main.js`) klik
`.hero-actions a.btn` (Kembali/Seterusnya) TANPA semak status
mana-mana modal skrin-penuh terbuka.** Disahkan via Playwright: buka
carousel infografik (atau pratonton PDF — SAMA pepijat, KEDUA-DUA
guna corak `document.addEventListener('keydown', ...)` fasa bubble
tanpa `stopPropagation()`), tekan ArrowRight → carousel/PDF SENYAP
tertutup drpd navigasi keluar halaman (klik pautan tersembunyi di
sebalik overlay), bukan gerak ke slaid/muka surat seterusnya spt
dijangka. **Punca**: pelbagai listener `keydown` berasingan pd
`document`, fasa bubble — `preventDefault()` SAHAJA tak cukup halang
listener LAIN drpd turut jalan; urutan pendaftaran (bukan kod dlm
handler) tentukan siapa jalan dulu, & handler shortcut sejagat
didaftar lebih awal (skrip tahap-atas) drpd handler modal manapun.
**Fix (kedua-dua pratonton PDF & carousel infografik)**: tukar
pendaftaran keydown ke fasa CAPTURE (`addEventListener('keydown', fn,
true)` — hujah ke-3 `true`) + panggil `e.stopPropagation()` pd
cabang Escape/ArrowLeft/ArrowRight (hanya bila overlay berkenaan
SEDANG terbuka). Fasa capture jamin handler modal jalan PALING AWAL
(sebelum SEBARANG listener bubble document lain, tak kira urutan
pendaftaran), `stopPropagation()` halang keydown sampai ke shortcut
sejagat terus. **Kalau tambah modal skrin-penuh BAHARU dgn keyboard
nav sendiri, guna corak capture+stopPropagation ni drpd awal** — jangan
ulang corak bubble-tanpa-stop lama.

Disahkan via Playwright (blok semua permintaan rentas-asal via
`ctx.route()`, elak bunyi CDN tersekat dlm sandbox): FAB muncul HANYA
pd `bab-1-1.html` (SIFAR pd `bab-1-2.html`/`bab-1.html`/
`notes/index.html`/`quiz/bab-1-1.html`), carousel buka & papar 10
slaid (kiraan + tajuk betul), imej pertama & terakhir SAH dimuat
(`naturalWidth` bukan sifar), butang next/ArrowRight/Escape semua
berfungsi (lepas fix capture+stopPropagation atas), FAB galeri &
sparkle TAK bertindih (ujian `boundingBox()` menegak), `seo-audit.py`
(117 halaman) & `check-zh-coverage.py` (100% merentas semua bab) KEKAL
lulus (elemen baharu tiada `data-zh-unit-id`, tak sentuh struktur SEO
sedia ada).

**Susulan — carousel BUKAN betul-betul skrin penuh (pengguna lapor
tangkapan skrin peranti sebenar).** Susun atur ASAL: `#zym-ig-topbar`
bar pepejal (`#0f172a`) yg tolak imej ke bawah + `.zym-ig-slide`
berpadding dgn imej berbucu-bulat/bayang terapung dlm latar gelap
(`#18182b`) — nampak macam "kad dlm bilik gelap", BUKAN pengalaman
tepi-ke-tepi cerita Instagram/status WhatsApp yg dimaksudkan sejak
awal. Fix: imej isi SELURUH `#zym-ig-viewport` (`position:absolute;
inset:0`, imej `width/height:100%; object-fit:contain`, TIADA
padding/bucu-bulat/bayang), `#zym-ig-topbar` bertukar
`position:absolute` TERAPUNG di atas imej dgn latar
`linear-gradient(to bottom, rgba(0,0,0,.68), transparent)` (gaya
scrim cerita, bukan bar pepejal berasingan) — `padding-top: calc(12px
+ env(safe-area-inset-top))` elak bertindih notch/status bar.

**Susulan LAGI — logo "ZN"/header "SEJARAH TINGKATAN 4 · BAB 1" TERBAKAR
dlm imej sumber jadi PENDUA lepas fix skrin-penuh atas** (topbar
overlay kita SENDIRI dah papar tajuk "1.1 Latar Belakang Negara
Bangsa" telus di atas imej — logo+label bab dlm imej jadi lapisan
kedua yg bertindih/berlainan dgn overlay). Pengguna bekalkan SEMULA
10 imej sumber (versi TANPA logo/header terbakar, "supaya kita boleh
letak sendiri di header") — imej WEBP sedia ada di
`assets/infographics/bab-1-1/` DIGANTIKAN penuh (nama fail KEKAL sama,
kandungan tukar).

**AWAS — nama fail imej TAK bertukar bila kandungan ditukar, jadi
`sw.js` cache-first (rujuk atas) TAKKAN nampak imej "baharu" di peranti
yg dah pernah buka galeri sebelum ni** (SAMA punca aduan pengguna
"masih tiada" sblm fix skrin-penuh di atas — cache PWA). Fix (kekal,
bukan sekadar sekali sahaja): `HZ_INFOGRAPHIC_PAGES['bab-X-Y']` kini
ada medan `imgVersion` (integer, mula drpd `1`); `buildOverlay()`
lampirkan `?v=<imgVersion>` pd SETIAP `src` slaid. **Bila TUKAR
kandungan fail imej sedia ada (nama fail sama, isi baharu), WAJIB
naikkan `imgVersion`** — URL berubah (`...01-pengenalan.webp?v=3`
lwn `?v=2`) jadi entri cache BAHARU sepenuhnya drpd sudut pandang
`sw.js`/pelayar, elak peranti pengguna terperangkap dgn versi lama.
TAK perlu naik kalau cuma TAMBAH slaid baharu ke senarai `slides`
(laluan fail baharu automatik "baharu" di cache).

**Susulan — FAB galeri kini IKUT FAB sparkle bila diseret/dibuka**
(pengguna nyata FAB sparkle boleh diseret ke mana-mana 4 penjuru
skrin — rujuk `ZymStore.getPref('fabCorner')`/`snapToCorner()` §sedia
ada — & minta FAB galeri turut serta, termasuk "swap" kedudukan
[atas↔bawah fab sparkle] bila penjuru ATAS dipilih, & beri laluan
[berganjak] bila menu sparkle dibuka supaya tak bertindih dgn item yg
mengembang). **Pendekatan: PANTAU DOM sparkle via `MutationObserver`
pd atribut `class` `.note-sparkle-wrap` (dlm IIFE
`setupInfographicGallery()`), BUKAN gandingan terus dgn kod seret/
snap-penjuru sparkle** (kekal disiplin "IIFE berasingan" sedia ada,
rujuk atas) — fungsi `sync()` baca kelas `fab-corner-*` sparkle semasa
& salin ke wrap FAB galeri sendiri (CSS `.note-gallery-fab-wrap.
fab-corner-tr/tl` letak FAB galeri di BAWAH anchor `top:80px` sparkle
— TERBALIK drpd `fab-corner-br/bl` yg letak DI ATAS, memadankan corak
`column-reverse` sparkle pd penjuru atas [fab dekat anchor, item
kembang KE ARAH BERLAWANAN drpd penjuru bawah]).

**Semasa drag AKTIF** (antara `pointerdown`→`pointerup`), sparkle
buang KESEMUA kelas `fab-corner-*` drpd wrapnya (rujuk `snapToCorner()`/
handler `pointermove` sedia ada) & guna `wrap.style.left/top` piksel
terus ikut jari — `sync()` SENGAJA TIDAK cuba ikut kedudukan piksel
drag tu (elak gandingan rapuh dgn matematik drag sparkle); FAB galeri
kekal diam di kedudukan penjuru TERAKHIR sepanjang drag aktif, &
"melompat" terus ke penjuru BAHARU sebaik `snapToCorner()` letak
semula kelas `fab-corner-*` (pengesanan: `sparkleWrap.className.match(...)`
gagal → `isTop` kekal drpd kelas FAB galeri SENDIRI yg belum diubah).
Disahkan cukup baik secara UX (bukan bug) — tiada aduan "FAB galeri
tercicir semasa seret", cuma kedudukan akhir yg penting.

**Bila menu sparkle terbuka** (`sparkleWrap.classList.contains('is-open')`):
`sync()` ukur `.note-sparkle-items` punya `offsetHeight` (SUDAH
sentiasa reserved dlm DOM tak kira status buka/tutup — rujuk
`opacity:0` bukan `display:none` pd `.note-sparkle-item`, jadi tinggi
tu STABIL, bukan berubah ikut animasi) + 14px jarak, & lekap
`transform:translateY(±shift)` pd wrap FAB galeri (arah NEGATIF utk
penjuru bawah [naik lagi ke atas, jauhi item yg mengembang KE ATAS],
POSITIF utk penjuru atas [turun lagi ke bawah, jauhi item yg
mengembang KE BAWAH]) — animasi CSS `transition:transform` sedia ada
pd `.note-gallery-fab-wrap` jadikan pergerakan ni licin, bukan
melompat. Disahkan via Playwright (simulasi drag tetikus sebenar
`mouse.down/move/up`, BUKAN set kelas terus): penjuru asal `br` →
seret ke `tl` → kelas & kedudukan FAB galeri betul (BAWAH fab
sparkle) → buka menu sparkle → FAB galeri berganjak jauh (y
152→409) → tutup menu → kembali (y 409→152).

**Ikon FAB galeri turut dibesarkan** (46px→48px bulatan, 22px→25px
ikon dalaman; mudah alih 42px→44px/20px→23px) — pengguna nyata "lebih
kemas" drpd nisbah asal.

**Susulan — scrim topbar terlalu lutsinar (bocor warna krim imej sbg
"jalur putih tak kemas" di bawah status bar OS) & anak panah prev/next
sentiasa kelihatan dilaporkan mengganggu.** Fix scrim: `#zym-ig-topbar`
gradient tukar drpd `rgba(0,0,0,.68)→0%` (lutsinar drpd awal) kpd
LEGAP PENUH `rgba(0,0,0,.92)` kekal sehingga 30% tinggi topbar, baru
reda ke `.55` (65%) & lutsinar (100%) — padding-bottom turut
dipanjangkan 28px→46px supaya blend ke imej lebih graduan (bukan
reveal mendadak). Fix anak panah: `#zym-ig-prev`/`#zym-ig-next` kini
`opacity:0;pointer-events:none` LALAI (bukan sentiasa nampak) — hanya
berdenyut SEBENTAR (`@keyframes zymIgHintPulsePrev/Next`, ~1.6s, arah
translateX bertentangan kiri/kanan sbg isyarat "boleh swipe") bila
`openOverlay()` tambah kelas `.zym-ig-hint-pulse` pd overlay (dibuang
via `setTimeout` lepas animasi tamat). Logik `scrollBy()` sedia ada
KEKAL sama, cuma kelihatan/klik yg berubah — swipe & kekunci panah
KEKAL cara utama navigasi (disahkan Playwright: `ArrowRight` masih
berfungsi lepas hint reda, klik pd kawasan anak panah yg dah lutsinar
TIDAK berdaftar sbb `pointer-events:none`). Guna `void overlay.
offsetWidth` (paksa reflow) sebelum tambah semula kelas hint pd SETIAP
`openOverlay()` — CSS animation TAK restart kalau kelas dibuang &
ditambah semula dlm tick JS yg sama tanpa reflow paksa di antaranya
(bug animasi terkenal), jadi buka-tutup-buka carousel pantas tetap
dapat denyut baharu setiap kali.

**Susulan — 4 pembaikan lanjut lepas pengguna tunjuk tangkapan skrin
peranti sebenar (mod cerah): (1) status bar OS putih, (2) gantikan
anak panah dgn dash/dot, (3) logo ZymNotes rasmi pd header, (4)
disclaimer beretika kandungan janaan AI.**

1. **Status bar putih dlm mod cerah** — `applyTheme()` (dekat awal
   fail ni) tukar `meta[name=theme-color]` ikut tema laman (`#ffffff`
   mod cerah, `#0D0F1A` mod gelap) — bila carousel (lightbox gelap)
   dibuka semasa mod cerah, status bar OS kekal putih, berlanggar dgn
   overlay gelap. Fix: `setOverlayThemeColor(dark)` (dlm
   `setupInfographicGallery()`) paksa `#000000` bila `openOverlay()`,
   pulih ikut tema SEBENAR (baca `data-theme` drpd `<html>` terus,
   bukan andaian tetap) bila `closeOverlayUi()`.
2. **Anak panah digantikan dash indicator kekal** (bukan sekadar
   denyut sekali spt susulan sblm ni — DIBUANG sepenuhnya, gantung
   `#zym-ig-dashes`: N `<span class="zym-ig-dash">` nipis gaya
   "segmented progress bar" cerita IG, `.is-active`/`.is-passed`
   dikemas kini dlm `updateNav()` ikut slaid semasa). Navigasi
   tetikus (guru projektor tanpa skrin sentuh) — ketik 30% tepi
   kiri/kanan imej, corak "ketik tepi imej" cerita IG/status WhatsApp
   sebenar (bukan cuma swipe/kekunci panah).

   **AWAS — JANGAN laksanakan zon ketik ni sbg elemen `<div>`
   berasingan position:absolute BERLAPIS DI ATAS `#zym-ig-track`.**
   Percubaan PERTAMA (`.zym-ig-tap-zone-prev/next`, `z-index:2`, 30%
   lebar tepi) PECAHKAN swipe tepi kiri/kanan sepenuhnya — dilaporkan
   pengguna "swipe tak berfungsi bila diseret dari hujung skrin, cuma
   bahagian tengah boleh". Punca: div overlay tu "menelan" gerak
   isyarat SENTUH SEBELUM sampai ke `#zym-ig-track` (scroll-snap
   sebenar) di bawahnya — walau `pointer-events`/`preventDefault`
   TAK disentuh langsung, kewujudan elemen SIBLING yg dilapis di atas
   (bukan CHILD track) sudah cukup jadi TARGET touch pertama pd 30%
   kawasan tu, & elemen tu sendiri tiada `overflow-x`/scroll-snap
   (bukan keturunan track), jadi touch drag di situ MATI (tiada
   scroll native berlaku, cuma tap/click SAHAJA yg didaftar). **Fix
   (kekal)**: buang elemen `.zym-ig-tap-zone` terus, gantikan dgn
   SATU listener `click` terus pd `#zym-ig-track` sendiri (`e.clientX`
   dikira relatif drpd `track.getBoundingClientRect()`, <30% =
   prev, >70% = next). Klik TERUS pd track/imej (bukan elemen berlapis
   berasingan) TAK berlanggar dgn swipe — pelayar sendiri TAK
   lepaskan event `click` bila gerakan touch/tetikus melebihi ambang
   dalaman (drag ≠ tap), jadi track kekal 100% scroll-snap-kan
   sepanjang lebarnya sambil TETAP dpt klik/tap kiri-kanan.
3. **Logo ZymNotes rasmi pd header** — `#zym-ig-logo` guna
   `/icons/icon.svg` SEDIA ADA (badge gradien "ZN", sama aset persis
   dipakai pd `.app-logo-icon` header laman biasa) — SELF-HOSTED, tak
   terjejas sekatan CDN sandbox spt ikon Fluent/Icons8 lain. Diletak
   sbg pengganti logo/header yg dibuang drpd imej sumber sblm ni
   (rujuk susulan "logo ZN terbakar" atas) — jenama kini datang drpd
   chrome overlay kita, bukan dibakar dlm imej.
4. **Disclaimer AI beretika** — `#zym-ig-ai-disclaimer` (teks kecil
   terapung bawah, SEPANJANG carousel terbuka, bukan per-slaid sbb
   berkaitan SEMUA 10 ilustrasi): "Ilustrasi dijana AI, mungkin tidak
   tepat — nota teks kekal rujukan utama" — frasa sengaja ikut corak
   disclaimer SEDIA ADA `.audio-notice-text` ("Audio mungkin
   mengandungi ringkasan — nota adalah rujukan utama") supaya nada
   konsisten merentas laman, bukan dikarang generik/beza gaya.

Disahkan via Playwright: `meta[theme-color]` betul `#ffffff`(sebelum)
→`#000000`(terbuka)→`#ffffff`(tutup, mod cerah default), 10 dash
wujud dgn `.is-active` betul pd slaid 1, `#zym-ig-prev`/`#zym-ig-next`
disahkan SIFAR (dibuang penuh drpd DOM), logo & disclaimer wujud &
teks tepat, klik pd 30% kanan `#zym-ig-track` majukan carousel (kiraan
2/10) & kemas kini dash (`.is-passed` pd dash 1, `.is-active` pd dash
2) dgn betul — & lepas fix zon-ketik (rujuk AWAS atas), gerak isyarat
sentuh SEBENAR (CDP `Input.dispatchTouchEvent`, BUKAN klik) drpd tepi
KIRI (x=20) & tepi KANAN (x=370, viewport 390px) kedua-duanya
disahkan majukan/mundurkan `track.scrollLeft` dgn betul.

## Teaser SEO Infografik — `<img>` STATIK berwatermark utk Google Image (2026-08-13)

**Isu ditemui**: carousel galeri (§atas) 100% JS-injected — `buildOverlay()`
HANYA dipanggil bila FAB diklik (`openOverlay()`), jadi elemen `<img>`
slaid TIADA LANGSUNG dlm HTML halaman kecuali pengguna sebenar klik.
Googlebot execute JS semasa crawl tapi TAK simulasi klik pengguna, jadi
kesemua 10 slaid setiap galeri kekal TAK PERNAH diindeks Google Image
walau `alt` text ditulis rapi — disahkan via `curl`/fetch mentah HTML
(tiada laluan `assets/infographics/` langsung dlm sumber).

**Fix**: satu `<img>` STATIK (slaid 1/cover sahaja, BUKAN 10-10) diletak
terus dlm HTML setiap halaman yg ada entri `HZ_INFOGRAPHIC_PAGES` —
`<a class="note-infographic-teaser" id="zym-ig-seo-teaser">` dgn `<img>`
+ label CTA "Lihat infografik penuh", diletak dlm `note-section` PERTAMA
lepas hero (sblm pemain audio). Klik disambungkan semula ke
`openOverlay()` SEDIA ADA (`main.js`, dlm `setupInfographicGallery()`
lepas `fab.addEventListener`) — cari `#zym-ig-seo-teaser`, kalau wujud
lampirkan listener yg buka carousel penuh SAMA macam FAB, `href` jatuh
balik ke laluan imej terus (bukan `#`) sekiranya JS gagal.

**AWAS — imej teaser BERWATERMARK, BERBEZA drpd slaid 1 dlm galeri
sendiri** (`assets/infographics/<slug>/seo-thumbnail.webp`, fail
BERASINGAN drpd `01-pengenalan.webp`) — logo "ZN" (`icons/icon-512.png`)
+ teks "zymnotes.com" diletak dlm JALUR FOOTER KHAS ditambah DI BAWAH
imej asal (kanvas baharu, tinggi asal + ~11% lebar), BUKAN overlay atas
kandungan asal. **Sebab jalur berasingan (bukan overlay atas imej)**:
percubaan pertama overlay lutsinar di penjuru bawah-kanan menutupi teks
sebenar pd sesetengah kandungan (footer band bab-1-2 sampai hujung
bawah, tiada margin kosong konsisten merentas semua cover) — jalur
footer khas jamin TIADA overlap walau reka letak cover berbeza-beza.
Cuma imej COVER sahaja (bukan semua 10 slaid) diwatermark — cukup utk
tujuan SEO/pengecaman jenama tanpa proses 10× kerja tiap subtopik.

**Skrip janaan** (bukan automatik, jalan manual tiap kali cover baharu/
diganti): rujuk corak dlm sejarah PR "Tambah teaser SEO infografik" —
`Image.new('RGB', (w, h+strip_h), (250,247,238))`, tampal imej asal di
`(0,0)`, logo + teks Liberation Sans Bold (`/usr/share/fonts/truetype/
liberation/`) dicantum tengah dlm jalur bawah. **Bila cover subtopik
digantikan** (rujuk §"Infografik Galeri" atas, disiplin `imgVersion`),
`seo-thumbnail.webp` WAJIB turut dijana semula drpd cover baharu — janji
`<img>` statik dlm HTML kekal segerak dgn slaid 1 galeri sebenar.

**AWAS — `<img src>`/`<a href>` teaser WAJIB ada `?v=<imgVersion>`
(sama nilai drpd `HZ_INFOGRAPHIC_PAGES[slug].imgVersion` semasa)** — laluan
`seo-thumbnail.webp` STATIK dlm HTML (bukan disuntik JS), jadi TIADA
mekanisme automatik utk tambah query cache-bust macam slaid galeri
(`buildOverlay()` lampirkan `?v=` sendiri). Tanpa `?v=` di sini, peranti
yg dah cache URL tu (via `MEDIA_CACHE`, match EXACT URL) kekal papar
kandungan LAMA selama-lamanya walau fail sumber dah diganti — lupa
tambah/naikkan nombor ni ialah punca paling senang tersasar bila cover
diganti kemudian.

Disahkan via Playwright: `<img>` disahkan wujud dlm HTML MENTAH (fetch
terus, bukan lepas JS render) utk kedua-dua `bab-1-1`/`bab-1-2`, klik
kad teaser disahkan buka `#zym-infographic-overlay.is-open` SAMA persis
drpd FAB. `scripts/seo-audit.py` (117 halaman) kekal lulus.

## FAB Suka — akses pantas reaksi "Suka" (2026-08-14)

**Isu**: butang "Suka!" boleh-klik SEBENAR cuma wujud dlm widget
`.nota-feedback` di HUJUNG halaman subtopik (rujuk IIFE "Nota Feedback
Widget", `main.js`) — pengguna perlu skrol jauh utk bertindak balas,
walau bar statistik ringkas `.nota-stat-bar` (paparan sahaja, TAK boleh
klik) dah muncul dekat atas lepas `.lead`. Pengguna laporkan ni jejaskan
"first impression".

**Fix**: FAB baharu (`.note-suka-fab-wrap`/`.note-suka-fab`, IIFE
`setupSukaFab()` dlm `main.js`, lepas IIFE `setupInfographicGallery()`)
bagi akses SATU-KLIK segera. **Skop v1 (disahkan pengguna): "Suka" ❤️
SAHAJA** — 3 reaksi opinion lain (Mudah difahami/Boleh diperbaiki/Kurang
jelas) KEKAL di widget bawah sahaja, sbb perlukan pelajar dah BACA &
fikir dulu (tak sesuai jadi FAB satu-klik).

**Kedudukan — ikut penjuru FAB sparkle SEMASA** (SAMA corak `sync()`
FAB galeri: pantau `.note-sparkle-wrap` via MutationObserver, BUKAN
gandingan terus — kekal falsafah "IIFE berasingan" §"Infografik
Galeri"). **Kalau FAB galeri turut wujud pd halaman ni** (cth.
`bab-1-1`/`bab-1-2`), FAB Suka susun SATU TINGKAT LEBIH JAUH (translateY
tambahan ±58px desktop/±54px mobile, dikesan drpd wujud
`.note-gallery-fab-wrap` semasa — BUKAN dikodkan keras per-halaman)
supaya 3 FAB (Suka/Galeri/Sparkle) tersusun kemas TANPA bertindih.

**SATU sumber kebenaran storan** — guna SEMULA
`ZymStore.getSukaGiven/saveFeedback/clearSuka` sedia ada (BUKAN storan
berasingan). **Penyegerakan 2-hala merentas 3 lokasi** (FAB, widget
bawah, `.nota-stat-bar` atas) guna event custom `document.dispatchEvent
(new CustomEvent('zym-suka-changed', {detail:{path}}))` — disiar
SETIAP kali state berubah drpd MANA-MANA lokasi, ketiga-tiga lokasi
dengar & baca semula `ZymStore` (bukan kongsi closure/variable terus
rentas IIFE, kekal falsafah decoupling sedia ada). **Kalau tambah
lokasi UI baharu utk reaksi Suka pd masa depan, ikut corak event ni**
drpd cuba panggil fungsi IIFE lain terus (tak boleh — skop tertutup).

**Panggilan RPC Supabase disalin kecil** (`submitSukaRpc`/`deleteSukaRpc`
dlm IIFE FAB) drpd cuba kongsi terus dgn `submitFeedback`/
`deleteSukaFromSupabase` dlm IIFE widget bawah (skop LOKAL kedua-dua,
tak boleh diakses rentas IIFE) — ikut disiplin sedia ada fail ni (rujuk
`fetchReactionCounts`/`fetchPdfDownloadCount` yg turut buat salinan
kecil serupa drpd cuba abstrak fungsi kongsi).

**Hati melayang bila TAMBAH Suka** (bukan bila buang) — 3 emoji ❤️
literal (bukan imej CDN, elak permintaan rangkaian tambahan) disemai
di kedudukan FAB, animasi CSS `@keyframes zym-heart-float` (translate
naik + fade out + jitter mendatar rawak via `--hx`), dibuang JS lepas
~1.2s. Murni hiasan (`aria-hidden`, `pointer-events:none`).

**Skop TAK termasuk (buat masa ini, disengajakan)**: akses reaksi Suka
DALAM carousel galeri fullscreen sendiri — pengguna cadangkan asalnya
tapi keputusan skop v1 kekal "FAB sahaja". Boleh tambah kemudian sbg
susulan (rujuk sejarah perbualan) — kalau buat, ikut corak event
`zym-suka-changed` sedia ada, JANGAN gandingan terus dgn IIFE galeri.

**AWAS — FAB HILANG PERLAHAN lepas "Suka" diberi** (susulan maklum
balas pengguna: kekal kelihatan lepas diklik dilaporkan "mengganggu").
`syncVisual(immediate)` dlm `setupSukaFab()` urus DUA laluan berbeza —
(1) **muat kali PERTAMA halaman** (`immediate=true`): kalau rekod dah
"suka" drpd sesi lalu, FAB terus `opacity:0` SEBELUM cat pertama,
TIADA kelip kelihatan-lalu-hilang; (2) **tukar SEMASA sesi ni**
(`immediate=false`, klik FAB atau klik widget bawah): FAB kekal
kelihatan 700ms dulu (beri ruang animasi hati melayang habis) SEBELUM
`opacity` beralih ke 0 via CSS transition — `hideTimer` (var closure)
disahkan clear sblm jadual baharu, elak timer bertindih kalau
`syncVisual()` dipanggil berulang pantas (cth. klik sendiri turut
picu event `zym-suka-changed` yg dengar balik pd IIFE sama). **Undo
(klik "Suka!" di widget bawah) buat FAB MUNCUL SEMULA serta-merta**
(bukan kekal tersembunyi) — keadaan FAB sentiasa cerminkan "bolehkah
bagi reaksi ni SEKARANG", bukan "adakah pernah diklik".

Disahkan via Playwright: FAB muncul & posisi betul pd halaman TANPA
galeri (`bab-1-3`) & DGN galeri (`bab-1-1`, tersusun tanpa bertindih,
disahkan `bounding_box()` tiada overlap menegak), klik FAB spawn 3
hati melayang & tukar `ZymStore.getSukaGiven` ke `true`, keadaan
disahkan sync KEDUA-DUA arah (klik FAB → widget bawah `is-active` ikut
sama; klik widget bawah → FAB `is-active` ikut sama), FAB yield betul
bila menu sparkle dibuka (translateY berubah). Susulan (hilang
perlahan): disahkan FAB KEKAL kelihatan 200ms lepas klik (animasi
hati sempat nampak), `opacity` jatuh ke ~0 lepas ~900ms, undo drpd
widget bawah pulihkan `opacity` ke 1 serta-merta, & muat semula halaman
dgn rekod "suka" sedia ada terus `opacity:0` (tiada kelip). `scripts/seo-audit.py`
(117 halaman) lulus.

