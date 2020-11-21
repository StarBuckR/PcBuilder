import enum
from percentage import Percentage
from pymongo import MongoClient

# Enum that contains Build Types such as Gaming, Casual(Desktop) and Rendering(Workstation)
class BuildType(enum.Enum):
    Gaming = "Gaming"
    Casual = "Casual"
    Rendering = "Rendering"

# Enum that contains Gpu Brands
class GpuBrand(enum.Enum):
    Nvidia = ["Nvidia"]
    AMD = ["AMD"]
    Both = ["Nvidia", "AMD"]

# Enum that contains Cpu Brands
class CpuBrand(enum.Enum):
    Intel = ["Intel"]
    AMD = ["AMD"]
    Both = ["Intel", "AMD"]

# Enum that contains Storage Types such as Only HDD, Only SSD and Both
class StorageType(enum.Enum):
    OnlyHDD = "OnlyHDD"
    OnlySSD = "OnlySSD"
    Both = "Both"

# quick lambda function for getting the percentage of given number as float
percent = lambda x: x/100
# lambda function for getting the full price based on the percentage
full_price = lambda x, y: percent(x)*y

client = MongoClient('mongodb://localhost:27017/')
db = client.PcBuilder

def build_pc(price, percentages, title, build_type = BuildType.Gaming.value, gpu_brand = GpuBrand.Both.value, cpu_brand = CpuBrand.Both.value, storage_type = StorageType.Both.value):
    # if percentage is not spesifically given, create percentages according to build type
    if percentages == None:
        percentages = get_percentages(build_type)
        if percentages == None: return

    if price < 550:
        print("Price can not be lower than 550 dollars")
        import sys
        sys.exit()

    # price that will spent on psu and case (currently not supported, it's basically blank for now but price is calculated)
    leftover_price = price - full_price(percentages.psu_and_case, price)

    ssd = None
    hdd = None
    if storage_type == StorageType.Both.value:
        leftover_price, ssd = pick_ssd(full_price(percentages.ssd, price), leftover_price)
        leftover_price, hdd = pick_hdd(full_price(percentages.hdd, price), leftover_price)
    elif storage_type == StorageType.OnlySSD.value:
        leftover_price, ssd = pick_ssd(full_price(percentages.ssd, price), leftover_price)
    elif storage_type == StorageType.OnlyHDD.value:
        leftover_price, hdd = pick_hdd(full_price(percentages.hdd, price), leftover_price)

    leftover_price, cpu = pick_cpu(full_price(percentages.cpu, price), build_type, cpu_brand, leftover_price)
    leftover_price, motherboard = pick_motherboard(full_price(percentages.motherboard, price), cpu["Socket"], cpu["Chipset OC"], cpu["Chipset"], leftover_price)
    leftover_price, ram = pick_ram(full_price(percentages.ram, price), motherboard["Memory Max"], motherboard["Memory Slots"], motherboard["MHZ"], leftover_price)
    leftover_price, gpu = pick_gpu(leftover_price, build_type, gpu_brand, leftover_price)

    pc = {}
    pc["Total Price"] = price
    pc["Title"] = title
    pc["CPU"] = cpu
    pc["Motherboard"] = motherboard
    pc["RAM"] = ram
    pc["GPU"] = gpu
    pc["SSD"] = ssd
    pc["HDD"] = hdd
    pc["Leftover Price"] = leftover_price

    return pc

def pick_ssd(spendable_price, price):
    m2 = False
    # if price is more than 70 dollars, it should pick an m2 ssd
    if spendable_price >= 70:
        m2 = True

    if spendable_price > 250:
        ssd = db.SSD.find_one({"Price": {"$lte": spendable_price}, "M2": m2, "Storage": {"$lt": spendable_price * 20, "$gt": 1000}}, sort=[("Price-Performance", -1)])
    else:
        ssd = db.SSD.find_one({"Price": {"$lte": spendable_price}, "M2": m2, "Storage": {"$lt": spendable_price * 20, "$gt": spendable_price * 4}}, sort=[("Price-Performance", -1)])
    if ssd:
        return price - ssd["Price"], ssd
    else:
        return price, None

def pick_hdd(spendable_price, price):
    hdd = db.HDD.find_one({"Price": {"$lte": spendable_price}}, sort=[("Storage", -1)])
    if hdd:
        return price - hdd["Price"], hdd
    else:
        return price, None

def pick_cpu(spendable_price, build_type, cpu_brand, price):
    benchmark = get_benchmark_text(build_type)
    cpu = db.CPU.find_one({"Price":{"$lte": spendable_price}, "Brand": {"$in": cpu_brand}}, sort=[(benchmark, -1)])

    if cpu:
        return price - cpu["Price"], cpu
    else:
        return price, None

def pick_motherboard(spendable_price, socket, chipset_oc, chipset, price):
    atx = ["ATX", "EATX"] if spendable_price > 100 else ["Micro ATX", "Mini ITX", "ATX", "EATX"]
    
    # hacky fix for a little bug that caused by scraped websites socket naming convention
    if socket in ["TRX4", "TR4"]:
        socket = "s" + socket

    motherboard = db.MOTHERBOARD.find_one({"Price":{"$lte": spendable_price*1.1}, "Atx": {"$in": atx}, "Socket": socket.replace(" ", ""), "Chipset": {"$in": chipset_oc.split(",")}}, sort=[("MHZ", -1)])
    if not motherboard:
        motherboard = db.MOTHERBOARD.find_one({"Price":{"$lte": spendable_price*1.1}, "Atx": {"$in": atx}, "Socket": socket.replace(" ", ""), "Chipset": {"$in": chipset.split(",")}}, sort=[("MHZ", -1)])
    
    if motherboard:
        return price - motherboard["Price"], motherboard
    else:
        return price, None

def pick_ram(spendable_price, total_memory, memory_slots, mhz, price):
    rams = db.RAM.find({"Price":{"$lte": spendable_price}, "Total Memory": {"$lte": total_memory}, "RAM Count" : {"$lte": memory_slots}, "MHZ": {"$lte": mhz}})

    ram = rams[0]
    for r in rams:
        if (r["Latency"] < ram["Latency"] and r["Total Memory"] >= ram["Total Memory"]) or r["Total Memory"] > ram["Total Memory"]:
            ram = r

    if ram:
        return price - ram["Price"], ram
    else:
        return price, None

def pick_gpu(spendable_price, build_type, gpu_brand, price):
    benchmark = get_benchmark_text(build_type)
    gpu = db.GPU.find({"Price":{"$lte": spendable_price}, "Brand": {"$in": gpu_brand}}).sort(benchmark, -1)[0]

    if gpu:
        return price - gpu["Price"], gpu
    else:
        return price, None

# default percentages are: gpu = 33%, cpu = 22%, ram = 10%, motherboard = 12%, ssd = 10%, hdd = 5%, psu_and_case = 8%
def get_percentages(build_type):
    switcher = { 
        BuildType.Gaming.value: Percentage(), # default
        BuildType.Casual.value: Percentage(28, 27), # gpu = 28%, cpu = 27%, others stays the same
        BuildType.Rendering.value: Percentage(28, 27), # gpu = 28%, cpu = 27%, others stays the same
    } 

    return switcher.get(build_type, None)

def get_benchmark_text(build_type):
    switcher = { 
        BuildType.Gaming.value: "Gameplay Benchmark",
        BuildType.Casual.value: "Desktop Benchmark",
        BuildType.Rendering.value: "Workstation Benchmark",
    } 

    return switcher.get(build_type, None)
