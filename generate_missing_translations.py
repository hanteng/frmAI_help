import glob
import os
import re

MAIN_LANG = "zh-hant"
TARGET_LANGS = ["en"]

CALLOUT_BANNER = """::: {.callout-note}
🚧 Under Construction / 建設中  {.fs-3 .under-construction .unnumbered}

This page is not yet fully translated into English. Below is the original content for reference.
:::
"""

CHARCOUNT_BANNER_TEMPLATE = """::: {{.callout-tip}}
📊 Character Counts / 字數統計

- Chinese version: {zh_count} characters
- English version: {en_count} characters
:::
"""

def find_main_qmd_files():
    all_qmd = glob.glob("**/*.qmd", recursive=True)
    main_files = []
    for filepath in all_qmd:
        if any(ignored in filepath.split(os.sep) for ignored in ["_book", "_site", ".quarto"]):
            continue
        filename = os.path.basename(filepath)
        is_localized = any(filename.endswith(f".{lang}.qmd") for lang in TARGET_LANGS) or filename.endswith(f".{MAIN_LANG}.qmd")
        if not is_localized:
            main_files.append(filepath)
    return main_files

def split_yaml_and_body(content):
    """Return (yaml_header, body) if YAML exists, else ('', content)."""
    yaml_pattern = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)
    match = yaml_pattern.match(content)
    if match:
        return match.group(0), content[match.end():]
    else:
        return "", content

def count_characters(content):
    _, body = split_yaml_and_body(content)
    return len(body)

def insert_banners(content, banners):
    """Insert banners after YAML header, avoiding duplicates."""
    yaml_header, body = split_yaml_and_body(content)
    combined_banner = "\n".join(banners)
    if combined_banner in content:
        return content  # already inserted
    if yaml_header:
        return yaml_header + "\n" + combined_banner + "\n" + body
    else:
        return combined_banner + "\n" + content

def document_char_counts(main_file, target_file):
    with open(main_file, "r", encoding="utf-8") as f:
        zh_content = f.read()
    zh_count = count_characters(zh_content)

    if os.path.exists(target_file):
        with open(target_file, "r", encoding="utf-8") as f:
            en_content = f.read()
        en_count = count_characters(en_content)
        banner = CHARCOUNT_BANNER_TEMPLATE.format(zh_count=zh_count, en_count=en_count)
        new_content = insert_banners(en_content, [banner])
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"📊 Documented counts in: {target_file} (ZH={zh_count}, EN={en_count})")
    else:
        print(f"⚠️ No English file yet for: {main_file} (ZH={zh_count})")

def process_missing_translations():
    main_files = find_main_qmd_files()
    print(f"🔍 Found {len(main_files)} main chapter files. Checking translations and character counts...\n")

    for main_file in main_files:
        base_path, _ = os.path.splitext(main_file)
        for target_lang in TARGET_LANGS:
            target_file = f"{base_path}.{target_lang}.qmd"

            if not os.path.exists(target_file):
                print(f"❌ Missing [{target_lang}]: {target_file}")
                user_input = input(f"   👉 Create placeholder for '{target_file}'? (y/n/all): ").strip().lower()
                if user_input in ["y", "yes", "a", "all"]:
                    with open(main_file, "r", encoding="utf-8") as f:
                        original_content = f.read()
                    new_content = insert_banners(original_content, [CALLOUT_BANNER])
                    with open(target_file, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"   ✅ Created: {target_file}\n")

            document_char_counts(main_file, target_file)

if __name__ == "__main__":
    process_missing_translations()