import glob
import os
import re

# Configuration
MAIN_LANG = "zh-hant"  # Base files have no suffix or primary extension
TARGET_LANGS = ["en"]  # Suffixes to check, e.g., '.en.qmd'

# Banner to insert after YAML header
CALLOUT_BANNER = """::: {.callout-note}
### 🚧 Under Construction / 建設中  {.under-construction .unnumbered}

This page is not yet fully translated into English. Below is the original content for reference.
:::

"""


def find_main_qmd_files():
    """Find all main .qmd files excluding localized target files and output dirs."""
    all_qmd = glob.glob("**/*.qmd", recursive=True)
    main_files = []

    for filepath in all_qmd:
        # Ignore files inside _book, _site, or .quarto directories
        if any(
            ignored in filepath.split(os.sep)
            for ignored in ["_book", "_site", ".quarto"]
        ):
            continue

        # Check if file is already localized (e.g., ends with .en.qmd or .qmd)
        filename = os.path.basename(filepath)
        is_localized = any(
            filename.endswith(f".{lang}.qmd") for lang in TARGET_LANGS
        ) or filename.endswith(f".{MAIN_LANG}.qmd")

        if not is_localized:
            main_files.append(filepath)

    return main_files


def insert_callout_after_yaml(content, banner):
    """Inserts callout banner right after the frontmatter YAML block (between second ---)."""
    # Regex matching YAML header surrounded by ---
    yaml_pattern = re.compile(r"^(---\s*\n.*?\n---\s*\n)", re.DOTALL)
    match = yaml_pattern.match(content)

    if match:
        yaml_header = match.group(1)
        body = content[match.end() :]
        return yaml_header + "\n" + banner + body
    else:
        # If no YAML header exists, place banner at the very top
        return banner + content


def process_missing_translations():
    main_files = find_main_qmd_files()
    missing_count = 0

    print(f"🔍 Found {len(main_files)} main chapter files. Checking for missing translations...\n")

    for main_file in main_files:
        base_path, ext = os.path.splitext(main_file)

        for target_lang in TARGET_LANGS:
            target_file = f"{base_path}.{target_lang}.qmd"

            if not os.path.exists(target_file):
                missing_count += 1
                print(f"❌ Missing [{target_lang}]: {target_file}")
                
                # Prompt user
                user_input = (
                    input(
                        f"   👉 Create duplicate placeholder for '{target_file}' with 🚧 callout? (y/n/all): "
                    )
                    .strip()
                    .lower()
                )

                if user_input in ["y", "yes", "a", "all"]:
                    # Read original file content
                    with open(main_file, "r", encoding="utf-8") as f:
                        original_content = f.read()

                    # Insert callout
                    new_content = insert_callout_after_yaml(
                        original_content, CALLOUT_BANNER
                    )

                    # Write to localized target file
                    with open(target_file, "w", encoding="utf-8") as f:
                        f.write(new_content)

                    print(f"   ✅ Created: {target_file}\n")

                elif user_input == "skip_all":
                    print("Skipping remaining files.")
                    return
                else:
                    print(f"   ⏭️ Skipped: {target_file}\n")

    if missing_count == 0:
        print("✨ All target localized files are present!")
    else:
        print("🎉 Processing complete.")


if __name__ == "__main__":
    process_missing_translations()