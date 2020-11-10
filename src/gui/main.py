import json
import os, sys

if not os.path.exists('./config.json'):
    print("h")
    data = { "Initialized": False }
    with open("./config.json", "w") as f:
        json.dump(data, f, indent=4)

with open("./config.json", "r") as file:
    data = json.load(file)

    if data["Initialized"] != True:
        import os, sys
        sys.path.insert(1, os.getcwd() +'/src/db/')
        import createdb_cpu, createdb_gpu, createdb_hdd, createdb_motherboard, createdb_ram, createdb_ssd

    data["Initialized"] = True
    with open("config.json", "w") as outfile:
        json.dump(data, outfile)

print("Test")
