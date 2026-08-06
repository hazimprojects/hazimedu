#!/usr/bin/env python3
"""Semakan pematuhan panduan editorial ZH untuk unit BM→ZH."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

FILES = sorted(Path("data/zh-units").glob("*.json"))

MALAY_MARKERS = (
    " ialah ",
    " yang ",
    " dan ",
    " dengan ",
    " kepada ",
    " oleh ",
    " untuk ",
    " dalam ",
    " kerana ",
    " selepas ",
    " terhadap ",
)

ACRO_RE = re.compile(r"\b[A-Z]{2,}(?:-[A-Z]{2,})?\b")
ZH_RE = re.compile(r"[\u4e00-\u9fff]")
UNPOLISHED_RE = re.compile(r"^\s*\u91ca\u4e49[\uff1a:]")


def iter_units(payload: object):
    if isinstance(payload, dict) and isinstance(payload.get("units"), list):
        for unit in payload["units"]:
            if isinstance(unit, dict):
                yield unit


def extract_entities(text: str) -> list[str]:
    out: list[str] = []
    out.extend(ACRO_RE.findall(text))
    # NOTA: TITLE_RE (nama Sultan/Tun/Tunku/Dato' dll.) SENGAJA dibuang drpd
    # senarai wajib-kekal ni — keputusan editorial (docs/zh-mode-editorial-
    # guideline.md §"Nama Orang & Gelaran") ialah nama orang MESTI
    # ditransliterasi ke aksara Cina + konteks kurungan, BUKAN dikekalkan
    # bentuk asal — jadi kehadiran nama asal BM dlm translate bukan lagi
    # kriteria yg betul (piawaian rasmi ialah 苏丹穆扎法沙（Sultan Muzaffar
    # Shah, konteks）, bukan Sultan Muzaffar Shah dikekalkan verbatim).
    # NOTA: "Tanah Melayu"/"Raja-raja Melayu" SENGAJA dibuang drpd senarai ni —
    # bukan nama khas (org rasmi/orang), terjemahan ke 马来亚/马来统治者 ialah
    # amalan BETUL, bukan pelanggaran (disahkan audit — 425 "pelanggaran" palsu).
    # "Malayan Union"/"Persekutuan Tanah Melayu" turut dibuang atas sebab sama —
    # istilah ni MEMANG patut diterjemah (马来亚联盟/马来亚联合邦), konsistensi
    # antara terjemahan diselia oleh data/zh-glossary.json, bukan semakan ni.
    dedup: list[str] = []
    for item in out:
        if item not in dedup:
            dedup.append(item)
    return dedup


def malay_heavy(text: str) -> bool:
    lower = f" {text.lower()} "
    hits = sum(1 for token in MALAY_MARKERS if token in lower)
    return hits >= 3


def translation_unpolished(zh: str) -> bool:
    """Kesan pembalut placeholder "释义：…（原文：…）" drpd enrich-zh-unit-translations.py.

    Panduan editorial sendiri terangkan corak ni sbg penanda kandungan BELUM
    disunting jadi ayat Cina lancar penuh — semakan tepat ni gantikan heuristik
    kiraan-aksara lama (lantai mutlak ≥4 aksara) yg terbukti hasilkan 2 jenis
    positif-palsu: frasa pendek yg SAH pendek (cth. "Jerman"→"德国"), DAN ayat
    panjang yg SAH tapi banyak nama khas dikekalkan asal (cth. "Kesultanan
    Melayu Melaka" dikekalkan ejaan asal, jadi nisbah aksara Cina rendah
    walaupun terjemahan betul).
    """
    return bool(UNPOLISHED_RE.match(zh))


def main() -> int:
    if not FILES:
        print("Tiada fail dijumpai di data/zh-units/*.json")
        return 1

    issues: list[str] = []

    for path in FILES:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as err:
            issues.append(f"{path}: JSON tidak sah ({err})")
            continue

        for unit in iter_units(payload):
            sid = unit.get("source_id", "<no-id>")
            bm = str(unit.get("bm_original", "")).strip()
            zh = str(unit.get("translate", "")).strip()
            if not bm or not zh:
                issues.append(f"{path} -> {sid}: bm_original/translate kosong.")
                continue

            if translation_unpolished(zh):
                issues.append(f"{path} -> {sid}: terjemahan masih placeholder \"释义：…（原文：…）\" — belum disunting jadi ayat Cina lancar.")

            if malay_heavy(zh):
                issues.append(f"{path} -> {sid}: terjemahan bercampur BM terlalu tinggi.")

            entities = extract_entities(bm)
            for ent in entities:
                if len(ent) < 3:
                    continue
                if ent not in zh:
                    issues.append(f"{path} -> {sid}: entiti '{ent}' tidak dikekalkan dalam translate.")

    if issues:
        print("Semakan pematuhan ZH gagal:")
        for item in issues[:200]:
            print(f" - {item}")
        if len(issues) > 200:
            print(f" ... dan {len(issues) - 200} isu lagi.")
        return 1

    print(f"Semakan pematuhan ZH lulus untuk {len(FILES)} fail.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
