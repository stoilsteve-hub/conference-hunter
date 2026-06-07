import pandas as pd

df = pd.read_excel('safe_data.xlsx')

garbage_words = ["PLENARY", "PEGS", "Sponsor", "Exhibitor", "Scenes from", "FIRESIDE CHAT", "Break", "Lunch", "Networking", "Chair", "Panel", "Registration", "Coffee", "Welcome", "Closing", "Opening", "Reception"]

def is_garbage(row):
    name = str(row['Speaker Full Name']).upper()
    
    if pd.isna(row['Speaker Job Title']) and pd.isna(row['Speaker Company']):
        return True
        
    for word in garbage_words:
        if word.upper() in name:
            return True
            
    if len(name) < 3:
        return True
            
    return False

df_clean = df[~df.apply(is_garbage, axis=1)].copy()


df_clean.drop_duplicates(subset=['Speaker Full Name', 'Conference Name'], keep='first', inplace=True)

df_clean.to_excel('conference_data.xlsx', index=False)
print(f"Final completely clean dataset size: {len(df_clean)}")
