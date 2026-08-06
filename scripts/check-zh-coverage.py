#!/usr/bin/env python3
"""Semak liputan ID ZH antara notes HTML dan fail unit ZH."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict

NOTE_CHAPTER_RE = re.compile(r"^bab-(\d+)(?:-(\d+))?\.html$")
SOURCE_CHAPTER_RE = re.compile(r"^(?:bab-)?(\d+)(?:-(\d+))?-")
ZH_ID_RE = re.compile(r'data-zh-unit-id\s*=\s*(["\'])(.*?)\1', re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Semak padanan data-zh-unit-id (notes/*.html) vs source_id "
            "(data/zh-units/*.json), termasuk konflik source_id pendua."
        )
    )
    parser.add_argument(
        "--notes-dir",
        default="notes",
        help="Direktori fail notes HTML (lalai: notes)",
    )
    parser.add_argument(
        "--units-dir",
        default="data/zh-units",
        help="Direktori fail unit ZH JSON (lalai: data/zh-units)",
    )
    return parser.parse_args()


def chapter_from_note_filename(path: Path) -> str | None:
    match = NOTE_CHAPTER_RE.match(path.name)
    if not match:
        return None
    return f"Bab {int(match.group(1))}"


def chapter_from_source_id(source_id: str) -> str | None:
    match = SOURCE_CHAPTER_RE.match(source_id)
    if not match:
        return None
    return f"Bab {int(match.group(1))}"


def extract_note_ids(notes_dir: Path) -> tuple[set[str], dict[str, set[str]], list[str]]:
    note_ids: set[str] = set()
    note_ids_by_chapter: DefaultDict[str, set[str]] = defaultdict(set)
    errors: list[str] = []

    html_files = sorted(notes_dir.glob("*.html"))
    if not html_files:
        errors.append(f"Tiada fail HTML dijumpai di {notes_dir}")
        return note_ids, dict(note_ids_by_chapter), errors

    for path in html_files:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as err:
            errors.append(f"{path}: gagal baca fail ({err})")
            continue

        found_ids = {match.group(2).strip() for match in ZH_ID_RE.finditer(text) if match.group(2).strip()}
        note_ids.update(found_ids)

        chapter = chapter_from_note_filename(path)
        if chapter and found_ids:
            note_ids_by_chapter[chapter].update(found_ids)

    return note_ids, dict(note_ids_by_chapter), errors


def extract_source_ids(units_dir: Path) -> tuple[set[str], dict[str, set[str]], dict[str, set[str]], list[str]]:
    source_ids: set[str] = set()
    source_ids_by_chapter: DefaultDict[str, set[str]] = defaultdict(set)
    source_locations: DefaultDict[str, set[str]] = defaultdict(set)
    errors: list[str] = []

    json_files = sorted(path for path in units_dir.glob("*.json") if path.name != "index.json")
    if not json_files:
        errors.append(f"Tiada fail unit JSON dijumpai di {units_dir}")
        return source_ids, dict(source_ids_by_chapter), dict(source_locations), errors

    for path in json_files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as err:
            errors.append(f"{path}: JSON tidak sah / gagal baca ({err})")
            continue

        units = payload.get("units") if isinstance(payload, dict) else None
        if not isinstance(units, list):
            errors.append(f"{path}: format tidak sah, jangkaan objek dengan kunci 'units'.")
            continue

        for idx, unit in enumerate(units):
            if not isinstance(unit, dict):
                errors.append(f"{path}: unit indeks {idx} bukan objek.")
                continue

            source_id = unit.get("source_id")
            if not isinstance(source_id, str) or not source_id.strip():
                errors.append(f"{path}: unit indeks {idx} tiada source_id sah.")
                continue

            source_id = source_id.strip()
            source_ids.add(source_id)
            source_locations[source_id].add(path.name)

            chapter = chapter_from_source_id(source_id)
            if chapter:
                source_ids_by_chapter[chapter].add(source_id)

    return source_ids, dict(source_ids_by_chapter), dict(source_locations), errors


def format_list(values: list[str], limit: int = 30) -> list[str]:
    if len(values) <= limit:
        return values
    remaining = len(values) - limit
    return values[:limit] + [f"... (+{remaining} lagi)"]


def check_index_registration(units_dir: Path) -> tuple[list[str], list[str], list[str]]:
    """Sahkan data/zh-units/index.json (senarai fail SEBENAR yg zh-mode.js
    muat semasa runtime) padan tepat dgn fail *.json di disk.

    PUNCA bug sebenar (ditemui semasa siasatan pengguna): bab-8-2.json wujud
    di disk dgn 68 unit betul, check-zh-coverage.py laporkan 100% coverage
    (kerana extract_source_ids() imbas terus fail *.json di disk, bukan
    baca index.json) — tapi index.json TAK PERNAH disunting utk sebut
    "bab-8-2.json", jadi zh-mode.js (yg fetch ikut index.json sahaja, bukan
    imbas direktori) TAK PERNAH muat data tu. 100% coverage jadi angka palsu
    yg tak cerminkan realiti runtime. Semakan ni tutup jurang tu.
    """
    index_path = units_dir / "index.json"
    errors: list[str] = []
    unregistered: list[str] = []
    ghost: list[str] = []

    if not index_path.exists():
        errors.append(f"{index_path}: fail tidak wujud.")
        return errors, unregistered, ghost

    try:
        payload = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as err:
        errors.append(f"{index_path}: JSON tidak sah / gagal baca ({err})")
        return errors, unregistered, ghost

    listed = payload.get("files") if isinstance(payload, dict) else None
    if not isinstance(listed, list):
        errors.append(f"{index_path}: tiada kunci 'files' (senarai) yang sah.")
        return errors, unregistered, ghost

    listed_set = {name.strip() for name in listed if isinstance(name, str) and name.strip()}
    on_disk = {path.name for path in units_dir.glob("*.json") if path.name != "index.json"}

    unregistered = sorted(on_disk - listed_set)
    ghost = sorted(listed_set - on_disk)

    return errors, unregistered, ghost


def report_chapter_coverage(note_ids_by_chapter: dict[str, set[str]], source_ids: set[str]) -> None:
    print("\nLaporan liputan per bab:")
    print("-----------------------")

    if not note_ids_by_chapter:
        print("- Tiada data-zh-unit-id ditemui dalam notes/*.html")
        return

    for chapter in sorted(note_ids_by_chapter, key=lambda c: int(c.split()[1])):
        expected = note_ids_by_chapter[chapter]
        covered = expected & source_ids
        total = len(expected)
        percentage = (len(covered) / total * 100.0) if total else 0.0
        print(f"- {chapter}: {len(covered)}/{total} ({percentage:.1f}%)")


def main() -> int:
    args = parse_args()
    notes_dir = Path(args.notes_dir)
    units_dir = Path(args.units_dir)

    note_ids, note_ids_by_chapter, note_errors = extract_note_ids(notes_dir)
    source_ids, _, source_locations, source_errors = extract_source_ids(units_dir)

    missing_ids = sorted(note_ids - source_ids)
    extra_ids = sorted(source_ids - note_ids)
    duplicate_conflicts = sorted((sid, sorted(files)) for sid, files in source_locations.items() if len(files) > 1)
    index_errors, unregistered_files, ghost_files = check_index_registration(units_dir)

    has_error = bool(
        note_errors or source_errors or missing_ids or extra_ids or duplicate_conflicts
        or index_errors or unregistered_files or ghost_files
    )

    print("Ringkasan semakan ZH coverage")
    print("============================")
    print(f"Jumlah data-zh-unit-id (notes): {len(note_ids)}")
    print(f"Jumlah source_id (unit ZH):    {len(source_ids)}")

    report_chapter_coverage(note_ids_by_chapter, source_ids)

    if note_errors or source_errors:
        print("\nRalat pemprosesan:")
        for msg in note_errors + source_errors:
            print(f"- {msg}")

    if missing_ids:
        print("\nID hilang (ada di notes, tiada di unit ZH):")
        for source_id in format_list(missing_ids):
            print(f"- {source_id}")

    if extra_ids:
        print("\nID berlebihan (ada di unit ZH, tiada di notes):")
        for source_id in format_list(extra_ids):
            print(f"- {source_id}")

    if duplicate_conflicts:
        print("\nKonflik source_id pendua merentas fail unit:")
        for source_id, files in duplicate_conflicts:
            print(f"- {source_id}: {', '.join(files)}")

    if index_errors:
        print("\nRalat index.json:")
        for msg in index_errors:
            print(f"- {msg}")

    if unregistered_files:
        print("\nFail wujud di disk TAPI TIADA dlm index.json 'files' (zh-mode.js TAK PERNAH muat data ni):")
        for name in unregistered_files:
            print(f"- {name}")

    if ghost_files:
        print("\nFail disenaraikan dlm index.json TAPI TIADA di disk (zh-mode.js akan gagal fetch, 404):")
        for name in ghost_files:
            print(f"- {name}")

    if has_error:
        print("\nKeputusan: GAGAL (betulkan isu sebelum release).")
        return 1

    print("\nKeputusan: LULUS (coverage konsisten).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
