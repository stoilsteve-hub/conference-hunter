import pandas as pd
import os

for f in ['conference_data.xlsx', 'conference_data_backup.xlsx', 'conference_data_old.xlsx']:
    try:
        df = pd.read_excel(f)
        print(f"{f}: {len(df)} rows")
    except Exception as e:
        print(f"{f}: CORRUPTED - {e}")
        
