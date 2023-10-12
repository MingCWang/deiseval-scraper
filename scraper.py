from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

from helper_function import select_subject, select_term
import time
import os



def driver():
    '''creates driver instance'''
    driver = webdriver.Chrome()
    driver.get("https://registrar-prod.unet.brandeis.edu/registrar/schedule/search")
    return driver

def scraper(driver, start, end):
    '''main scraper function'''
    count = 0
    value = start - 1
    try:
        while value < end:
            if count == 3:
                count = 1
                value += 8
            else:
                value += 1
                count += 1
            select_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "strm")))
            select = Select(select_element)
            select.select_by_value(str(value))
            print(value)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "searchsubmit"))).click()
            time.sleep(10)
           
            # select_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "subject")))
            # select = Select(select_element)
            # for index, option in enumerate(select.options):
            #     select_subject(index, option, driver)
    except Exception as e: 
        print('Error: ', e)


def main():
	start = 1201 
	end = 1233
	webdriver = driver()
	scraper(webdriver, start, end)
	print(f'\n==========================================\nDOWNLOAD COMPLETED\n==========================================')


main()