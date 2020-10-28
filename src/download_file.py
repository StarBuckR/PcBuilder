import requests

base_url = "https://www.userbenchmark.com/resources/download/csv/"
def download(type):
    try:
        full_url = base_url + type + "_UserBenchmarks.csv"
        file_path = "./csv/" + type + ".csv"
        print(file_path)
        file = requests.get(full_url, allow_redirects=True)
        
        with open(file_path, "wb") as f:
            f.write(file.content)
    except(RuntimeError):
        print(RuntimeError)
        