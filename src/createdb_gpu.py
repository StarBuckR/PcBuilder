import os
import csv
import pandas as pd
from pymongo import MongoClient
import json

nvidia_keywords = ["RTX", "Quadro", "Titan", "GTX"]
nvidia_forbidden_keywords = ["Mobile"]
amd_keywords = ["RX", "Vega", "Radeon", "R9"]
gpus = []

if not os.path.exists('./csv/GPU.csv'):
    import download_file as df
    df.download("GPU")

with open('./csv/GPU.csv', newline='') as f:
    reader = csv.DictReader(f)
    gpu_csv_file = list(reader)

with open('./json/GPU.json') as f:
  json_file = json.load(f)

def dict_search():
    watt = 350
    last_rank = 1
    for row in gpu_csv_file:
        if int(row["Rank"]) > 126:
            break

        if int(row["Rank"]) > last_rank:
            watt = watt - 2
            last_rank = int(row["Rank"])

        row["Watt"] = watt

        if any(x in row["Model"] for x in nvidia_keywords) and \
        not any(y in row["Model"] for y in nvidia_forbidden_keywords):
            digit = [int(s) for s in row["Model"].split() if s.isdigit()]
            if (digit != [] and digit[0] < 1000):
                del row
                continue
            else:
                row["Brand"] = "Nvidia"
        if any(x in row["Model"] for x in amd_keywords):
            digit = [int(s) for s in row["Model"].split() if s.isdigit()]
            if (digit != [] and digit[0] < 500 and digit[0] > 64):
                del row
                continue
            else:
                row["Brand"] = "AMD"

        if row["Brand"] != "Nvidia" and row["Brand"] != "AMD":
            del row
            continue
        
        gpus.append(row)

dict_search()

client = MongoClient('mongodb://localhost:27017/')
db = client['PcBuilder']

for gpu in gpus:
    if gpu["URL"] in json_file and json_file[gpu["URL"]]["Price"]:
        post = {"Brand": gpu["Brand"],
                "Model": gpu["Model"],
                "URL": gpu["URL"],
                "Rank": gpu["Rank"],
                "Watt": gpu["Watt"],
                "Gameplay Benchmark": json_file[gpu["URL"]]["Gameplay Benchmark"],
                "Desktop Benchmark": json_file[gpu["URL"]]["Desktop Benchmark"],
                "Workstation Benchmark": json_file[gpu["URL"]]["Workstation Benchmark"],
                "Price": json_file[gpu["URL"]]["Price"]
                }
        
        posts = db.GPU
        post_id = posts.insert_one(post).inserted_id
