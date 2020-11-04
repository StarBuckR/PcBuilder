from pymongo import MongoClient
import json

mongo_client = MongoClient('localhost', 27017)
db = mongo_client.PcBuilder
col = db.motherboard


# Writing to sample.json 
with open("./json/motherboardmhzz.json", "w") as outfile:
    for x in col.find({},{'_id':0,'MHZ': 1,'Name': 1}):
        data = {
        x["Name"].replace("\n", ""): {
        'MHZ': x["MHZ"].replace("\n", "")} 
    }
        json.dump(data, outfile, indent=4, separators=(", ", ": "), sort_keys=True)

