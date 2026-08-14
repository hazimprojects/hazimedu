# Bendera Negara — Sejarah & Disiplin Penuh

> Dipecahkan drpd `CLAUDE.md` (2026-08-14) supaya fail utama kekal
> senang navigasi. Rujuk fail ni bila tambah/ubah bendera negara pd
> nota. Ringkasan AWAS penting kekal dlm `CLAUDE.md` — fail ni ialah
> rekod penuh keputusan & pengesahan setiap pusingan.

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

