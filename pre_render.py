import os
import re

def sort_key(filename):
    # ファイル名から数字を抽出（例： "1.md" -> 1）
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else 9999

def generate_in_progress():
    in_progress_dir = "InProgress"
    lines = []
    if os.path.exists(in_progress_dir):
        for item in sorted(os.listdir(in_progress_dir)):
            if os.path.isdir(os.path.join(in_progress_dir, item)):
                lines.append(f"- {item}")
    
    with open("_in_progress.qmd", "w", encoding="utf-8") as f:
        if lines:
            f.write("\n".join(lines))
        else:
            f.write("現在執筆中のコンテンツはありません。")

def generate_published():
    published_dir = "Published"
    lines = []
    
    if os.path.exists(published_dir):
        for item in sorted(os.listdir(published_dir)):
            item_path = os.path.join(published_dir, item)
            if os.path.isdir(item_path):
                # ロゴ画像の探索（ディレクトリ名と同名のPNG）
                logo_path = os.path.join(item_path, f"{item}.png")
                logo_rel = f"Published/{item}/{item}.png"
                
                logo_md = ""
                if os.path.exists(logo_path):
                    logo_md = f"<img src='{logo_rel}' width='50' style='vertical-align: middle; border-radius: 50%; margin-right: 10px;'/>"
                
                # Markdownファイルの取得とソート
                md_files = [f for f in os.listdir(item_path) if f.endswith('.md')]
                md_files.sort(key=sort_key)
                
                if md_files:
                    first_article = f"Published/{item}/{md_files[0]}"
                    lines.append(f"### [{logo_md}{item}]({first_article})")
                else:
                    lines.append(f"### {logo_md}{item} (記事なし)")
                    
                # ディレクトリごとのサイドバーナビゲーション用 _metadata.yml を生成
                metadata_path = os.path.join(item_path, "_metadata.yml")
                with open(metadata_path, "w", encoding="utf-8") as mf:
                    mf.write("sidebar:\n")
                    mf.write(f"  title: \"{item}\"\n")
                    mf.write("  style: \"docked\"\n")
                    mf.write("  contents:\n")
                    for md in md_files:
                        mf.write(f"    - \"{md}\"\n")
    
    with open("_published_dirs.qmd", "w", encoding="utf-8") as f:
        if lines:
            f.write("\n\n".join(lines))
        else:
            f.write("現在公開中のコンテンツはありません。")

if __name__ == "__main__":
    generate_in_progress()
    generate_published()
