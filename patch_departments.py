import re

dept_logic = """
                            dept_keywords = ['development', 'research', 'chemistry', 'operations', 'lab', 'strategy', 'manufacturing', 'controls', 'platform', 'immunology', 'discovery', 'sciences', 'biology', 'engineering', 'analytics', 'regulatory', 'access', 'value', 'project', 'team', 'biochemistry', 'oncology', 'medical affairs', 'clinical', 'data', 'bioinformatics', 'computational', 'formulation', 'delivery', 'cmc', 'quality', 'assurance', 'qc', 'qa', 'market', 'commercial', 'sales', 'marketing', 'business', 'alliance', 'search', 'evaluation', 'innovation', 'technology']
                            company_keywords_ext = company_indicators + ['biotech', 'solutions', 'health', 'care', 'sanofi', 'pfizer', 'novartis', 'merck', 'janssen', 'astrazeneca', 'roche', 'abbvie', 'bayer', 'lilly', 'gsk', 'amgen', 'gilead', 'biogen', 'regeneron', 'vertex', 'moderna', 'biontech', 'takeda', 'daiichi', 'astellas', 'eisai', 'otsuka', 'sun', 'reddy', 'cipla', 'aurobindo', 'lupin', 'zydus', 'intas', 'torrent', 'biocon', 'glenmark', 'macleods', 'mankind', 'alchem', 'usv', 'wockhardt', 'group', 'partner', 'consulting', 'association', 'society', 'council', 'network', 'fund', 'foundation', 'ventures', 'capital', 'holdings', 'partners']
                            
                            if company.strip() != '':
                                c_lower = company.lower()
                                if not any(k in c_lower for k in company_keywords_ext):
                                    if any(dk in c_lower for dk in dept_keywords) and 'national research council' not in c_lower:
                                        title = title + ", " + company if title else company
                                        company = ""
"""

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
        
    start_py = content.find("if company.strip() == '':")
    if start_py != -1:
        
        end_if = content.find("summary = ", start_py)
        if end_if != -1:
            content = content[:end_if] + dept_logic.strip() + "\n                            \n                            " + content[end_if:]
            with open(filepath, 'w') as f:
                f.write(content)
                
patch_file('spiders/chi_spider.py')
patch_file('spiders/informa_spider.py')
patch_file('spiders/hanson_wade_spider.py')
print("Successfully patched all spiders with department logic.")
