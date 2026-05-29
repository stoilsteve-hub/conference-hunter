import pandas as pd
import os
from core.exporter import Exporter

df = pd.read_excel("conference_data.xlsx")
data_list = df.to_dict('records')

os.remove("conference_data.xlsx")
exporter = Exporter("conference_data.xlsx")
exporter.save_data(data_list)
