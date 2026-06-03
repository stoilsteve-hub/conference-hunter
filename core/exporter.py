import pandas as pd
import os

class Exporter:
    def __init__(self, output_file="conference_data.xlsx"):
        self.output_file = output_file
        # These are the columns requested
        self.columns = [
            "Conference ID", "Conference Name", "Topic", "Dates", "Location",
            "Speaker First Name", "Speaker Full Name", "Speaker Job Title",
            "Speaker Company", "Presentation Title", "Speaker Summary", "Speaker Profile",
            "Speaker Image URL"
        ]

    def _standardize_date(self, d):
        import re
        if not isinstance(d, str) or d.strip() == "": return "TBD"
        d = d.split('|')[0].strip()
        d = d.replace("Returning ", "").replace("Ran ", "").strip()
        
        year_match = re.search(r'\b(202[0-9])\b', d)
        year = year_match.group(1) if year_match else "TBD"
        
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        month = ""
        for m in months:
            if m.lower() in d.lower():
                month = m
                break
                
        day_match = re.search(r'\b([0-9]{1,2}(?:-[0-9]{1,2})?)\b', d)
        day = day_match.group(1) if day_match and day_match.group(1) != year and len(day_match.group(1)) <= 5 else ""
        
        if month and day and year != "TBD":
            return f"{month} {day}, {year}"
        elif month and year != "TBD":
            return f"{month} {year}"
        elif year != "TBD":
            return year
        else:
            return "TBD"

    def _standardize_location(self, loc):
        if not isinstance(loc, str) or loc.strip() == "": return "TBD"
        if "|" in loc:
            loc = loc.split("|")[1].strip()
        loc = loc.strip()
        
        if "Boston" in loc: return "Boston, MA"
        if "San Diego" in loc: return "San Diego, CA"
        if "San Francisco" in loc: return "San Francisco, CA"
        if "London" in loc: return "London, UK"
        if "Arlington" in loc: return "Arlington, VA"
        if "Raleigh" in loc: return "Raleigh, NC"
        if "Berlin" in loc: return "Berlin, Germany"
        if "Washington" in loc: return "Washington, DC"
        if "Seoul" in loc: return "Seoul, South Korea"
        if "Nashville" in loc: return "Nashville, TN"
        return loc

    def save_data(self, new_data_list):
        if not new_data_list:
            return 0
            
        new_df = pd.DataFrame(new_data_list, columns=self.columns)
        
        # check if file exists, if not create new dataframe
        if os.path.exists(self.output_file):
            df = pd.read_excel(self.output_file)
            before_len = len(df)
            combined = pd.concat([df, new_df], ignore_index=True)
            # Drop duplicates keeping the first occurrence (which would be the existing one if it exists)
            # or keep the last to overwrite with fresh data. Let's keep last to update with new rich data
            combined.drop_duplicates(subset=['Speaker Full Name', 'Conference Name'], keep='last', inplace=True)
            after_len = len(combined)
            new_added = after_len - before_len
            df = combined
        else:
            df = new_df
            new_added = len(df)
            
        # Standardize Dates and Locations
        for i, row in df.iterrows():
            raw_date = str(row['Dates']) if pd.notnull(row['Dates']) else ""
            raw_loc = str(row['Location']) if pd.notnull(row['Location']) else "TBD"
            
            if "|" in raw_date and (raw_loc == "TBD" or raw_loc == ""):
                raw_loc = raw_date.split("|")[1].strip()
                
            df.at[i, 'Dates'] = self._standardize_date(raw_date)
            df.at[i, 'Location'] = self._standardize_location(raw_loc)
        
        df.to_excel(self.output_file, index=False)
        print(f"Data saved to {self.output_file}! {new_added} NEW speakers added.")
        return new_added
