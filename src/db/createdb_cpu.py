
import os
import csv
import requests
from pymongo import MongoClient
import json
import re
from selenium import webdriver
from currency_converter import CurrencyConverter

import sys
sys.path.insert(1, os.getcwd() + '/src/helpers/')
import get_price

cpu_link = []
intel_data = []
amd_data = []
cpus = []
temp_list = []

if not os.path.exists('./csv/CPU.csv'):
    import download_file as df
    df.download_csv("CPU")

if not os.path.exists('./driver/geckodriver.exe'):
    import download_file as df
    df.download_gecko_driver()

with open('./json/CPU.json') as f:
    json_file = json.load(f)

def intel_chipset(model):
    if model == "Model":
        pass
    else:
        series = re.findall("[0-9]", model, 1)
        series = series[0]
        code = model[len(model)-2:len(model)]

        if re.search("[-][8-9]", model) and (re.search("0K", code) or re.search("0F", code) or re.search("KS", code) or re.search("KF", code) or re.search("6K", code) or re.search("[0-9][0-9]", code)):
            oc = "Z370,Z390"
            no_oc = "H310,B365,B360,H370,Q370"
            pin = "LGA 1151"
            return oc, no_oc, pin
        elif re.search("[-][7-9]", model) and (re.search("X", code) or re.search("XE", code)):
            oc = "X299"
            no_oc = "X299"
            pin = "LGA 2066"
            return oc, no_oc, pin
        elif re.search("[-][7]", model) and (re.search("0K", code) or re.search("0F", code) or re.search("KF", code) or re.search("[0-9][0-9]", code)):
            oc = "Z270"
            no_oc = "B250,Q250,H270,Q270"
            pin = "LGA 1151"
            return oc, no_oc, pin
        elif re.search("-10", model, 1) and (re.search("0K", code) or re.search("0F", code) or re.search("KF", code) or re.search("[0-9][0-9]", code), re.search("0X", code)):
            oc = "Z490"
            no_oc = "H410,B460,H470,Q470,W480"
            pin = "LGA 1200"
            return oc, no_oc, pin
        else:
            oc = "Unknown"
            no_oc = "Unkown"
            pin = "Unkown"
            return oc, no_oc, pin

def amd_chipset(model):
    if model == "Model":
        pass
    else:
        if re.search("TR", model, 1):
            if(re.search("3", model)):
                pin = "TRX4"
            else:
                pin = "TR4"
            temp_gen = re.split("TR", model, 1)
        elif re.search("[0-9]", model, 1):
            pin = "AM4"
            series = re.findall("[0-9]", model, 1)
            series = series[0]
            temp_gen = re.split("[0-9]", model, 1)
        else:
            temp_gen = model

        gen = str(temp_gen[len(temp_gen) - 1]).strip()
        
        if gen[len(gen) - 1] != "U" or "H" or "M":
            if gen[0] == "1" or (gen[0] == "2" and gen[len(gen) - 1] == "G"):
                oc = "X370,B350,X470,B450"
                no_oc = "A320"
                if(pin == "TR4"):
                    oc = "X399"
                    no_oc = "X399"
                return oc, no_oc, pin
            elif gen[0] == "2" or (gen[0] == "3" and gen[len(gen) - 1] == "G"):
                oc = "X370,B350,X470,B450,X570"
                no_oc = "A320"
                if(pin == "TR4"):
                    oc = "X399"
                    no_oc = "X399"
                return oc, no_oc, pin
            elif gen[0] == "3":
                oc = "X470,B450,X570,B550"
                no_oc = "A520"
                if(pin == "TRX4"):
                    oc = "TRX40"
                    no_oc = "TRX40"
                return oc, no_oc, pin
            else:
                oc = "Unknown"
                no_oc = "Unkown"
                pin = "Unkown"
                return oc, no_oc, pin
        else:
            oc = "Unknown"
            no_oc = "Unkown"
            pin = "Unkown"
            return oc, no_oc, pin

with open('./csv/CPU.csv', newline='') as cpu_first_data:
    reader = csv.DictReader(cpu_first_data)
    cpu_csv_file = list(reader)

    for i, cpu in enumerate(cpu_csv_file, start=1):
        if i <= 300:
            if (re.search("Ryzen", cpu["Model"])):
                check = amd_chipset(cpu["Model"])
                if check:
                    oc, no_oc, pin = amd_chipset(cpu["Model"])
                    cpu["Chipset OC"] = oc
                    cpu["Chipset"] = no_oc
                    cpu["Socket"] = pin
                else:
                    pass
            elif re.search("Core", cpu["Model"]):
                check = intel_chipset(cpu["Model"])
                if check:
                    oc, no_oc, pin = intel_chipset(cpu["Model"])
                    cpu["Chipset OC"] = oc
                    cpu["Chipset"] = no_oc
                    cpu["Socket"] = pin
                else:
                    pass
            else:
                pass
        else:
            break

def cpu_price():
    driver = webdriver.Firefox(executable_path="./driver/geckodriver.exe")
    c = CurrencyConverter()
    for row in cpu_csv_file:
        if row["URL"] in json_file:
            if row["Brand"] == "AMD":
                product = row["Brand"]+row["Model"]
            elif row['Brand'] == "Intel":
                product = row["Brand"]+" "+row["Model"]
            product = re.sub("\s", "%20", product)
            base_url = "https://pricespy.co.uk/search?search="
            last_url = base_url + product
            price = get_price.get_price(driver, c, last_url)
            row["Price"] = price
        else:
            continue
    driver.quit()

cpu_price()
client = MongoClient('mongodb://localhost:27017/')
db = client['PcBuilder']

for i, cpu in enumerate(cpu_csv_file, start=1):
    if cpu["URL"] in json_file and cpu["Price"] and i <= 300 and cpu['Socket'] != "Unkown":
        post = {
            "Brand": cpu["Brand"],
            "Model": cpu["Model"],
            "URL": cpu["URL"],
            "Rank": int(cpu["Rank"]),
            "Chipset OC": cpu["Chipset OC"],
            "Chipset": cpu["Chipset"],
            "Socket": cpu["Socket"],
            "Gameplay Benchmark": json_file[cpu["URL"]]["Gameplay Benchmark"],
            "Desktop Benchmark": json_file[cpu["URL"]]["Desktop Benchmark"],
            "Workstation Benchmark": json_file[cpu["URL"]]["Workstation Benchmark"],
            "Price": cpu["Price"]
        }
        posts = db.CPU
        post_id = posts.insert_one(post).inserted_id
