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
  **Skop diluaskan** (pengguna tunjuk tangkapan skrin kad "Filipina/
  Burma/Vietnam/Indonesia/Thailand" masih guna glob generik, minta
  imbasan MENYELURUH 8 bab + accordion/chip). Kajian sistematik (regex
  cari kesemua `.paper-chip` di SELURUH `notes/*.html` yg teksnya
  SAMA PERSIS nama negara ATAU bermula "NEGARA –/—/→ ringkasan"
  pendek — SENGAJA elak padan ayat prosa penuh yg cuma SEBUT nama
  negara di tengah, cth. "British bertindak mengekang..." — itu BUKAN
  cip identiti, jgn diberi bendera) dedah **10 cip** merentas 2
  halaman terlepas drpd imbasan asal: `bab-2-4.html` (5 — Filipina,
  Burma, Vietnam, Indonesia, Thailand, dlm kad "Kesimpulan 2.4") &
  `bab-3-2.html` (5 — Jerman×2, Austria-Hungary, Rusia×2, corak "NEGARA
  → akibat" dlm accordion "A. Keruntuhan Pemerintahan Beraja", TERLEPAS
  drpd imbasan asal walau halaman ni SUDAH dlm skop 13-halaman —
  akibat berlainan corak cip: "NEGARA sahaja" vs "NEGARA → ringkasan").
  2 negara BAHARU (Vietnam, Thailand) tiada SVG lagi — ditarik dari
  `circle-flags` (git proxy baca awanama, klon cetek `--depth 1`,
  salin `flags/vn.svg`+`flags/th.svg` ke `assets/flags/`, padam klon
  lepas siap — LICENSE.md sedia ada sudah cukup, MIT sama). Skop
  semasa: **42 negara** (rujuk senarai kod ISO dlm `assets/flags/`)
  merentas **14 halaman** — bab-2-4 (baharu), bab-3-2, bab-3-3 s/d
  bab-3-8 (PD1/PD2), bab-4-6, bab-5-1, bab-5-2, bab-6-1, bab-6-3,
  bab-7-5. Entiti sejarah
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

  **Skop diluaskan lagi (pusingan 2)**: pengguna tunjuk tangkapan skrin
  kad navigasi `.paper-kingdom` (grid nombor keycap di atas seksyen,
  cth. "1️⃣ Nasionalisme di India 🌐") + `<h2>` seksyen sepadan (teks +
  ikon SAMA berulang) — corak BERBEZA drpd `.paper-chip`, TERLEPAS drpd
  KEDUA-DUA imbasan asal. Minta imbasan MENYELURUH "jangan terlepas
  satu pun" — dibuat 2 pusingan imbasan agen berasingan (kad
  kingdom/h2 dahulu, accordion bersarang `.paper-accordion-item`
  kemudian, sbb corak accordion baharu ditemui semasa imbasan pertama).
  Kes kabur (negara sbg PENYERANG/aktor sepintas lalu dlm tajuk ttg
  sejarah TEMPATAN kita, cth. "Penentangan terhadap British di Kedah",
  "Faktor/Serangan Jepun terhadap **Negara Kita**") — user sahkan KEKAL
  DIKECUALIKAN (ikut precedent Czechoslovakia/dll di atas — bukan
  keputusan mekanikal, perlu tanya dulu). Kes tajuk yg negara jelas jadi
  SUBJEK biarpun tatabahasa jadi objek (cth. "Sekatan Ekonomi terhadap
  Jepun", "Garisan Masa Serangan Jepun", "Kerjasama dengan Amerika")
  KEKAL diberi bendera — beza drpd kes "Negara Kita" sbb fokus naratif
  tetap negara asing tu, bukan Malaysia/tempatan.
  - Kad `.paper-kingdom` + `<h2>` sepadan (lebar 20px kad / 22px h2,
    KEKALKAN beza ni bila ganti ikon): bab-2-2 (England→`gb.svg`,
    Amerika Syarikat→`us.svg`, Perancis→`fr.svg`), bab-2-3 (India→`in.svg`,
    China→`cn.svg`, Jepun→`jp.svg`, Empayar Uthmaniyah & Mesir→
    `tr.svg`+`eg.svg` DWI-bendera), bab-2-4 (Filipina→`ph.svg`, Burma→
    `mm.svg`, Vietnam→`vn.svg`, Indonesia→`id.svg`, Thailand→`th.svg`),
    bab-3-4 (Peluasan Kuasa Jepun & Sekatan Ekonomi terhadap Jepun→
    `jp.svg`), bab-6-1 (Komunis dari China→`cn.svg`, dari Indonesia→
    `id.svg`; kad kingdom di sini TIADA ikon ekor asal — bendera
    DITAMBAH, bukan ganti).
  - Kad `.paper-accordion-item` (ikon dlm `.paper-accordion-no`, 20px,
    kekalkan lebar) + `.paper-strip.strip-sub` sepadan bila wujud:
    bab-2-3 (Dahagi India 1857→`in.svg`; Kemerdekaan India dan
    Pakistan→`in.svg`+`pk.svg` DWI-bendera, Pakistan svg BAHARU), bab-2-4
    (Kerjasama dengan Amerika→`us.svg`, Kesudahan perjuangan di
    Vietnam→`vn.svg`, Revolusi Thai→`th.svg`), bab-3-3 (Fasisme di
    Itali→`it.svg`, Nazisme di Jerman→`de.svg`, Kesan terhadap
    Jerman/Itali→`de.svg`/`it.svg`, Krisis Habsyah→`et.svg` Ethiopia svg
    BAHARU gantikan 2 ikon glob bertindan, Penaklukan Jerman di Eropah
    Barat→`de.svg`, Pengeboman Britain→`gb.svg`, Penyertaan Itali dalam
    Perang→`it.svg`, Serangan ke atas Rusia – Operasi Barbarossa→
    `ru.svg`), bab-3-4 (Garisan Masa Serangan Jepun→`jp.svg`), bab-6-1
    (Kegagalan di Indonesia→`id.svg`). **Krisis Manchuria** (bab-3-3)
    SENGAJA dikekalkan tanpa bendera tunggal — Manchuria bukan negara
    berdaulat (rujuk entiti dilangkau di atas), badan teks dah guna
    cip bendera berasingan (`jp.svg` penyerang / `cn.svg` pemilik).
  - Skop semasa selepas 2 pusingan ni: **45 negara** (rujuk
    `assets/flags/`, +3 baharu drpd pusingan ni: `eg.svg`, `pk.svg`,
    `et.svg`).

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

## Eksport PDF — Susun Atur 2 Lajur (skop Bab 1 & Bab 2)

Pengguna minta gaya "2 lajur" (spt nota Scribd rujukan pelajar — mudah
lipat 2, guna ruang kosong dgn bijak). Skop asal DIHADKAN kpd Bab 1
sahaja, kemudian DILUASKAN ke Bab 2 (`_pdfIsTwoColumnScope()`, regex
`/\/notes\/bab-[12](-\d+)?\.html$/i` pd `window.location.pathname`)
— bab lain kekal 1 lajur asal, TIADA perubahan langsung drpd semakan
skop ni (kod lama berjalan byte-demi-byte sama bila `twoCol=false`).
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
(78 konsep / 507 kemunculan) **& 100% konsep unik Bab 2** (+88 konsep
baharu, 166 kesemuanya) — sengaja penuh, bukan separa, sebab
liputan separa (dulu 25 konsep = 82%) tinggalkan **campuran gaya
OpenMoji + Fluent dlm senarai yg sama** (cth. keycap 1–4 OpenMoji tapi
5–6 Fluent) yg ketara janggal. Bila luaskan ke bab lain, liputi
SEMUA konsep bab itu sekali gus. `_pdfEmojiSrc()` turut terima segmen
varian pilihan sebelum `/3D/` (cth. `/assets/Writing hand/Default/3D/`)
— tanpa itu ikon sebegini senyap terlepas drpd peta.

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
  kedua-dua tapak panggilannya DIBUANG). Pinch native tak lagi
  berfungsi dlm modal — digantikan kawalan +/- di bawah.
- `_pdfApplyZoom()`/`_pdfZoomBy()`/`_pdfResetZoom()` (`main.js`, lepas
  `var _pdfCache = {...}`) urus tahap zum (`_pdfZoomLevel`, langkah
  0.25, julat 50%–300%) via kelas `#zym-pdf-pages.zp-zoomed` + `width`
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
