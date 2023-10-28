from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select


def driver():
    '''creates driver instance'''
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options) # use this line if you want to run the scraper in the background
    # driver = webdriver.Chrome()
    driver.get("https://registrar-prod.unet.brandeis.edu/registrar/schedule/search")
    return driver

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
   
def get_data_from_popup(driver, links):
    '''get course description from the popup'''
    popup_link = links[0].get_attribute('href')[18:].split(',')[0].split("%")[0]
    popup_link = "https://registrar-prod.unet.brandeis.edu/registrar/schedule/" + popup_link
    driver.get(popup_link)
    description = driver.find_element(By.XPATH, "//div[@id='coursepage']/p").text.split('\n')[0]
    return description

def find_class_table(driver):
    '''find the table that contains the course data'''
    class_table = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'classes-list')))
    class_list = class_table.find_elements(By.TAG_NAME, 'tr')
    return class_list

def get_course_data(class_list, i, driver):
    '''get course data from the table'''
    data = class_list[i].find_elements(By.TAG_NAME, 'td')
    links = data[0].find_elements(By.TAG_NAME, 'a')
    syllabus = ''
    if len(links) == 2:
        syllabus = links[1].get_attribute('href')
    else:
        syllabus = 'Not Provided'
    course = links[0].text
    courseTitle = data[1].find_element(By.TAG_NAME, 'strong').text
    span = data[1].find_elements(By.TAG_NAME, 'span') # get the requirements from the list of span tags
    requirements = [requirement.text for requirement in span]
    instructor = data[4].text
    description = get_data_from_popup(driver, links)
    
    return course, courseTitle, syllabus, instructor, requirements, description

def navigate_to_current_term(driver, value, count):
    if count == 3: # loop through terms based on the options value
        count = 1
        value += 8
    else:
        value += 1
        count += 1
    selected_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//select[@name="strm"]/option[@value="{str(value)}"]')))
    selected_text = selected_option.text.strip() # get the text of the option
    selected_option.click() # select the option
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "searchsubmit"))).click() # click the search button
    
    return selected_text, value

   
   