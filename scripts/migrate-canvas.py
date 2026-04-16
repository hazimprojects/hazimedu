#!/usr/bin/env python3
"""
migrate-canvas.py — Tambah atribut canvas-ready pada semua halaman subtopik.

Perubahan yang dibuat:
  • Tambah kelas cv-unit + data-cv-* pada Ringkasan, Soalan Utama, Fokus,
    content boards, accordion items, Kesimpulan, Rumusan Besar Bab
  • Balut kandungan dalam <div class="cv-unit-body">
  • Info/glossary nested dalam accordion panel → data-cv-collectible="false"
  • Semua paper-chip dan paper-kingdom → data-cv-collectible="false"
  • Tambah script Sortable.js dan canvas.js selepas main.js

Jalankan dari root repo:
  python3 scripts/migrate-canvas.py
"""

import os
import re
import glob
from bs4 import BeautifulSoup, Tag, NavigableString

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
NOTES_DIR  = os.path.join(SCRIPT_DIR, '..', 'notes')


# ── Helpers ──────────────────────────────────────────────────────────────────

def subtopic_code(filename):
    """bab-1-1.html → '1.1'"""
    m = re.match(r'bab-(\d+)-(\d+)\.html$', filename)
    return f"{m.group(1)}.{m.group(2)}" if m else None


def chapter_num(filename):
    """bab-1-1.html → '1'"""
    m = re.match(r'bab-(\d+)-\d+\.html$', filename)
    return m.group(1) if m else None


def add_cv_attrs(el, cv_type, cv_title):
    """Tambah kelas cv-unit dan data-cv-* pada elemen."""
    classes = list(el.get('class', []))
    if 'cv-unit' not in classes:
        classes.append('cv-unit')
    el['class'] = classes
    el['data-cv-collectible'] = 'true'
    el['data-cv-type'] = cv_type
    el['data-cv-title'] = cv_title


def get_paper_strip(el):
    """Cari paper-strip anak terus (bukan rekursif)."""
    for child in el.children:
        if isinstance(child, Tag) and 'paper-strip' in child.get('class', []):
            return child
    return None


def wrap_after(soup, parent, after_el=None):
    """
    Balut anak-anak parent dalam cv-unit-body.
    Jika after_el diberikan, hanya balut anak selepas after_el.
    Jika after_el=None, balut semua anak.
    """
    to_move = []
    collecting = (after_el is None)

    for child in list(parent.children):
        if not collecting:
            if child is after_el:
                collecting = True
            continue
        to_move.append(child)

    if not to_move:
        return

    cv_body = soup.new_tag('div', **{'class': 'cv-unit-body'})
    for child in to_move:
        child.extract()
    parent.append(cv_body)
    for child in to_move:
        cv_body.append(child)


def derive_title(article, fallback=''):
    """
    Hasilkan cv-title untuk content board biasa.
    Keutamaan: paper-strip > section-heading h2 > h2 dalam article > fallback.
    """
    strip = get_paper_strip(article)
    if strip:
        return strip.get_text(strip=True)

    parent_sec = article.find_parent('section')
    if parent_sec:
        heading = parent_sec.find(class_='section-heading')
        if heading:
            h2 = heading.find('h2')
            if h2:
                return h2.get_text(strip=True)

    h2 = article.find('h2')
    if h2:
        return h2.get_text(strip=True)

    return fallback


# ── Main processor ────────────────────────────────────────────────────────────

def process_file(filepath):
    filename = os.path.basename(filepath)
    code = subtopic_code(filename)
    chap = chapter_num(filename)
    if not code:
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Skip jika sudah diproses sebelum ini
    if soup.find(class_='cv-unit'):
        return True

    done = set()   # id() bagi article yang sudah diproses


    # 1. Ringkasan ─────────────────────────────────────────────────────────────
    ring = soup.find(id='mula-nota')
    if ring and ring.name == 'article':
        add_cv_attrs(ring, 'board', f'Ringkasan {code}')
        strip = get_paper_strip(ring)
        wrap_after(soup, ring, after_el=strip)
        done.add(id(ring))


    # 2. Soalan Utama ──────────────────────────────────────────────────────────
    flap = soup.find(class_='paper-flap-card')
    if flap and flap.name == 'article':
        add_cv_attrs(flap, 'flap', f'Soalan Utama {code}')
        # Balut answer-paper dalam cv-unit-body (soalan kekal di luar)
        answer = flap.find(class_='answer-paper')
        if answer:
            cv_body = soup.new_tag('div', **{'class': 'cv-unit-body'})
            answer.wrap(cv_body)
        done.add(id(flap))


    # 3. Fokus ─────────────────────────────────────────────────────────────────
    for art in soup.find_all('article', class_='paper-board'):
        if id(art) in done:
            continue
        strip = get_paper_strip(art)
        if strip and 'Fokus' in strip.get_text():
            add_cv_attrs(art, 'board', f'Fokus {code}')
            wrap_after(soup, art, after_el=strip)
            done.add(id(art))
            break


    # 4. Accordion items ───────────────────────────────────────────────────────
    for item in soup.find_all('article', class_='paper-accordion-item'):
        title_el = item.find(class_='paper-accordion-title')
        cv_title = title_el.get_text(strip=True) if title_el else f'Kandungan {code}'
        add_cv_attrs(item, 'accordion', cv_title)

        panel = item.find(class_='paper-accordion-panel')
        if panel:
            # Tandakan info/glossary nested sebagai tidak boleh dikutip
            for nested in panel.find_all('article'):
                if set(nested.get('class', [])) & {'info-paper', 'glossary-paper'}:
                    nested['data-cv-collectible'] = 'false'
            # Balut semua kandungan panel dalam cv-unit-body
            wrap_after(soup, panel, after_el=None)

        done.add(id(item))


    # 5. Kesimpulan ────────────────────────────────────────────────────────────
    for art in soup.find_all('article'):
        if id(art) in done:
            continue
        classes = art.get('class', [])
        strip   = get_paper_strip(art)
        is_conc = 'conclusion-paper' in classes or (
            strip and 'Kesimpulan' in strip.get_text()
        )
        if is_conc:
            add_cv_attrs(art, 'board', f'Kesimpulan {code}')
            wrap_after(soup, art, after_el=strip)
            done.add(id(art))


    # 6. Rumusan Besar Bab (subtopik terakhir) ─────────────────────────────────
    for art in soup.find_all('article', class_='paper-board'):
        if id(art) in done:
            continue
        strip = get_paper_strip(art)
        if strip and 'Rumusan Besar' in strip.get_text():
            add_cv_attrs(art, 'board', f'Rumusan Besar Bab {chap}')
            wrap_after(soup, art, after_el=strip)
            done.add(id(art))


    # 7. Semua paper-board lain ────────────────────────────────────────────────
    for art in soup.find_all('article', class_='paper-board'):
        if id(art) in done:
            continue

        cls_set = set(art.get('class', []))
        is_info = bool(cls_set & {'info-paper', 'glossary-paper'})

        if is_info:
            in_accordion = bool(art.find_parent(class_='paper-accordion-panel'))
            if in_accordion:
                # Nested info → sudah ditanda dalam langkah 4, pastikan sekali lagi
                art['data-cv-collectible'] = 'false'
            else:
                # Standalone info → cv-unit tersendiri
                title = derive_title(art, fallback=f'Info {code}')
                add_cv_attrs(art, 'board', title)
                strip = get_paper_strip(art)
                wrap_after(soup, art, after_el=strip)
        else:
            # Content board biasa
            title = derive_title(art, fallback=f'Kandungan {code}')
            add_cv_attrs(art, 'board', title)
            strip = get_paper_strip(art)
            wrap_after(soup, art, after_el=strip)

        done.add(id(art))


    # 8. paper-chip → data-cv-collectible="false" ──────────────────────────────
    for chip in soup.find_all(class_='paper-chip'):
        if isinstance(chip, Tag):
            chip['data-cv-collectible'] = 'false'


    # 9. paper-kingdom → data-cv-collectible="false" ───────────────────────────
    for kingdom in soup.find_all('article', class_='paper-kingdom'):
        kingdom['data-cv-collectible'] = 'false'


    # 10. Tambah script Sortable.js dan canvas.js ──────────────────────────────
    main_script = None
    for s in soup.find_all('script'):
        if 'main.js' in (s.get('src') or ''):
            main_script = s
            break

    already_has_canvas = any(
        'canvas.js' in (s.get('src') or '')
        for s in soup.find_all('script')
    )

    if main_script and not already_has_canvas:
        sortable = soup.new_tag(
            'script',
            src='https://cdn.jsdelivr.net/npm/sortablejs@1.15.3/Sortable.min.js'
        )
        canvas = soup.new_tag('script', src='../assets/js/canvas.js?v=1')
        main_script.insert_after(canvas)
        main_script.insert_after(sortable)


    # Simpan ───────────────────────────────────────────────────────────────────
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    return True


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    pattern = os.path.join(NOTES_DIR, 'bab-*-*.html')
    files   = sorted(glob.glob(pattern))
    print(f"Ditemui {len(files)} fail untuk diproses...\n")
    ok = err = 0
    for fp in files:
        try:
            if process_file(fp):
                print(f"  ✓ {os.path.basename(fp)}")
                ok += 1
        except Exception as e:
            import traceback
            print(f"  ✗ {os.path.basename(fp)}: {e}")
            traceback.print_exc()
            err += 1
    print(f"\nSelesai: {ok} berjaya, {err} ralat")


if __name__ == '__main__':
    main()
