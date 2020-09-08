
import math

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-gpu')

driver = webdriver.Chrome(ChromeDriverManager().install())
url = 'https://sprs.parl.gov.sg/search/home'
driver.get(url)

# Set search paramters
# Either search by keyword or parliament sitting
# NOTE: Only keyword_search or parliament_sitting can be true at the same time!!

# Change this to True/False if searching by keyword
keyword_search = True
KEYWORD = "autonomous vehicle"

# Change this to True/False if searching by parliament sitting
parliament_sitting = False

# "PARLIAMENT_NO: PARLIAMENT_NO"
PARLIAMENT_NO = "13: 13"

# Number of links to scrape on each page, max 20
# NOTE: Don't enter beyond 20
NO_OF_LINKS = 20


# Dictionary structure to store scraped data
# One dictionary for each parliament no, 
# one dictionary for each sitting, 
# one dictionary for text by mp name

HANSARD_PARLIAMENT_NO_13 = {

    "sitting_1_dict" : {
        "session_no" : [],
        "volume_no" : [],
        "sitting_date" : [],
        "section_name" : [],
        "title" : [],
        "MPs_speaking" : [],
        "raw_text" : []
        "text_by_MPs_dict" : {
            "MP_name_1" : [],
            "MP_name_2" : []
            # Etc

        }
    }

    "sitting_2_dict" : {
        "session_no" : [],
        "volume_no" : [],
        "sitting_date" : [],
        "section_name" : [],
        "title" : [],
        "MPs_speaking" : [],
        "raw_text" : [],
        "text_by_MPs_dict" : {
            "MP_name_1" : [],
            "MP_name_2" : []
            # Etc

        }
    }

    # etc

}


## Search page
if keyword_search == True:
    # Select search box and search
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="divmpscreen2"]/div[2]/div[1]/div/div[1]/input')))
    search_box = driver.find_element_by_xpath('//*[@id="divmpscreen2"]/div[2]/div[1]/div/div[1]/input')
    search_box.send_keys(KEYWORD)

elif parliament_sitting == True:
    # Select parliament sitting
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="divmpscreen2"]/div[2]/div[1]/div/div[2]/select')))
    parliament_sitting_select = Select(driver.find_element_by_xpath('//*[@id="divmpscreen2"]/div[2]/div[1]/div/div[2]/select'))
    parliament_sitting_select.select_by_value(PARLIAMENT_NO)


# Click search
driver.find_element_by_xpath('//*[@id="divmpscreen2"]/div[2]/div[3]/div/button[2]').click()
driver.switch_to.window(driver.window_handles[1])

# Store current window handle
search_page_handle = driver.current_window_handle

# Recursive version
# TODO: Debug
# Chrome quits after the first 5 links: Means that code has run until the first if statement but has not loaded the next page

def crawl_pages():
    # find elements returns a list, if there is something, then length would not be 0
    check_nextpage_button = len(driver.find_elements_by_xpath('//*[@id="searchResults"]/div[3]/section/ul/li[1]/a/em'))

    if check_nextpage_button == 0:
        driver.quit()
    elif check_nextpage_button != 0:
        next_page = driver.find_element_by_xpath('//*[@id="searchResults"]/div[3]/section/ul/li[1]/a/em')
        
        # ints are from 1 until 20 because there are 20 search results per page
        for number in range(1,21):
            
            # Check if link exists
            if len(driver.find_elements_by_xpath(f'//*[@id="searchResults"]/table/tbody[{number}]/tr[1]/td[2]/a')) != 0:    
                # Go to each link
                link = driver.find_element_by_xpath(f'//*[@id="searchResults"]/table/tbody[{number}]/tr[1]/td[2]/a')
                driver.execute_script('arguments[0].click();', link)
                driver.switch_to.window(driver.window_handles[2])
                
                # TODO: Scrape the text
                WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="right1"]/div[2]/span/h1/strong')))
                titles.append(driver.find_element_by_xpath('//*[@id="right1"]/div[2]/span/h1/strong').text)

                # Go back to results page
                driver.close()
                driver.switch_to_window(search_page_handle)

        # Go to next page
        driver.switch_to_window(search_page_handle)
        driver.execute_script('arguments[0].click();', next_page)
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div/div[1]/h3')))
        crawl_pages()

crawl_pages()