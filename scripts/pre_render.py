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
        for root, dirs, files in os.walk(in_progress_dir):
            # フォルダやファイルをソートして順序を固定
            dirs.sort()
            for f in sorted(files):
                if f.endswith('.md'):
                    filepath = os.path.join(root, f)
                    title = f"({f} タイトル未設定)"
                    with open(filepath, "r", encoding="utf-8") as md_file:
                        for line in md_file:
                            if line.startswith("# "):
                                title = line[2:].strip()
                                break
                    
                    rel_dir = os.path.relpath(root, in_progress_dir)
                    if rel_dir == ".":
                        lines.append(f"- {title}")
                    else:
                        lines.append(f"- 【{rel_dir}】 {title}")
    
    with open("_generated/_in_progress.qmd", "w", encoding="utf-8") as f:
        if lines:
            f.write("\n".join(lines))
        else:
            f.write("現在執筆中のコンテンツはありません。")

def generate_published():
    published_dir = "Published"
    lines = []
    sidebar_yaml = ["website:", "  sidebar:", "    style: \"docked\"", "    contents:"]
    
    if os.path.exists(published_dir):
        for item in sorted(os.listdir(published_dir)):
            item_path = os.path.join(published_dir, item)
            if os.path.isdir(item_path):
                # ロゴ画像の探索（ディレクトリ名と同名の画像）
                logo_md = ""
                for ext in ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg', '.JPG', '.PNG', '.JPEG']:
                    logo_path = os.path.join(item_path, f"{item}{ext}")
                    if os.path.exists(logo_path):
                        logo_rel = f"Published/{item}/{item}{ext}"
                        logo_md = f"<img src='{logo_rel}' width='50' style='vertical-align: middle; border-radius: 50%; margin-right: 10px;'/>"
                        break
                
                # Markdownファイルの再帰的な取得とソート
                md_files = []
                for root, dirs, files in os.walk(item_path):
                    for f in files:
                        if f.endswith('.md'):
                            rel_path = os.path.relpath(os.path.join(root, f), item_path)
                            md_files.append(rel_path)
                            
                md_files.sort(key=lambda x: sort_key(os.path.basename(x)))
                
                # サブディレクトリでグループ化 (先に行う)
                from collections import defaultdict
                sections = defaultdict(list)
                for md in md_files:
                    parts = md.replace("\\", "/").split("/")
                    if len(parts) > 1:
                        section_name = parts[0]
                        sections[section_name].append(md)
                    else:
                        sections[""].append(md)

                if md_files:
                    if "" in sections:
                        root_art = sections[''][0].replace('\\', '/')
                        first_article = f"Published/{item}/{root_art}"
                        lines.append(f"### [{logo_md}{item}]({first_article})")
                    else:
                        lines.append(f"### {logo_md}{item}")
                    for sec_name in sections.keys():
                        if sec_name != "":
                            first_sec_art = f"Published/{item}/{sections[sec_name][0]}"
                            
                            # サブディレクトリのロゴ探索
                            sec_logo_md = ""
                            sec_dir = os.path.join(item_path, sec_name)
                            for ext in ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg', '.JPG', '.PNG', '.JPEG']:
                                sec_logo_path = os.path.join(sec_dir, f"{sec_name}{ext}")
                                if os.path.exists(sec_logo_path):
                                    sec_logo_rel = f"Published/{item}/{sec_name}/{sec_name}{ext}"
                                    sec_logo_md = f"<img src='{sec_logo_rel}' width='30' style='vertical-align: middle; border-radius: 50%; margin-right: 5px;'/>"
                                    break
                            
                            lines.append(f"- {sec_logo_md}[{sec_name}]({first_sec_art})")
                else:
                    lines.append(f"### {logo_md}{item} (記事なし)")
                    

                # グローバルサイドバーのセクション構成
                sidebar_yaml.append(f"      - section: \"{item}\"")
                sidebar_yaml.append(f"        contents:")
                
                # ルート直下のファイルを先に出力
                if "" in sections:
                    for md in sections[""]:
                        md_clean = md.replace('\\', '/')
                        sidebar_yaml.append(f"          - \"Published/{item}/{md_clean}\"")
                
                # サブディレクトリごとのセクションを出力
                for sec_name, sec_mds in sections.items():
                    if sec_name != "":
                        sidebar_yaml.append(f"          - section: \"{sec_name}\"")
                        sidebar_yaml.append(f"            contents:")
                        for md in sec_mds:
                            md_clean = md.replace('\\', '/')
                            sidebar_yaml.append(f"              - \"Published/{item}/{md_clean}\"")
    
    with open("_generated/_sidebars.yml", "w", encoding="utf-8") as f:
        f.write("\n".join(sidebar_yaml))
    
    with open("_generated/_published_dirs.qmd", "w", encoding="utf-8") as f:
        if lines:
            f.write("\n\n".join(lines))
        else:
            f.write("現在公開中のコンテンツはありません。")

if __name__ == "__main__":
    generate_in_progress()
    generate_published()
