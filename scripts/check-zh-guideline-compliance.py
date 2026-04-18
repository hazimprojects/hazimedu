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

TITLE_RE = re.compile(r"\b(?:Tun|Tunku|Tuanku|Dato'?|Datuk|Sultan|Raja)\s+[A-Z][\w'’.-]+(?:\s+[A-Z][\w'’.-]+){0,4}\b")
ACRO_RE = re.compile(r"\b[A-Z]{2,}(?:-[A-Z]{2,})?\b")
ZH_RE = re.compile(r"[\u4e00-\u9fff]")


def iter_units(payload: object):
    if isinstance(payload, dict) and isinstance(payload.get("units"), list):
        for unit in payload["units"]:
            if isinstance(unit, dict):
                yield unit


def extract_entities(text: str) -> list[str]:
    out: list[str] = []
    out.extend(TITLE_RE.findall(text))
    out.extend(ACRO_RE.findall(text))
    for fixed in ("Malayan Union", "Persekutuan Tanah Melayu", "Tanah Melayu", "Raja-raja Melayu"):
        if fixed in text:
            out.append(fixed)
    dedup: list[str] = []
    for item in out:
        if item not in dedup:
            dedup.append(item)
    return dedup


def malay_heavy(text: str) -> bool:
    lower = f" {text.lower()} "
    hits = sum(1 for token in MALAY_MARKERS if token in lower)
    return hits >= 3


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

            zh_count = len(ZH_RE.findall(zh))
            if zh_count < 4:
                issues.append(f"{path} -> {sid}: terjemahan terlalu sedikit aksara Cina.")

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
