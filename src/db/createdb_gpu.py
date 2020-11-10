import os
import csv
from pymongo import MongoClient
import json
from selenium import webdriver
from currency_converter import CurrencyConverter

# because of a buggy importing error, i had to import files like this
import sys
sys.path.insert(1, os.getcwd() +'/src/helpers/')
import get_price

nvidia_keywords = ["RTX", "Quadro", "Titan", "GTX"]
nvidia_forbidden_keywords = ["Mobile"]
amd_keywords = ["RX", "Vega", "Radeon", "R9"]
gpus = []

if not os.path.exists('./csv/GPU.csv'):
    import download_file as df
    df.download_csv("GPU")

with open('./csv/GPU.csv', newline='') as f:
    reader = csv.DictReader(f)
    gpu_csv_file = list(reader)

if not os.path.exists('./driver/geckodriver.exe'):
    import download_file as df
    df.download_gecko_driver()

with open('./json/GPU.json') as f:
    json_file = json.load(f)

def dict_search():
    driver = webdriver.Firefox(executable_path="./driver/geckodriver.exe")
    c = CurrencyConverter()
    price_url_base = "https://pricespy.co.uk/search?search="
    for row in gpu_csv_file:
        if int(row["Rank"]) > 126:
            break

        # this code block is filtering models by given keywords and forbidden keywords.
        if any(x in row["Model"] for x in nvidia_keywords) and \
                not any(y in row["Model"] for y in nvidia_forbidden_keywords):
            # number is if model contains any number, eg. 1080 Ti, it gets that number and checks if its outdated model number
            number = [int(s) for s in row["Model"].split() if s.isnumeric()]
            if (number != [] and number[0] < 1000):
                del row
                continue
            else:
                row["Brand"] = "Nvidia"
        # this code block is filtering models by given keywords.
        if any(x in row["Model"] for x in amd_keywords):
            # number is if model contains any number, eg. 1080 Ti, it gets that number and checks if its outdated model number
            number = [int(s) for s in row["Model"].split() if s.isnumeric()]
            if (number != [] and number[0] < 500 and number[0] > 64):
                del row
                continue
            else:
                row["Brand"] = "AMD"
        # if brand is not "Nvidia" nor "AMD", then delete that row and continue
        if row["Brand"] != "Nvidia" and row["Brand"] != "AMD":
            del row
            continue

        full_url = price_url_base + row["Model"]
        full_url = full_url.replace(" ", "%20")
        # get models price from another script
        price = get_price.get_price(driver, c, full_url)

        if price:
            row["Price"] = price
            gpus.append(row)
    driver.quit()
    
dict_search()

# open mongo client and insert data one by one
client = MongoClient('mongodb://localhost:27017/')
db = client['PcBuilder']

for gpu in gpus:
    # price > 100 dollars because it can be mistaken single fan price or 
    # that sort of stuff for real gpu. and their price is definitely lower
    # than 100 dollars
    if gpu["URL"] in json_file and gpu["Price"] and gpu["Price"] > 100:
        post = {
                "Brand": gpu["Brand"],
                "Model": gpu["Model"],
                "URL": gpu["URL"],
                "Rank": int(gpu["Rank"]),
                "Gameplay Benchmark": json_file[gpu["URL"]]["Gameplay Benchmark"],
                "Desktop Benchmark": json_file[gpu["URL"]]["Desktop Benchmark"],
                "Workstation Benchmark": json_file[gpu["URL"]]["Workstation Benchmark"],
                "Price": gpu["Price"]
            }

        posts = db.GPU
        post_id = posts.insert_one(post).inserted_id
