from pymongo import MongoClient
import math

client = MongoClient('mongodb://localhost:27017/')
db = client.PcBuilder

def update_database(value, database, given_id, key):
    database.find_one_and_update(
         {"_id" : given_id},
            {"$set":
                {key: value}
            },upsert=True
    )

def ssd():
    for document in db.SSD.find():
        # our own algorithm for finding price-performance ratio
        m2 = 1 if document['M2'] == True else 0
        price_performance_value = float((document['Benchmark']/document['Price']) + math.sqrt(document['Storage']/5000) + m2)

        update_database(price_performance_value, db.SSD, document["_id"], "Price-Performance")

def ram():
    for document in db.RAM.find():
        # our own algorithm for finding price-performance ratio
        price_performance_value = float((document['CL']/document['MHZ']*100000)/(document["Price"]/4) + document['Total Memory']/8)
        latency_value = float(document['CL']/document['MHZ']*1000)

        update_database(price_performance_value, db.RAM, document["_id"], "Price-Performance")
        update_database(latency_value, db.RAM, document["_id"], "Latency")

def gpu():
    for document in db.GPU.find():
        # our own algorithm for finding price-performance ratio
        price_performance_value = float((document['Gameplay Benchmark'] + document['Desktop Benchmark'] + document['Workstation Benchmark'])*10/(document["Price"]))
        
        update_database(price_performance_value, db.GPU, document["_id"], "Price-Performance")

def cpu():
     for document in db.CPU.find():
        # our own algorithm for finding price-performance ratio
        price_performance_value = float((document['Gameplay Benchmark'] + document['Desktop Benchmark'] + document['Workstation Benchmark'])*10/(document["Price"]))
        
        update_database(price_performance_value, db.CPU, document["_id"], "Price-Performance")
