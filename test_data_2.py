import pandas as pd
df = pd.read_excel('conference_data.xlsx')

def analyze_col(col_name):
    print(f"\n--- {col_name} ---")
    val_counts = df[col_name].value_counts()
    print(val_counts.head(10))

analyze_col('Speaker Company')
analyze_col('Speaker Job Title')
