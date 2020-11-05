from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from currency_converter import CurrencyConverter

def get_price(driver, c, url):
    driver.get(url)
    try:
        elements = WebDriverWait(driver, 2).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'PriceLabel-sc-7gzlos-0'))
        )
    except(TimeoutException):
        print(url + " Timeout")
        return ""
    finally:
        print(url + " Done")
        
    if elements == []:
        return ""

    gbp_price = elements[0].text[1:].replace(",", "")
    price = c.convert(float(gbp_price), 'GBP', 'USD')
    return int(price)