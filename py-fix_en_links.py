#!/usr/bin/env python3
from pathlib import Path
import re
import sys

# Regex to capture markdown links: [text](target.qmd#section)
# Group 1: Link Text, Group 2: Base Target Filename, Group 3: Optional Anchor (#...)
LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+?\.qmd)(#[^)]+)?\)')

def forecast_and_fix(root_dir=".", execute=False):
    root_path = Path(root_dir)
    en_files = list(root_path.glob("**/*.en.qmd"))
    
    # Collect all existing filenames in repo for verification
    all_files = {f.name for f in root_path.glob("**/*")}

    total_replacements = 0
    files_modified = 0

    print(f"🔍 Scanning {len(en_files)} `.en.qmd` files (Mode: {'EXECUTE' if execute else 'FORECAST/DRY-RUN'})...\n")

    for file_path in en_files:
        content = file_path.read_text(encoding="utf-8")
        modified_content = content
        file_changes = 0

        def replace_link(match):
            nonlocal file_changes
            link_text = match.group(1)
            target = match.group(2)
            anchor = match.group(3) or ""

            # Skip external links or already correct .en.qmd targets
            if target.startswith(("http://", "https://")) or target.endswith(".en.qmd"):
                return match.group(0)

            # Construct proposed .en.qmd filename
            target_path = Path(target)
            en_target_name = f"{target_path.stem}.en.qmd"
            
            # Form relative path with .en.qmd extension
            if target_path.parent != Path("."):
                new_target = str(target_path.parent / en_target_name)
            else:
                new_target = en_target_name

            # Log forecasting info
            print(f"  📄 File: {file_path.relative_to(root_path)}")
            print(f"     Original: [{link_text}]({target}{anchor})")
            print(f"     Updated:  [{link_text}]({new_target}{anchor})")
            
            # Check if target .en.qmd actually exists on disk
            expected_file_name = Path(new_target).name
            if expected_file_name not in all_files:
                print(f"     ⚠️  WARNING: Target file '{expected_file_name}' not found on disk!")
            print()

            file_changes += 1
            return f"[{link_text}]({new_target}{anchor})"

        # Run replacement pass
        new_content = LINK_PATTERN.sub(replace_link, content)

        if file_changes > 0:
            total_replacements += file_changes
            files_modified += 1
            if execute:
                file_path.write_text(new_content, encoding="utf-8")

    print("=" * 60)
    print(f"📊 Summary:")
    print(f"   Files with broken links: {files_modified}")
    print(f"   Total link replacements: {total_replacements}")
    
    if not execute and total_replacements > 0:
        print("\n💡 This was a DRY RUN (forecast only). To apply changes, run:")
        print("   python3 fix_en_links.py --apply")

if __name__ == "__main__":
    should_apply = "--apply" in sys.argv
    forecast_and_fix(root_dir=".", execute=should_apply)