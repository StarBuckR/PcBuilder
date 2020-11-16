import requests
import zipfile
import os
import sys

base_url = "https://www.userbenchmark.com/resources/download/csv/"
def download_csv(type):
    try:
        full_url = base_url + type + "_UserBenchmarks.csv"
        file_path = "./csv/" + type + ".csv"
        print(file_path)
        file = requests.get(full_url, allow_redirects=True)

        os.makedirs("./csv/", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(file.content)
    except(RuntimeError):
        print(RuntimeError)

def download_gecko_driver():
    url = "https://github.com/mozilla/geckodriver/releases/download/v0.27.0/geckodriver-v0.27.0-win64.zip"
    try:
        file = requests.get(url, allow_redirects=True, stream=True)
        
        with open("./gecko.zip", "wb") as f:
            for chunk in file.iter_content(chunk_size=128):
                f.write(chunk)
        
        #os.makedirs("./driver/")
        with zipfile.ZipFile("./gecko.zip", 'r') as zip_ref:
            zip_ref.extractall("./driver/")
        os.remove("./gecko.zip")
    except(RuntimeError):
        print(RuntimeError)
def download_fonts():
    url = "https://fonts.google.com/download?family=Quantico"
    try:
        file = requests.get(url, allow_redirects=True, stream=True)
        
        with open("./Quantico.zip", "wb") as f:
            for chunk in file.iter_content(chunk_size=128):
                f.write(chunk)
        
        #os.makedirs("./driver/")
        with zipfile.ZipFile("./Quantico.zip", 'r') as zip_ref:
            zip_ref.extractall("./fonts")
        os.remove("./Quantico.zip")
    except(RuntimeError):
        print(RuntimeError)