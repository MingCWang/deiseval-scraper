from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select


def select_subject(index, option, driver):
    select_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "subject")))
    select = Select(select_element)
    select.select_by_index(index)
    option_text = option.text.strip()  # .strip() removes leading and trailing whitespac
    print(f"Option {index}: {option_text}")
    
def select_term(i, count, driver):
    ''' Selects the term from dropdown menu'''
    select_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "strm")))
    select = Select(select_element)
    select.select_by_value(str(i))
    if count == 3:
        count = 0
        i = i - 2 + 9
    else:
        count += 1
    return i
   
   
   