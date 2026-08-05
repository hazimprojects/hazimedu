// Asas ringan (config-recommended) sengaja dipilih drpd config-standard —
// standard tambah banyak peraturan gaya (notasi warna, garis kosong antara
// rule, dll.) yg hasilkan >3000 isu kosmetik merentas 11k+ baris CSS sedia
// ada. Matlamat gate ni: tangkap CSS tak sah/rosak pada PR akan datang,
// BUKAN paksa tulis semula fail sedia ada.
module.exports = {
  extends: "stylelint-config-recommended",
  rules: {
    // Kedua-dua biasa & sengaja dlm CSS sedia ada (override tema
    // gelap/responsive reopen selector yg sama lewat dlm fail; specificity
    // bertindih antara komponen). Bukan bug — matlamat gate ni tangkap CSS
    // tak sah, bukan audit senibina cascade sedia ada.
    "no-descending-specificity": null,
    "no-duplicate-selectors": null,
  },
};
