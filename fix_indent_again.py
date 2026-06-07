def fix_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        
    out = []
    in_block = False
    for line in lines:
        if 'parts = [p.strip() for p in first_line.split(",")]' in line:
            in_block = True
            
        if in_block:
            stripped = line.lstrip()
            if not stripped:
                out.append('\n')
                continue
                
            
            if 'if "speaker" in name.lower() or "expand_more" in title.lower() or "@" in title or "bpicustomerservice" in title.lower(): continue' in line:
                out.append(' ' * 28 + stripped + '\n')
                in_block = False
                continue
                
            if 'if len(name) > 60 or "Archived Content" in name or any(char.isdigit() for char in name): continue' in line:
                out.append(' ' * 28 + stripped + '\n')
                continue
                
            
            if 'name = parts[0]' in line: out.append(' ' * 28 + stripped + '\n')
            elif 'title = ""' in line: out.append(' ' * 28 + stripped + '\n')
            elif 'company = ""' in line: out.append(' ' * 28 + stripped + '\n')
            elif 'if len(parts) > 1:' in line: out.append(' ' * 28 + stripped + '\n')
            elif 'if parts[1].upper() in' in line: out.append(' ' * 32 + stripped + '\n')
            elif 'name += ", " + parts[1]' in line: out.append(' ' * 36 + stripped + '\n')
            elif 'if len(parts) > 2:' in line: out.append(' ' * 36 + stripped + '\n')
            elif 'title = ", ".join(parts[2:-1])' in line: out.append(' ' * 40 + stripped + '\n')
            elif 'company = parts[-1]' in line: out.append(' ' * 40 + stripped + '\n')
            elif 'else:' in line: out.append(' ' * 32 + stripped + '\n')
            elif 'title = parts[1]' in line: out.append(' ' * 36 + stripped + '\n')
            elif 'company = ", ".join(parts[2:])' in line: out.append(' ' * 36 + stripped + '\n')
            elif 'company_indicators =' in line: out.append(' ' * 28 + stripped + '\n')
            elif 'title_indicators =' in line: out.append(' ' * 28 + stripped + '\n')
            elif 'if company.strip() == "":' in line: out.append(' ' * 28 + stripped + '\n')
            elif 'if any(ci in title.lower()' in line: out.append(' ' * 32 + stripped + '\n')
            elif 'company = title' in line: out.append(' ' * 36 + stripped + '\n')
            elif 'title = ""' in line: out.append(' ' * 36 + stripped + '\n')
            elif 'summary = "\\n".join(' in line: out.append(' ' * 28 + stripped + '\n')
            elif 'if summary.lower().startswith' in line: out.append(' ' * 28 + stripped + '\n')
            elif 'summary = summary[10:]' in line: out.append(' ' * 32 + stripped + '\n')
            elif 'if \'wayback machine\' in' in line: out.append(' ' * 28 + stripped + '\n')
            elif 'summary = \'\'' in line: out.append(' ' * 32 + stripped + '\n')
            else: out.append(' ' * 28 + stripped + '\n')
        else:
            out.append(line)
            
    with open(filepath, 'w') as f:
        f.writelines(out)

fix_file('spiders/chi_spider.py')
fix_file('spiders/informa_spider.py')
fix_file('spiders/hanson_wade_spider.py')
print("Fixed indentations.")
