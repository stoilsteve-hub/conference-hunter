import pandas as pd
import os

if os.path.exists('conference_data.xlsx'):
    try:
        df = pd.read_excel('conference_data.xlsx')
        count = len(df)
        print(f"Total AI Extracted Speakers: {count}")
        
        if count > 0:
            print("\n--- Latest Extracted AI Data Sample ---")
            
            sample = df.tail(5)[['Speaker Full Name', 'Speaker Job Title', 'Speaker Company', 'Speaker Summary']]
            for _, row in sample.iterrows():
                print(f"Name:    {str(row['Speaker Full Name'])[:40]}")
                print(f"Title:   {str(row['Speaker Job Title'])[:60]}")
                print(f"Company: {str(row['Speaker Company'])[:40]}")
                summ_len = len(str(row['Speaker Summary']))
                print(f"Bio:     [Paragraph of {summ_len} chars]")
                print("-" * 50)
                
    except Exception as e:
        print(f"Error reading file (might be locked by exporter): {e}")
else:
    print("conference_data.xlsx not yet created.")
