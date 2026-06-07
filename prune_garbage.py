import pandas as pd

df = pd.read_excel('conference_data.xlsx')
initial_count = len(df)



garbage_words = ["PLENARY", "PEGS", "Sponsor", "Exhibitor", "Scenes from", "FIRESIDE CHAT"]

def is_garbage(row):
    name = str(row['Speaker Full Name']).upper()
    
    if pd.isna(row['Speaker Job Title']) and pd.isna(row['Speaker Company']):
        return True
        
    for word in garbage_words:
        if word.upper() in name:
            return True
            
    return False

df = df[~df.apply(is_garbage, axis=1)]

final_count = len(df)
df.to_excel('conference_data.xlsx', index=False)
print(f"Pruned {initial_count - final_count} garbage rows. Remaining speakers: {final_count}")
