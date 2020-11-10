import enum
from percentage import Percentage
from pymongo import MongoClient

class BuildType(enum.Enum):
    Gaming = "Gaming"
    Casual = "Casual"
    Rendering = "Rendering"

class GpuBrand(enum.Enum):
    Nvidia = "Nvidia"
    AMD = "AMD"

class CpuBrand(enum.Enum):
    Intel = "Intel"
    AMD = "AMD"

# quick lambda function for getting the percentage of given number as float
percent = lambda x: x/100
# lambda function for getting the full price based on the percentage
full_price = lambda x, y: percent(x)*y

client = MongoClient('mongodb://localhost:27017/')
db = client.PcBuilder
gpus = db.GPU

def build_pc(price, percentages, build_type = BuildType.Gaming.name, gpu_brand = GpuBrand.Nvidia.name, cpu_brand = CpuBrand.Intel.name):
    if percentages == None:
        percentages = get_percentages(build_type)
        if percentages == None: return

    # price that will spent on psu and case (currently not supported, it's basically blank for now)
    leftover_price = price - full_price(percentages.psu_and_case, price)
    
    leftover_price, ssd = pick_ssd(full_price(percentages.ssd, price), leftover_price)
    leftover_price, hdd = pick_hdd(full_price(percentages.hdd, price), leftover_price)

    if leftover_price > price - full_price(percentages.psu_and_case + percentages.ssd + percentages.hdd, price):
        percentages.cpu += percentages.cpu*10/100

    leftover_price, cpu = pick_cpu(full_price(percentages.cpu, price), build_type, cpu_brand, leftover_price)
    leftover_price, motherboard = pick_motherboard(full_price(percentages.motherboard, price), cpu["Socket"], cpu["Chipset"], leftover_price)
    leftover_price, ram = pick_ram(full_price(percentages.ram, price), leftover_price)
    leftover_price, gpu = pick_gpu(leftover_price, build_type, gpu_brand, leftover_price)

    print(leftover_price)
    print(cpu)
    print(motherboard)
    print(ram)
    print(gpu)
    print(ssd)
    print(hdd)

def pick_cpu(spendable_price, build_type, cpu_brand, price):
    benchmark = get_benchmark_text(build_type)
    cpu = db.CPU.find({"Price":{"$lt": spendable_price}, "Brand": cpu_brand}).sort(benchmark, -1)[0]
    return price - cpu["Price"], cpu

def pick_ssd(spendable_price, price):
    ssd = db.SSD.find({"Price": {"$lt": spendable_price}}).sort("Benchmark", -1)[0]
    return price - ssd["Price"], ssd

def pick_motherboard(spendable_price, socket, chipset, price):
    motherboard = db.MOTHERBOARD.find({"Price":{"$lt": spendable_price}, "Socket": socket.replace(" ", ""), "Chipset": chipset.split(",")[0]})[0]
    return price - motherboard["Price"], motherboard

def pick_ram(spendable_price, price):
    ram = db.RAM.find({"Price":{"$lt": spendable_price}})[0]
    return price - ram["Price"], ram

def pick_gpu(spendable_price, build_type, gpu_brand, price):
    benchmark = get_benchmark_text(build_type)
    gpu = db.GPU.find({"Price":{"$lt": spendable_price}, "Brand": gpu_brand,}).sort(benchmark, -1)[0]
    return price - gpu["Price"], gpu

def pick_hdd(spendable_price, price):
    hdd = db.HDD.find({"Price": {"$lt": spendable_price}})[0]
    return price - hdd["Price"], hdd    

# default percentage: gpu = 28%, cpu = 22%, ram = 10%, motherboard = 15%, ssd = 10%, hdd = 5%, psu_and_case = 10%
def get_percentages(build_type):
    switcher = { 
        BuildType.Gaming.name: Percentage(), # default
        BuildType.Casual.name: Percentage(25, 25), # gpu = 25%, cpu = 25%, others stays the same
        BuildType.Rendering.name: Percentage(25, 25), # gpu = 25%, cpu = 25%, others stays the same
    } 

    return switcher.get(build_type, None)

def get_benchmark_text(build_type):
    switcher = { 
        BuildType.Gaming.name: "Gameplay Benchmark", # default
        BuildType.Casual.name: "Desktop Benchmark", # gpu = 25%, cpu = 25%, others stays the same
        BuildType.Rendering.name: "Worksation Benchmark", # gpu = 25%, cpu = 25%, others stays the same
    } 

    return switcher.get(build_type, None)

build_pc(1000, None)
