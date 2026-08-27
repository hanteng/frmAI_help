import os
import sys
from pathlib import Path


def audit_quarto_manifest(project_dir="."):
    root = Path(project_dir).resolve()
    print(f"🔍 Auditing Quarto Manifest in: {root}\n")

    qmd_files = {}
    en_qmd_files = {}

    # Crawl repository for all .qmd files
    for path in root.rglob("*.qmd"):
        # Ignore hidden folders, _book, _site, etc.
        rel_parts = path.relative_to(root).parts
        if any(
            p.startswith(".") or p.startswith("_")
            for p in rel_parts[:-1]
            if p != "."
        ):
            continue

        rel_path_str = str(path.relative_to(root)).replace("\\", "/")

        if rel_path_str.endswith(".en.qmd"):
            en_qmd_files[rel_path_str.lower()] = rel_path_str
        else:
            qmd_files[rel_path_str.lower()] = rel_path_str

    print(f"📊 SUMMARY COUNTS:")
    print(f"  - Base (.qmd) files:     {len(qmd_files)}")
    print(f"  - English (.en.qmd) files: {len(en_qmd_files)}")
    print(f"  - Total indexed:          {len(qmd_files) + len(en_qmd_files)}\n")

    # Audit 1: Check expected pairing (Base -> .en.qmd)
    missing_en_translations = []
    matched_pairs = 0

    for lower_base, actual_base in qmd_files.items():
        expected_en_lower = lower_base[:-4] + ".en.qmd"
        if expected_en_lower in en_qmd_files:
            matched_pairs += 1
            actual_en = en_qmd_files[expected_en_lower]

            # Case check between base and translation prefix
            base_prefix = actual_base[:-4]
            en_prefix = actual_en[:-7]
            if base_prefix != en_prefix:
                print(
                    f"⚠️ CASE MISMATCH DETECTED:\n  Base: {actual_base}\n  EN:   {actual_en}"
                )
        else:
            missing_en_translations.append(actual_base)

    print(f"✅ Matched Base/EN Pairs: {matched_pairs}")
    print(f"❓ Base files WITHOUT .en.qmd translation: {len(missing_en_translations)}")

    # Audit 2: Orphan .en.qmd files (English file with no base .qmd)
    orphan_en = []
    for lower_en, actual_en in en_qmd_files.items():
        expected_base_lower = lower_en[:-7] + ".qmd"
        if expected_base_lower not in qmd_files:
            orphan_en.append(actual_en)

    if orphan_en:
        print(f"\n⚠️ ORPHAN .en.qmd FILES (No matching base .qmd found): {len(orphan_en)}")
        for orphan in orphan_en:
            print(f"  - {orphan}")

    # Audit 3: Case Collision Check (Files that differ ONLY by case)
    all_paths = list(qmd_files.values()) + list(en_qmd_files.values())
    seen_lower = {}
    case_collisions = []

    for path_str in all_paths:
        l_str = path_str.lower()
        if l_str in seen_lower and seen_lower[l_str] != path_str:
            case_collisions.append((seen_lower[l_str], path_str))
        else:
            seen_lower[l_str] = path_str

    if case_collisions:
        print(f"\n❌ CASE COLLISIONS FOUND ({len(case_collisions)}):")
        for f1, f2 in case_collisions:
            print(f"  - {f1} <--> {f2}")
    else:
        print("\n✅ Zero exact case-sensitivity collisions found across all files.")

    # Write CSV Manifest for inspection
    manifest_path = root / "quarto_file_manifest.csv"
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write("type,relative_path\n")
        for path_str in sorted(qmd_files.values()):
            f.write(f"base,{path_str}\n")
        for path_str in sorted(en_qmd_files.values()):
            f.write(f"english,{path_str}\n")

    print(f"\n📄 Manifest exported to: {manifest_path.name}")


if __name__ == "__main__":
    audit_quarto_manifest()