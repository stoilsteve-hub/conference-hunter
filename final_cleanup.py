import pandas as pd

df = pd.read_excel('conference_data.xlsx')
original_len = len(df)

# Drop rows where Speaker First Name or Full Name is obviously a sentence (more than 5 words and no name indicators)
def is_garbage_name(name):
    name = str(name).strip()
    words = name.split()
    if len(words) > 6 and 'PhD' not in name and 'MD' not in name:
        return True
    lower = name.lower()
    if 'plenary fireside chat' in lower or 'alumni panel' in lower or 'welcome to' in lower or 'current trends' in lower or 'transformative tech' in lower or 'etourism moves' in lower:
        return True
    return False

df = df[~df['Speaker Full Name'].apply(is_garbage_name)]

# Fix 'Moderator: James Little'
def fix_moderator(name):
    name = str(name)
    if name.lower().startswith('moderator:'):
        return name[10:].strip()
    if name.lower().startswith('moderators:'):
        return name[11:].strip()
    return name

df['Speaker Full Name'] = df['Speaker Full Name'].apply(fix_moderator)
df['Speaker First Name'] = df['Speaker Full Name'].apply(lambda x: str(x).split()[0] if x else '')

print(f"Removed {original_len - len(df)} more garbage rows.")
print(f"Final clean database size: {len(df)}")

df.to_excel('conference_data.xlsx', index=False)
