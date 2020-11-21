import json
import os, sys

sys.path.insert(1, os.getcwd() + '/src/scripts/')
from main_page import create_main_window

if not os.path.exists('./config.json'):
    data = { 
        "Database Initialized": False,
        "Price-Performance Initialized": False 
        }
    with open("./config.json", "w") as f:
        json.dump(data, f, indent=4)

with open("./config.json", "r") as file:
    data = json.load(file)

    if data["Database Initialized"] != True:
        sys.path.insert(1, os.getcwd() +'/src/db/')
        import createdb_cpu, createdb_gpu, createdb_hdd, createdb_motherboard, createdb_ram, createdb_ssd
        
        data["Database Initialized"] = True
        with open("config.json", "w") as outfile:
            json.dump(data, outfile)

    if data["Price-Performance Initialized"] != True:
        import price_performance

        price_performance.ssd()
        price_performance.ram()
        price_performance.gpu()
        price_performance.cpu()

        data["Price-Performance Initialized"] = True
        with open("config.json", "w") as outfile:
            json.dump(data, outfile)

create_main_window()
