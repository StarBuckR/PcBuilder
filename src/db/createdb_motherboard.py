import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json
from pymongo import MongoClient

if not os.path.exists('./driver/geckodriver.exe'):
    import download_file as df
    df.download_gecko_driver()

browser = webdriver.Firefox(executable_path="./driver/geckodriver.exe")

with open("./json/motherboard.json") as f:
    json_file = json.load(f)

motherboards = [] 

for x in range(1, 7):
    URL = "https://pcpartpicker.com/products/motherboard/#page="+str(x)
    browser.get(URL)
    html = browser.page_source
    time.sleep(2)
    for x in range(0,100):
        row = dict()
        price = browser.find_elements_by_class_name('td__price')
        prc = price[x].get_attribute("innerText")
        prc = prc.split("Add")[0]
        prc = prc.split("$")[-1]

        if prc == "":
            continue
        row["Price"] = int(float(prc))

        name = browser.find_elements_by_class_name('td__nameWrapper')
        name = name[x].text
        name = name.split("(")[0]
        name = name.replace("\n", "")
        row["Name"] = name

        socket = browser.find_elements_by_class_name('td__spec--1')
        sck = socket[x].get_attribute("innerText")
        sck = sck.split("Socket / CPU")[-1]
        sck = sck.replace("\n", "")
        row["Socket"] = sck

        ATX = browser.find_elements_by_class_name('td__spec--2')
        atx = ATX[x].get_attribute("innerText")
        atx = atx.replace("\n", "")
        row["Atx"] = atx

        maxram = browser.find_elements_by_class_name('td__spec--3')
        ram = maxram[x].get_attribute("innerText")
        ram = ram.split("Memory Max")[-1]
        ram = ram.split("GB")[0]
        row["Ram"] = int(ram)

        memoryslot = browser.find_elements_by_class_name('td__spec--4')
        mem = memoryslot[x].get_attribute("innerText")
        mem = mem.split("Memory Slots")[-1]
        row["Memory"] = int(mem)
        
        link = browser.find_elements_by_css_selector("a[href*='/product/']")
        mboardurl = link[x].get_attribute("href")
        row["URL"] = str(mboardurl)

        motherboards.append(row)

       #Code for mhz parsing. But website will stop it for bot reasons after 45.parsing.
       #browser2=webdriver.Chrome()
       # URL = mboardurl
       # browser2.get(URL)
       # html = browser2.page_source
       # time.sleep(1)
       # ddr4list = browser2.find_elements_by_class_name("group--spec")[8]
       # ddr4 = ddr4list.get_attribute("innerText")
       # mhz = ddr4.split("DDR4-")[-1] #ddr3-2 de eklenmeli
       # mhz = mhz.split("\n")[0]

browser.quit()

client = MongoClient('mongodb://localhost:27017/')
db = client.PcBuilder
try:
    a = 1
    for motherboard in motherboards:
        if motherboard["Name"] in json_file:
            informations = {
                    "Brand": motherboard["Name"],
                    "Socket": motherboard["Socket"],
                    "Memory Max": int(motherboard["Ram"]),
                    "Memory Slots": int(motherboard["Memory"]),
                    "Price": int(motherboard["Price"]),
                    "URL": motherboard["URL"],
                    "MHZ": int(json_file[motherboard["Name"]]["MHZ"]),
                    "Chipset": json_file[motherboard["Name"]]["Chipset"],
                    "Rank": a,
                    "Atx" : motherboard["Atx"]
                }
            a += 1
            posts = db.MOTHERBOARD
            post_id = posts.insert_one(informations).inserted_id
            
except(KeyError):
    print(KeyError)
