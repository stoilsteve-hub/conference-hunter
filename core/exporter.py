import pandas as pd
import os

class Exporter:
    def __init__(self, output_file="conference_data.xlsx"):
        self.output_file = output_file
        # These are the columns requested
        self.columns = [
            "Conference ID", "Conference Name", "Topic", "Dates", "Location",
            "Speaker First Name", "Speaker Full Name", "Speaker Job Title",
            "Speaker Company", "Speaker Summary", "Speaker Profile",
            "Speaker Email", "Speaker Image URL", "Speaker LinkedIn"
        ]

    def save_data(self, new_data_list):
        # check if file exists, if not create new dataframe
        if os.path.exists(self.output_file):
            df = pd.read_excel(self.output_file)
            new_df = pd.DataFrame(new_data_list, columns=self.columns)
            df = pd.concat([df, new_df], ignore_index=True)
        else:
            df = pd.DataFrame(new_data_list, columns=self.columns)
        
        df.to_excel(self.output_file, index=False)
        print(f"Data saved to {self.output_file}! yey")
