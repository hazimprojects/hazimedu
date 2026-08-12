# ZymNotes — Panduan Agen

Laman statik (HTML/CSS/JS vanilla, tiada framework/build step JS) untuk nota
ulang kaji KSSM pelajar Malaysia. Deploy ke GitHub Pages (domain custom
`zymnotes.com` via `CNAME`, `.nojekyll` — serve terus dari root repo, `docs/`
bukan folder Pages, ia dokumentasi dalaman). Rujuk `README.md` untuk
senarai ciri & struktur penuh — fail ni fokus pada apa yang perlu tahu
supaya tak tersalah anggap senibina sedia ada.

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

  **Pusingan 3 — audit ikon 🌐 "Globe with meridians" (bukan chip
  identiti negara, tapi ikon generik dipilih utk pelbagai kandungan
  serantau).** Pengguna tunjuk tangkapan skrin kad "Pengaruh Luar &
  Serantau" (bab-2-6.html) dgn ikon 🌐🌐 berganda di hadapan
  "gerakan nasionalisme di Filipina dan Indonesia", minta semakan
  kesemua penggunaan ikon 🌐 merentas laman — "ada diantaranya lebih
  sesuai digunakan ikon bendera". BEZA drpd 2 pusingan sebelum (yg
  scope `.paper-chip`/`.paper-kingdom`/`.paper-accordion-item` bernama
  negara tepat), pusingan ni case-by-case: ikon 🌐 (`globe_with_
  meridians_3d.png`, BUKAN `globe_showing_asia-australia` yg dikhaskan
  utk lencana entiti dikecualikan) dipakai meluas sbg ikon generik utk
   apa sahaja "luar negara/serantau/antarabangsa" — kajian penuh **89
  kejadian merentas 27 fail** (regex cari semua `globe_with_meridians_
  3d.png` + strip tag utk baca teks konteks) dedah kebanyakan MEMANG
  sesuai kekal generik (cth. "Kuasa Utama dalam Perang Dunia Kedua" —
  label kategori merangkumi BANYAK negara, bukan satu; "politik
  antarabangsa" — istilah abstrak; kesemua kes "British bertindak ke
  atas [Sabah/Sarawak/Tanah Melayu/gerakan nasionalisme kita]" — corak
  KEKAL DIKECUALIKAN sedia ada, "Negara Kita" sbg fokus naratif; "kaum
  Cina"/"orang India"/"wakil orang Ceylon"/dll — komuniti ETNIK dlm
  Tanah Melayu, BUKAN identiti negara asing; "bahasa Inggeris"/"sekolah
  Inggeris" — deskriptor bahasa, bukan negara; "Krisis Manchuria" —
  disahkan KEKAL ikut keputusan sedia ada, Sushi+globe dwi-ikon betul).

  **20 kejadian merentas 10 fail** disahkan patut ditukar kpd bendera
  (chip/point-line/point-heading/strip-sub yg teksnya secara eksplisit
  namakan SATU negara berdaulat sedia-ada-bendera sbg fokus/subjek,
  walau kadang kedudukan tatabahasa jadi objek — ikut precedent
  "Sekatan Ekonomi terhadap Jepun"/"Garisan Masa Serangan Jepun" drpd
  pusingan lalu):
  - `bab-1-2.html` — "Melaka turut diiktiraf oleh **Dinasti Ming**"
    → `cn.svg` (dinasti historis ↔ China, sama logik "Empayar
    Uthmaniyah" ↔ Turki drpd pusingan lalu).
  - `bab-2-2.html` — kad "Kesudahan Revolusi Amerika" ("...bergabung
    menjadi **Amerika Syarikat**...") → `us.svg`; kad "Kesudahan
    Revolusi Perancis" ("**Republik Perancis** ditubuhkan...") →
    `fr.svg`.
  - `bab-2-3.html` — accordion "Kemerdekaan India dan Pakistan" (dah
    ada dwi-bendera `in.svg`+`pk.svg` pd header) — 2 CHIP anak
    "14 Ogos 1947 – Pakistan merdeka" & "15 Ogos 1947 – India merdeka"
    yg SEBELUM ni terlepas drpd bendera header → `pk.svg`/`in.svg`
    masing-masing (header dwi-bendera BUKAN automatik terpakai kpd
    chip anak — setiap chip perlu ikon sendiri).
  - `bab-2-4.html` — "**Filipina** kemudian diletakkan di bawah
    penguasaan Amerika Syarikat" → `ph.svg`; "**Vietnam Selatan**
    (Saigon) masih di bawah pengaruh Perancis dan Amerika Syarikat" →
    `vn.svg` (padan bendera accordion induk "Kesudahan perjuangan di
    Vietnam"); 3 chip "Penasihat **Britain** – kewangan..."/"Penasihat
    **Amerika** – kastam"/"Penasihat **Perancis** – ketenteraan"
    (corak "Penasihat NEGARA – ringkasan") → `gb.svg`/`us.svg`/`fr.svg`.
  - `bab-2-6.html` — "**Revolusi China** – Dr. Sun Yat Sen..." →
    `cn.svg`; "gerakan nasionalisme di **Filipina dan Indonesia** –
    memberi inspirasi..." (kes asal tangkapan skrin pengguna, dwi-ikon
    🌐🌐 sedia ada digantikan dwi-bendera) → `ph.svg`+`id.svg`.
  - `bab-2-8.html` — sub-tajuk `.paper-strip.strip-sub` "**Kesedaran
    Politik India**" (dlm accordion gabungan China+India, header
    accordion kekal ikon generik sbb liputi 2 negara) → `in.svg`.
  - `bab-3-2.html` — accordion "A. Keruntuhan Pemerintahan Beraja"
    (Jerman/Austria-Hungary/Rusia dah berbendera drpd pusingan lalu,
    TAPI 2 chip "**Empayar Uthmaniyah** → Sultan Mehmed VI
    digulingkan" & "**Turki** → lahir Republik Turki..." terlepas) →
    `tr.svg` kedua-duanya; accordion "B. Kemunculan Negara Baharu" —
    3 tajuk `point-heading` pengenalan sub-senarai "Daripada
    **Austria-Hungary**:"/"Daripada **Empayar Rusia**:"/"Daripada
    **Empayar Uthmaniyah**:" (anak-anak chip senarai di bawah SETIAP
    satu dah berbendera individu drpd pusingan lalu, tajuk pengenalan
    sendiri terlepas) → dwi `at.svg`+`hu.svg` (turut buang ikon Hibiscus
    dekoratif tak relevan yg tersasar di situ), `ru.svg`, `tr.svg`.
  - `bab-3-3.html` — chip "menjadi titik tolak **pembebasan
    Perancis**" (dlm kad "Kejayaan ini:" susulan D-Day, sibling chip
    "membantu membebaskan negara-negara Eropah Barat" KEKAL generik
    sbb merangkumi BANYAK negara) → `fr.svg`.
  - `bab-3-4.html` — chip "1937 — Jepun menduduki **China**" (dlm
    senarai "Peluasan Kuasa Jepun", sibling "1910 — Jepun menguasai
    Korea" & chip senarai "Korea" DIKEKALKAN buat masa ini — Korea
    tiada svg bendera lagi dlm `assets/flags/`, DAN berpecah 2 negara
    moden [Korea Utara/Selatan] sejak 1948, jadi tiada "1 bendera yg
    betul" utk rujukan sejarah era 1910–1940-an bersatu — SAMA kelas
    isu Czechoslovakia/Yugoslavia drpd pusingan lalu, perlu tanya user
    dulu sebelum tambah, BUKAN keputusan mekanikal) → `cn.svg`.
  - `bab-6-3.html` — chip senarai komposisi tentera "1 batalion
    **rejimen Fiji**" (sibling "25 ribu askar Britain"/"10 ribu askar
    Gurkha" guna ikon lain, "1 batalion askar Afrika" KEKAL generik
    benua) → `fj.svg` (svg sedia ada, tak pernah dipakai sebelum ni).

  **Susulan — Korea (2 kejadian di atas, `bab-3-4.html`) DITANYA kpd
  pengguna via `AskUserQuestion`** (2 pilihan: tambah bendera Korea
  Selatan `kr.svg` SEBAGAI rujukan lazim, ATAU kekalkan globe generik
  elak isu ketepatan sejarah). Pengguna pilih **tambah `kr.svg`** —
  ditarik drpd `circle-flags` (git proxy baca awanama, klon cetek
  `--depth 1`, salin `flags/kr.svg` ke `assets/flags/`, padam klon
  lepas siap, sama corak drpd bendera baharu sebelum ni — LICENSE.md
  sedia ada sudah cukup, MIT sama). Kedua-dua chip "Korea" (senarai
  "Jepun mewujudkan orde baharu...") & "1910 — Jepun menguasai Korea"
  (senarai "Peluasan Kuasa Jepun") kini `kr.svg`. Skop semasa selepas
  pusingan 3 + susulan Korea: **46 negara** (rujuk `assets/flags/`,
  +1 baharu `kr.svg`).

  Disahkan selepas edit: `python3 scripts/seo-audit.py` &
  `python3 scripts/check-zh-coverage.py` kekal 100% lulus (elemen
  disunting cuma tukar `src`/kelas `<img>`, tiada `data-zh-unit-id`
  disentuh), semua 13 laluan `assets/flags/*.svg` dirujuk sedia wujud
  (`ls assets/flags/` sebelum edit — tiada svg baharu diperlukan
  pusingan ni, kesemua 13 negara/kod [`cn`,`us`,`fr`,`pk`,`in`,`ph`,
  `vn`,`gb`,`tr`,`at`,`hu`,`ru`,`fj`] sudah ada drpd pusingan lalu),
  Playwright pratonton visual (`bab-2-6.html` dwi-bendera Filipina+
  Indonesia, `bab-3-2.html` accordion "B" dwi-bendera Austria-Hungary
  + bendera Rusia/Turki pd tajuk pengenalan) sahkan render betul.
  **66 kejadian 🌐 BAKI** (turun drpd 89 — 20 pusingan 3 + 2 susulan
  Korea) disahkan SEMUA kekal betul ikut klasifikasi di atas (generik
  sengaja/dikecualikan/komuniti etnik/deskriptor bahasa) — bukan
  terlepas pandang.

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

## Infografik Galeri — FAB berasingan, carousel skrin penuh

Ciri BAHARU (2026-08-11): kad infografik gaya carousel media sosial
(imej cerita ilustrasi bergaya "Instagram carousel", diselang-selikan
dgn kandungan teks nota sedia ada) — utk pelajar visual & guru
membentang via projektor kelas. **Skop semasa: 2 subtopik (`bab-1-1`,
`bab-1-2`), 10 slaid setiap satu** — `bab-1-2` (2026-08-12) mengesahkan
corak `HZ_INFOGRAPHIC_PAGES` generalize bersih ke subtopik kedua tanpa
ubah kod (cuma tambah satu entri data + fail WebP, sama proses persis
drpd bab-1-1). Peluasan ke subtopik lain kekal kerja akan datang (perlu
proses/mampatkan imej baharu tiap kali — rujuk langkah di bawah), BUKAN
automatik drpd struktur ciri ni.

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
