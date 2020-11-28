# Pc Builder
## About

**Pc Builder** is a Python program that finds the best build for your budget. It creates up-to 4 builds per request, which are, *Desired*, *Recommended By Algorithm*, *A bit cheaper* and *A bit expensive*. These vary based on the input. You can also examine build parts and compare with their competitors on the graph.

<p align="center">
  <img alt="Pc Builder main window" src="https://raw.githubusercontent.com/starbuckr/pcbuilder/main/images/main-window.png">
</p>

# Installation
## Requirements
* [PyQT5](https://pypi.org/project/PyQt5/)
* [PyQTGraph](https://pypi.org/project/pyqtgraph/)
* [Selenium](https://pypi.org/project/selenium/)
* [PyMongo](https://pypi.org/project/pymongo/)
* [CurrencyConverter](https://pypi.org/project/CurrencyConverter/)
* Firefox (Required for scraping)

## Creating Database

When you run **main.py** it will automatically generate all the database files via web scraping. It may take a while. After the scraping, price-performance ratios will be automatically created.

### Run
```
python /src/gui/main.py
```

## Graph

<p align="center">
  <img alt="Graph Window" src="https://raw.githubusercontent.com/starbuckr/pcbuilder/main/images/graph.png">
</p>
