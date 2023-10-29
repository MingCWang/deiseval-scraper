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
   
'''
To Do: NEED TO SOLVE WHY THIS IS INDEX OUT OF RANGE FROM THE POPUP TEXT

'''
def get_data_from_popup(driver, links):
    '''get course description from the popup'''
    try:
        popup_link = links[0].get_attribute('href')[18:].split(',')[0].split("%")[0]
        popup_link = "https://registrar-prod.unet.brandeis.edu/registrar/schedule/" + popup_link
        driver.get(popup_link)
        # print("------------------")
        text = driver.find_element(By.XPATH, "//div[@id='coursepage']/p").text.split('\n')
        if text == ['']: # if the p tag is empty, then the description is in the second p tag
            text = driver.find_element(By.XPATH, "//div[@id='coursepage']/p[2]").text.split('\n')
        try: # edge case where the description is in the 4th p tag
            description = WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.XPATH, "//div[@id='coursepage']/p[4]")))
            if description.text != '':
                text = description.text.split('\n')
        except: 
            pass
        # print(text)
        text = [line for line in text if line != '']
        
        if len(text) == 2 or len(text) == 1:
            description = text[0]
            prerequisites = ""
        elif len(text) != 0: 
            description = text[1]
            prerequisites = text[0]
        else: 
            description = ""
            prerequisites = ""
    except Exception as e:
        print('Error in get_data_from_popup', e)
    # print(description, prerequisites)
    return description, prerequisites

def find_class_table(driver):
    '''find the table that contains the course data'''
    class_table = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'classes-list')))
    class_list = class_table.find_elements(By.TAG_NAME, 'tr')
    return class_list

def get_course_data(class_list, i, driver):
    '''get course data from the table'''
    
    try: 
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
        description, prerequisites = get_data_from_popup(driver, links)
    except Exception as e:
        print('Error in get_course_data', e)
    return course, courseTitle, syllabus, instructor, requirements, prerequisites, description

def navigate_to_current_term(driver, value, count):
    if count == 3: # loop through terms based on the options value
        count = 1
        value += 8 
    else:
        value += 1
        count += 1
    print("current value: ", value)
    try:
        selected_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//select[@name="strm"]/option[@value="{str(value)}"]')))
        selected_text = selected_option.text.strip() # get the text of the option
        selected_option.click() # select the option
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "searchsubmit"))).click() # click the search button
    except Exception as e:
        print('error', e)
    return selected_text, value, count

   
   