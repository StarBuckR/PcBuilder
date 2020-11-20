import os
import csv
import requests
import re
from bs4 import BeautifulSoup
from currency_converter import CurrencyConverter
from selenium import webdriver
from pymongo import MongoClient

import sys
sys.path.insert(1, os.getcwd() + '/src/helpers/')
import get_price

if not os.path.exists('./csv/SSD.csv'):
    import download_file as df
    df.download_csv("SSD")
if not os.path.exists("./driver/geckodriver.exe"):
    import download_file as df
    df.download_gecko_driver()

with open('./csv/SSD.csv', newline='') as ssd_first_data:
    reader = csv.DictReader(ssd_first_data)
    ssd_csv_file = list(reader)


def ssd_price():
    driver = webdriver.Firefox(executable_path="./driver/geckodriver.exe")
    c = CurrencyConverter()

    for row in ssd_csv_file:
        product = row["Brand"]+" "+row["Model"]
        product = re.sub("\s", "%20", product)

        base_url = "https://pricespy.co.uk/search?search="
        last_url = base_url + product

        price = get_price.get_price(driver, c, last_url)
        print(price)
        if price:
            row["Price"] = price
    driver.quit()

ssd_price()

def ssd_model_parser(data_set):
    try:
        if re.search('M.2', data_set):  # Checking for 'M.2'
            m2 = True
        else:
            m2 = False
        storage_size = re.findall('[0-9][0-9][0-9][G][B]', data_set) or re.findall('[0-9][T][B]', data_set) \
            or re.findall('[0-9][0-9][G][B]', data_set)
        storage = storage_size[0]  # to parse storage

        # to parse ssd brand.Nvme always comes after model type.
        if re.search('NVMe', data_set):
            temp = re.split('NVMe', data_set)
        elif re.search('PCIe', data_set):
            temp = re.split('PCIe', data_set)
        elif re.search('SATA', data_set):
            temp = re.split('SATA', data_set)
        elif re.search(storage_size[0], data_set):
            temp = re.split(r"\b" + storage_size[0] + r"\b", data_set)
        else:
            temp = data_set
        model = temp[0]
        return model, storage, m2
    except:
        pass  # if it's empty or it doesn't fit the pattern

for data in ssd_csv_file:
    try:
        check = ssd_model_parser(data["Model"])
        if check:
            model, storage, m2 = ssd_model_parser(data["Model"])
            data["Model"] = model.strip()
            data["Storage"] = storage.strip()
            data["M2"] = m2
    except:
        pass

client = MongoClient('mongodb://localhost:27017/')
db = client.PcBuilder

for ssd in ssd_csv_file:
    try:
        if ssd["Price"]:
            post = {
                "Brand": ssd["Brand"],
                "Model": ssd["Model"],
                "URL": ssd["URL"],
                "Storage": ssd["Storage"],
                "M2": ssd["M2"],
                "Rank": int(ssd["Rank"]),
                "Price": ssd["Price"],
                "Benchmark": float(ssd["Benchmark"])
            }
            posts = db.SSD
            post_id = posts.insert_one(post).inserted_id
    except(KeyError):
        continue

for document in db.SSD.find():
    temp_storage = document['Storage']
    if re.search("GB", temp_storage):
        temp_value = re.split("GB", temp_storage)
        temp = int(temp_value[0])
    elif re.search("TB", temp_storage):
        temp_value = re.split("TB", temp_storage)
        temp = int(temp_value[0])*1000
    new_values = {"$set": {'Storage': temp}}
    to_change = {"Storage": document['Storage']}
    x = db.SSD.update_one(to_change, new_values)
    