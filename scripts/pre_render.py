import os
import re
import subprocess

DISPLAY_NAMES = {
    "bayesian_inference": "ベイズ推論",
    "equilibrium_stat_mech": "平衡系統計力学",
    "information_geometry": "情報幾何学",
    "optimization_math": "最適化数学",
    "machine_learning_theory": "機械学習理論"
}

def get_display_name(name):
    return DISPLAY_NAMES.get(name, name)

def sort_key(filename):
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else 9999

def get_md_title(filepath, default_title):
    title = default_title
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as md_file:
            in_yaml = False
            for line in md_file:
                if line.strip() == "---":
                    in_yaml = not in_yaml
                    continue
                if in_yaml:
                    match = re.match(r'^title\s*:\s*(.*)', line)
                    if match:
                        title = match.group(1).strip().strip('"').strip("'")
                        break
                elif line.startswith("# "):
                    title = line[2:].strip()
                    break
    return title

def generate_in_progress():
    in_progress_dir = "InProgress"
    lines = []
    if os.path.exists(in_progress_dir):
        for root, dirs, files in os.walk(in_progress_dir):
            dirs.sort()
            for f in sorted(files):
                if f.endswith('.md'):
                    filepath = os.path.join(root, f)
                    title = get_md_title(filepath, f"({f} タイトル未設定)")
                    
                    rel_dir = os.path.relpath(root, in_progress_dir)
                    if rel_dir == ".":
                        lines.append(f"- {title}")
                    else:
                        display_dir = get_display_name(rel_dir)
                        lines.append(f"- 【{display_dir}】 {title}")
    
    with open("_generated/_in_progress.qmd", "w", encoding="utf-8") as f:
        if lines:
            f.write("\n".join(lines))
        else:
            f.write("現在執筆中のコンテンツはありません。")

def generate_published():
    published_dir = "Published"
    lines = ["::: {.grid}"]
    sidebar_yaml = ["website:", "  sidebar:", "    style: \"docked\"", "    contents:"]
    
    if os.path.exists(published_dir):
        for item in sorted(os.listdir(published_dir)):
            item_path = os.path.join(published_dir, item)
            if os.path.isdir(item_path):
                lines.append("::: {.g-col-12 .g-col-md-4}")
                
                logo_md = ""
                for ext in ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg', '.JPG', '.PNG', '.JPEG']:
                    logo_path = os.path.join(item_path, f"{item}{ext}")
                    if os.path.exists(logo_path):
                        logo_rel = f"Published/{item}/{item}{ext}"
                        logo_md = f"<img src='{logo_rel}' width='40' style='vertical-align: middle; border-radius: 50%; margin-right: 8px;'/>"
                        break
                
                md_files = []
                for root, dirs, files in os.walk(item_path):
                    for f in files:
                        if f.endswith('.md'):
                            rel_path = os.path.relpath(os.path.join(root, f), item_path)
                            md_files.append(rel_path)
                            
                md_files.sort(key=lambda x: sort_key(os.path.basename(x)))
                
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
                        lines.append(f"### [{logo_md}{get_display_name(item)}]({first_article})")
                    else:
                        lines.append(f"### {logo_md}{get_display_name(item)}")
                    for sec_name in sections.keys():
                        if sec_name != "":
                            first_sec_art = f"Published/{item}/{sections[sec_name][0]}"
                            
                            sec_logo_md = ""
                            sec_dir = os.path.join(item_path, sec_name)
                            for ext in ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg', '.JPG', '.PNG', '.JPEG']:
                                sec_logo_path = os.path.join(sec_dir, f"{sec_name}{ext}")
                                if os.path.exists(sec_logo_path):
                                    sec_logo_rel = f"Published/{item}/{sec_name}/{sec_name}{ext}"
                                    sec_logo_md = f"<img src='{sec_logo_rel}' width='20' style='vertical-align: middle; border-radius: 50%; margin-right: 5px;'/>"
                                    break
                            
                            lines.append(f"- {sec_logo_md}[{get_display_name(sec_name)}]({first_sec_art})")
                else:
                    lines.append(f"### {logo_md}{get_display_name(item)} (記事なし)")
                lines.append(":::")
                lines.append("")
                    
                sidebar_yaml.append(f"      - section: \"{get_display_name(item)}\"")
                sidebar_yaml.append(f"        contents:")
                
                if "" in sections:
                    for md in sections[""]:
                        md_clean = md.replace('\\', '/')
                        title = get_md_title(os.path.join(item_path, md), md_clean)
                        sidebar_yaml.append(f"          - text: \"{title}\"")
                        sidebar_yaml.append(f"            href: Published/{item}/{md_clean}")
                
                for sec_name, sec_mds in sections.items():
                    if sec_name != "":
                        sidebar_yaml.append(f"          - section: \"{get_display_name(sec_name)}\"")
                        sidebar_yaml.append(f"            contents:")
                        for md in sec_mds:
                            md_clean = md.replace('\\', '/')
                            title = get_md_title(os.path.join(item_path, md), md_clean)
                            sidebar_yaml.append(f"              - text: \"{title}\"")
                            sidebar_yaml.append(f"                href: Published/{item}/{md_clean}")
        
        lines.append(":::")
    
    with open("_generated/_sidebars.yml", "w", encoding="utf-8") as f:
        f.write("\n".join(sidebar_yaml))
    
    with open("_generated/_published_dirs.qmd", "w", encoding="utf-8") as f:
        if lines:
            f.write("\n\n".join(lines))
        else:
            f.write("現在公開中のコンテンツはありません。")

def generate_git_history():
    try:
        result = subprocess.run(
            ['git', 'log', '-10', '--format=- %cd: %s', '--date=short'],
            capture_output=True,
            text=True,
            check=True
        )
        history = result.stdout
    except Exception as e:
        history = f"履歴の取得に失敗しました: {e}"

    with open("_generated/_git_history.qmd", "w", encoding="utf-8") as f:
        if history.strip():
            f.write(history)
        else:
            f.write("履歴がありません。")

if __name__ == "__main__":
    os.makedirs("_generated", exist_ok=True)
    generate_in_progress()
    generate_published()
    generate_git_history()
