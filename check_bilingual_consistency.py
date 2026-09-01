#!/usr/bin/env python3
"""
Bilingual Quarto consistency checker.

Compares a primary-language .qmd file against its paired _en.qmd (or other
suffix) translation and reports:
  - Header (##, ###, etc.) count mismatches per level
  - Anchor IDs (#nte-, #imp-, #tip-, #sec-, and any other #id- pattern found
    in {.unnumbered #id} or {#id title=...} callout/header attributes)
    present in one file but missing in the other
  - Cross-reference targets (e.g. appendix-glossary.qmd#def-mental-fill-in,
    @fig-mindmap-06) present in one file but missing in the other

Usage:
    python check_bilingual_consistency.py FILE_A.qmd FILE_B.qmd
    python check_bilingual_consistency.py --dir . --pairs           # auto-pair *_en.qmd with base

Exit code is non-zero if any mismatch is found (useful in CI / pre-commit).
"""

import argparse
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field


HEADER_RE = re.compile(r'^(#{1,6})\s+(.*)$', re.MULTILINE)
# Matches #anchor-id inside {...} attribute blocks (headers, callouts, divs)
ATTR_ID_RE = re.compile(r'\{[^}]*?#([A-Za-z][\w:-]*)[^}]*\}')
# Matches cross-reference targets: @fig-xxx, @sec-xxx, @tbl-xxx, @def-xxx etc.
CROSSREF_AT_RE = re.compile(r'@([A-Za-z]+-[\w-]+)')
# Matches inline links to other files with an anchor: file.qmd#anchor-id
FILE_ANCHOR_RE = re.compile(r'\(([\w./-]+\.qmd)#([\w-]+)\)')

ANCHOR_PREFIXES = ("nte-", "imp-", "tip-", "sec-")


@dataclass
class FileReport:
    path: str
    header_levels: dict = field(default_factory=dict)   # level -> count
    headers: list = field(default_factory=list)          # (level, text)
    anchor_ids: set = field(default_factory=set)          # all #id from {...}
    tracked_anchors: set = field(default_factory=set)     # subset matching ANCHOR_PREFIXES
    at_crossrefs: set = field(default_factory=set)        # @sec-xxx style
    file_anchor_refs: set = field(default_factory=set)    # file.qmd#anchor style


def parse_file(path: Path) -> FileReport:
    text = path.read_text(encoding="utf-8")
    rep = FileReport(path=str(path))

    for m in HEADER_RE.finditer(text):
        level = len(m.group(1))
        title = m.group(2).strip()
        rep.headers.append((level, title))
        rep.header_levels[level] = rep.header_levels.get(level, 0) + 1

    for m in ATTR_ID_RE.finditer(text):
        aid = m.group(1)
        rep.anchor_ids.add(aid)
        if aid.startswith(ANCHOR_PREFIXES):
            rep.tracked_anchors.add(aid)

    for m in CROSSREF_AT_RE.finditer(text):
        rep.at_crossrefs.add(m.group(1))

    for m in FILE_ANCHOR_RE.finditer(text):
        rep.file_anchor_refs.add(f"{m.group(1)}#{m.group(2)}")

    return rep


def strip_leading_marks(title: str) -> str:
    """Strip emoji/symbol clutter loosely so header counts/order are comparable."""
    # Remove markdown formatting characters and unnumbered/id attrs already
    # stripped by HEADER_RE capture; just trim whitespace here.
    return title.strip()


def compare(a: FileReport, b: FileReport) -> int:
    problems = 0
    print(f"=== Comparing ===\nA: {a.path}\nB: {b.path}\n")

    # 1. Header level counts
    print("--- Header counts by level (##, ###, ...) ---")
    levels = sorted(set(a.header_levels) | set(b.header_levels))
    for lvl in levels:
        ca = a.header_levels.get(lvl, 0)
        cb = b.header_levels.get(lvl, 0)
        flag = "  <-- MISMATCH" if ca != cb else ""
        if ca != cb:
            problems += 1
        print(f"  H{lvl}: A={ca}  B={cb}{flag}")

    # 2. Section-by-section (## only) side-by-side, to localize the gap
    a_h2 = [t for lvl, t in a.headers if lvl == 2]
    b_h2 = [t for lvl, t in b.headers if lvl == 2]
    print(f"\n--- ## section list (A has {len(a_h2)}, B has {len(b_h2)}) ---")
    maxlen = max(len(a_h2), len(b_h2))
    for i in range(maxlen):
        at = a_h2[i] if i < len(a_h2) else "∅ MISSING"
        bt = b_h2[i] if i < len(b_h2) else "∅ MISSING"
        flag = "  <-- " if (i >= len(a_h2) or i >= len(b_h2)) else ""
        print(f"  [{i+1}] A: {at}\n       B: {bt}{flag}")
    if len(a_h2) != len(b_h2):
        problems += 1

    # 3. Tracked anchor IDs (nte-, imp-, tip-, sec-)
    print("\n--- Tracked anchors (#nte-, #imp-, #tip-, #sec-) ---")
    only_a = sorted(a.tracked_anchors - b.tracked_anchors)
    only_b = sorted(b.tracked_anchors - a.tracked_anchors)
    if only_a:
        problems += len(only_a)
        print(f"  In A only (missing from B): {only_a}")
    if only_b:
        problems += len(only_b)
        print(f"  In B only (missing from A): {only_b}")
    if not only_a and not only_b:
        print("  OK — identical sets:", sorted(a.tracked_anchors))

    # 4. Other (untracked) anchor IDs, reported but not counted as failures
    other_a = sorted(a.anchor_ids - a.tracked_anchors)
    other_b = sorted(b.anchor_ids - b.tracked_anchors)
    only_other_a = sorted(set(other_a) - set(other_b))
    only_other_b = sorted(set(other_b) - set(other_a))
    if only_other_a or only_other_b:
        print("\n--- Other anchor IDs present in only one file (info only) ---")
        if only_other_a:
            print(f"  In A only: {only_other_a}")
        if only_other_b:
            print(f"  In B only: {only_other_b}")

    # 5. @crossref targets (e.g. @fig-mindmap-06, @sec-tri-aspect-cognitive)
    print("\n--- @cross-reference targets ---")
    only_a = sorted(a.at_crossrefs - b.at_crossrefs)
    only_b = sorted(b.at_crossrefs - a.at_crossrefs)
    if only_a:
        problems += len(only_a)
        print(f"  In A only (missing from B): {only_a}")
    if only_b:
        problems += len(only_b)
        print(f"  In B only (missing from A): {only_b}")
    if not only_a and not only_b:
        print("  OK — identical sets:", sorted(a.at_crossrefs))

    # 6. file.qmd#anchor style links (e.g. appendix-glossary.qmd#def-mental-fill-in)
    print("\n--- file.qmd#anchor links ---")
    only_a = sorted(a.file_anchor_refs - b.file_anchor_refs)
    only_b = sorted(b.file_anchor_refs - a.file_anchor_refs)
    if only_a:
        problems += len(only_a)
        print(f"  In A only (missing from B): {only_a}")
    if only_b:
        problems += len(only_b)
        print(f"  In B only (missing from A): {only_b}")
    if not only_a and not only_b:
        print("  OK — identical sets:", sorted(a.file_anchor_refs))

    print(f"\n=== Total flagged discrepancies: {problems} ===")
    return problems


def auto_pairs(directory: Path):
    """Find base.qmd / base_en.qmd pairs in a directory."""
    en_files = sorted(directory.glob("*_en.qmd"))
    pairs = []
    for en in en_files:
        base_name = en.name[:-len("_en.qmd")] + ".qmd"
        base = directory / base_name
        if base.exists():
            pairs.append((base, en))
        else:
            print(f"[warn] No base pair found for {en.name}", file=sys.stderr)
    return pairs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", help="Two files to compare: FILE_A.qmd FILE_B.qmd")
    ap.add_argument("--dir", type=str, help="Directory to scan for *_en.qmd / base.qmd pairs")
    args = ap.parse_args()

    total_problems = 0
    pairs = []

    if args.dir:
        pairs = auto_pairs(Path(args.dir))
        if not pairs:
            print("No pairs found.", file=sys.stderr)
            sys.exit(1)
    elif len(args.files) == 2:
        pairs = [(Path(args.files[0]), Path(args.files[1]))]
    else:
        ap.print_help()
        sys.exit(1)

    for a_path, b_path in pairs:
        a = parse_file(a_path)
        b = parse_file(b_path)
        total_problems += compare(a, b)
        print("\n" + "=" * 60 + "\n")

    sys.exit(1 if total_problems > 0 else 0)


if __name__ == "__main__":
    main()
