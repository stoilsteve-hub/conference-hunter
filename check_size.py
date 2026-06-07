import pandas as pd
import os
if os.path.exists('conference_data.xlsx'):
    df = pd.read_excel('conference_data.xlsx')
    print(f'Current rows: {len(df)}')
else:
    print('File not yet created')
