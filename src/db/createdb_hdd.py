import os
import csv
from pymongo import MongoClient
import re
from selenium import webdriver
from currency_converter import CurrencyConverter

# because of a buggy importing error, i had to import files like this
import sys
sys.path.insert(1, os.getcwd() +'/src/helpers/')
import get_price

if not os.path.exists('./csv/HDD.csv'):
    import download_file as df
    df.download_csv("HDD")

if not os.path.exists('./driver/geckodriver.exe'):
    import download_file as df
    df.download_gecko_driver()

with open('./csv/HDD.csv', newline='') as f:
    reader = csv.DictReader(f)
    hdd_csv_file = list(reader)

hdds = []
price_url_base = "https://pricespy.co.uk/search?search="

def hdd_model_and_price_parser():
    driver = webdriver.Firefox(executable_path="./driver/geckodriver.exe")
    c = CurrencyConverter()
    for row in hdd_csv_file:
        try:
            model = row["Model"]
            if any(x in model for x in "SSHD") or int(row["Rank"]) > 357:
                continue
            
            # check if model contains XXXGB, XXTB or XTB in its name
            storage_size = re.findall('[0-9][0-9][0-9][G][B]', model) or re.findall('[0-9][0-9][T][B]', model) \
                        or re.findall('[0-9][.][0-9][T][B]', model) or re.findall('[0-9][T][B]', model)
            if storage_size == []:
                continue

            storage = storage_size[0]

            if re.search(storage_size[0], model):
                temp = re.split(r"\b" + storage_size[0] + r"\b", model)
            else:
                temp = model

            final_model = temp[0]

            if re.search("GB",storage):
                temp_value = re.split("GB",storage)
                storage = int(temp_value[0])
            elif re.search("TB",storage):
                temp_value = re.split("TB",storage)
                storage = int(float(temp_value[0])*1000)

            row["Storage"] = storage
            row["Model"] = final_model

            full_url = price_url_base + row["Brand"] + " " + model
            full_url = full_url.replace(" ", "%20")
            # get models price from another script
            price = get_price.get_price(driver, c, full_url)

            if price:
                row["Price"] = price
                hdds.append(row)
        except(RuntimeError):
            print("error:" + model)
    driver.quit()
    
hdd_model_and_price_parser()

# open mongo client and insert data one by one
client = MongoClient('mongodb://localhost:27017/')
db = client['PcBuilder']

i = 1
for hdd in hdds:
    if hdd["Price"]:
        post = {
                "Brand": hdd["Brand"],
                "Model": hdd["Model"],
                "URL": hdd["URL"],
                "Rank": i,
                "Storage": int(hdd["Storage"]),
                "Price": hdd["Price"],
                "Benchmark": float(hdd["Benchmark"])
            }
        i += 1
        
        posts = db.HDD
        post_id = posts.insert_one(post).inserted_id
