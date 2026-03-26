import pandas as pd
import os
from datetime import datetime

CSV_PATH = "data/citizen.csv"

def init_csv():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(CSV_PATH):
        df = pd.DataFrame(columns=[
            "time_collect", "total", "ill", "address", "elderly", 
            "children", "danger_level", "status_before", "time_rescuse"
        ])
        df.to_csv(CSV_PATH, index=False)

def save_citizen_request(data):
    df = pd.DataFrame([data])
    df.to_csv(CSV_PATH, mode='a', header=False, index=False)