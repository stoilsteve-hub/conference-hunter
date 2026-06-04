import pandas as pd
import re

def clean_data():
    df = pd.read_excel('conference_data.xlsx')
    
    # 1. Annihilate Indonesian Spam and 404s
    spam_keywords = r'(Katsu5|slot online|RTP live|Result Macau|togel macau|does not exist or has been moved)'
    mask_spam = df['Speaker Summary'].astype(str).str.contains(spam_keywords, case=False, na=False)
    df.loc[mask_spam, 'Speaker Summary'] = ""
    print(f"Cleared {mask_spam.sum()} Indonesian spam / 404 errors from Summary.")

    # 2. Annihilate Location/Address Boilerplate
    address_keywords = r'(Hotel Circle|San Diego, CA|Seoul, South Korea|Boston, MA|Commonwealth Avenue|Edwin Land Boulevard|Huntington Avenue|Summer Street|Westin Boston)'
    mask_addr = df['Speaker Summary'].astype(str).str.contains(address_keywords, case=False, na=False)
    df.loc[mask_addr, 'Speaker Summary'] = ""
    print(f"Cleared {mask_addr.sum()} address/hotel boilerplate entries from Summary.")

    # 3. Annihilate Marketing Boilerplate
    marketing_keywords = r'(Returning September|Next in the Series|Komt dat zien|Advancing Construction|Your Flagship, Global Conference|Industry Update:)'
    mask_mkt = df['Speaker Summary'].astype(str).str.contains(marketing_keywords, case=False, na=False)
    df.loc[mask_mkt, 'Speaker Summary'] = ""
    print(f"Cleared {mask_mkt.sum()} marketing boilerplate entries from Summary.")
    
    # Same for Presentation Title
    mask_mkt_title = df['Presentation Title'].astype(str).str.contains(marketing_keywords, case=False, na=False)
    df.loc[mask_mkt_title, 'Presentation Title'] = ""
    
    # 4. If Summary is exactly equal to "Sanofi", "Biogen", "Merck", etc, move it to Company!
    companies = ['Sanofi', 'Biogen', 'Merck']
    for comp in companies:
        mask_comp = df['Speaker Summary'].astype(str).str.strip() == comp
        for i, row in df[mask_comp].iterrows():
            if pd.isna(row['Speaker Company']) or str(row['Speaker Company']).strip() == "":
                df.at[i, 'Speaker Company'] = comp
            df.at[i, 'Speaker Summary'] = ""
            
    # 5. Fix Presentation Title "Panel Discussion" if it's literally just "Panel Discussion"
    # Actually, the user's screenshot shows "Panel Discussion" as a Presentation Title. That's probably valid!
    # BUT wait, the user's screenshot shows "Your Flagship, Global Conference..." in Speaker Summary!
    
    # Let's completely wipe out any summary that is shorter than 100 characters and doesn't contain a period, because a bio should be a paragraph.
    # Actually, that's too destructive. Let's just stick to the targeted regex which catches the things in the screenshot.

    df.to_excel('conference_data.xlsx', index=False)
    print("Done aggressively cleaning dataset!")

if __name__ == "__main__":
    clean_data()
