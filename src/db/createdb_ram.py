import csv
import os
from pymongo import MongoClient
import requests
from currency_converter import CurrencyConverter
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

import sys
sys.path.insert(1, os.getcwd() +'./src/helpers/')
import get_price

if not os.path.exists('./csv/RAM.csv'):
    import download_file as df
    df.download_csv("RAM")

if not os.path.exists('./driver/geckodriver.exe'):
    import download_file as df
    df.download_gecko_driver()

with open('./csv/RAM.csv', newline='') as f:
    reader = csv.DictReader(f)
    data = list(reader)

lists = []

for row in data:
    if "DDR3" in row["Model"]:
        continue

    is_exist = False
    for e in lists:
        if row["URL"] == e["URL"]:
            is_exist = True
    if is_exist:
        continue

    gb = row["Model"].split(" ")[-1]
    gb = gb.split("GB")[0]
    a = gb.split("x")[0]
    b = gb.split("x")[-1]
    GB = int(a)*int(b)

    cl = row["Model"].split(" ")[-2]
    cl = cl.split("C")[-1]
    mhz = row["Model"].split(" ")[-3]
    row["Model"] = " ".join(row["Model"].split(" ")[:-3])

    row["RAM Count"] = a
    row["GB"] = gb
    row["TOTALMEMORY"] = GB
    row["CL"] = cl
    row["MHZ"] = str(mhz)
    lists.append(row)

driver = webdriver.Firefox(executable_path="./driver/geckodriver.exe")
c = CurrencyConverter()
def dict_search():
    price_url_base = "https://pricespy.co.uk/search?search="
    
    for row in lists:
        full_url = price_url_base + row["Model"] + " " + row["MHZ"] + " " + row["GB"]
        full_url = full_url.replace(" ", "%20")
        # get models price from another script
        price = get_price.get_price(driver, c, full_url)

        if price:
            row["Price"] = price
 
dict_search()

driver.quit()

client = MongoClient('mongodb://localhost:27017/')
db = client.PcBuilder

for row in lists:
    try:
        informations = {
            "Brand": row["Brand"],   
            "Model": row["Model"],
            "Rank": int(row["Rank"]),
            "Url": row["URL"],
            "Gb": row["GB"],
            "RAM Count": int(row["RAM Count"]),
            "Total Memory" : int(row["TOTALMEMORY"]),
            "CL": int(row["CL"]),
            "MHZ": int(row["MHZ"]),
            "Price": int(row["Price"]),
            }
        posts = db.RAM
        post_id = posts.insert_one(informations).inserted_id
    except(KeyError):
        print("KeyError")
