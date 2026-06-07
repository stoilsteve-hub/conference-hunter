def fix_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        
    out = []
    for line in lines:
        if 'dept_keywords =' in line or 'company_keywords_ext =' in line or "if company.strip() != '':" in line or 'c_lower = company.lower()' in line or 'if not any(k in c_lower for k in company_keywords_ext):' in line or "if any(dk in c_lower for dk in dept_keywords) and 'national research council' not in c_lower:" in line or 'title = title + ", " + company if title else company' in line or 'company = ""' in line:
            
            
            base = 16 if 'informa' in filepath else 28
            
            if 'dept_keywords =' in line or 'company_keywords_ext =' in line or "if company.strip() != '':" in line or 'company = ""' in line:
                out.append(' ' * base + line.strip() + '\n')
            elif 'c_lower = company.lower()' in line or 'if not any(k in c_lower for k in company_keywords_ext):' in line:
                out.append(' ' * (base + 4) + line.strip() + '\n')
            elif "if any(dk in c_lower for dk in dept_keywords)" in line:
                out.append(' ' * (base + 8) + line.strip() + '\n')
            elif 'title = title + ", " + company if title else company' in line:
                out.append(' ' * (base + 12) + line.strip() + '\n')
            else:
                out.append(' ' * base + line.strip() + '\n')
        else:
            out.append(line)
            
    with open(filepath, 'w') as f:
        f.writelines(out)

fix_file('spiders/chi_spider.py')
fix_file('spiders/informa_spider.py')
fix_file('spiders/hanson_wade_spider.py')
print("Fixed indentations.")
