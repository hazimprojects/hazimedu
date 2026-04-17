#!/usr/bin/env python3
"""Lint kualiti glosari BM -> ZH untuk kandungan Sejarah."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

DEFAULT_PATH = Path("data/zh-glossary.json")
META_KEYS = {"_meta", "_audit", "_editorial"}
GENERIC_BM_TERMS = {
    "bahasa",
    "politik",
    "agama",
    "kampung",
    "masyarakat",
    "penduduk",
    "kawasan",
    "bandar",
    "rakyat",
}


def lint_glossary(path: Path) -> list[str]:
    issues: list[str] = []

    if not path.is_file():
        return [f"{path}: fail tidak ditemui."]

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        return [f"{path}: JSON tidak sah ({err})."]

    if not isinstance(payload, dict):
        return [f"{path}: format root mesti objek JSON."]

    declared_general = {
        item.get("term", "").strip().lower()
        for item in (payload.get("_audit", {}) or {}).get("overly_general", [])
        if isinstance(item, dict) and isinstance(item.get("term"), str)
    }

    for raw_term, raw_value in payload.items():
        if raw_term in META_KEYS:
            continue

        if not isinstance(raw_term, str) or not raw_term.strip():
            issues.append(f"{path}: kunci istilah tidak sah: {raw_term!r}")
            continue

        term = raw_term.strip().lower()

        if not isinstance(raw_value, str) or not raw_value.strip():
            issues.append(f"{path}: istilah '{raw_term}' mempunyai padanan kosong/bukan teks.")
            continue

        value = raw_value.strip()

        if "/" in value:
            issues.append(
                f"{path}: istilah '{raw_term}' mengandungi padanan bercampur '{raw_value}'. Gunakan satu padanan utama sahaja."
            )

        if term in GENERIC_BM_TERMS and term not in declared_general:
            issues.append(
                f"{path}: istilah '{raw_term}' terlalu umum. Pecahkan ikut konteks sejarah (contoh: era/aktor/institusi)."
            )

        if re.search(r"\s{2,}", value):
            issues.append(f"{path}: istilah '{raw_term}' mempunyai jarak berganda pada nilai '{raw_value}'.")

    return issues


def main() -> int:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PATH
    failures = lint_glossary(target)

    if failures:
        print("Semakan glosari ZH gagal:")
        for item in failures:
            print(f" - {item}")
        return 1

    print(f"Semakan glosari ZH lulus untuk {target}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
