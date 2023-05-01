
# TODO: How to access this function from another .py file
def tag_mp_name_to_text(bolded_text, para_text) :
    
    # Check the para_text list for the indices where there is <bold>: This means that there is a new speaker for that paragraph
    tag_bold = []
    for index, para in enumerate(para_text):
        if "<strong>" in para.get_attribute('innerHTML'):
            tag_bold.append(index)


    # Maintain a counter for the index of bolded that starts at 1 (since the first bolded element is the name of the debat)
    # Loop over para_text, check if the index is in tag_bold.
    # If it is, insert the relevant name from the bolded list at the current index
    # If not, don't do anything

    names = [""] * len(para_text)
    bolded_counter = 1

    for index, para in enumerate(para_text):
        
        if index in tag_bold:
            names[index] = bolded_text[bolded_counter].text
            bolded_counter += 1
        
        elif index not in tag_bold :
            pass
    
    return names, [para.text for para in para_text]
        
     

import math
import pandas as pd

import sys
sys.path

from selenium import webdriver
from selenium.webdriver import ActionChains
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

# Search by MP
mp_name = False
MP_NAME = "74: 'Pritam Singh'"


# Number of links to scrape on each page, max 20
# NOTE: Don't enter beyond 20
NO_OF_LINKS = 20

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

elif mp_name == True:
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="advSearchLabel"]')))
    
    # Open advanced search
    advanced_search = driver.find_element_by_xpath(('//*[@id="advSearchLabel"]'))
    driver.execute_script('arguments[0].click();', advanced_search)

    # Click by MP radio button
    driver.find_element_by_xpath('//*[@id="byMP"]').click()


    # Find MP list box and select by MP name
    mp_name_select = Select(driver.find_element_by_xpath('//*[@id="portDIV"]/select'))
    mp_name_select.select_by_value(MP_NAME)



# Click search
WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="divmpscreen2"]/div[2]/div[3]/div/button[2]')))
search_button = driver.find_element_by_xpath('//*[@id="divmpscreen2"]/div[2]/div[3]/div/button[2]')
driver.execute_script('arguments[0].click();', search_button)
driver.switch_to.window(driver.window_handles[1])


# Store current window handle
search_page_handle = driver.current_window_handle

# Get total number of results
WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchResults"]/div[1]/div')))
result_string = driver.find_element_by_xpath('//*[@id="searchResults"]/div[1]/div').text
result_string = result_string.split()
total_no_of_results = int(result_string[6])

# Divide by 20 because each page only loads 20 responses, round up to nearest whole number
last_page_index = math.ceil(total_no_of_results / 20)

# Initialise empty dictionary to store results
HANSARD_BY_MP ={}


# Click first link on results page
# link = driver.find_element_by_xpath('//*[@id="searchResults"]/table/tbody[1]/tr[1]/td[2]/a')
# driver.execute_script('arguments[0].click();', link)
# driver.switch_to.window(driver.window_handles[2])


# TODO: Figure out control flow for headless driver
for index, pages in enumerate(range(1,(last_page_index + 1))):
    
    print("page", pages)
    # Iterate through the number of links on the search page to access individual parliamentary debates
    # ints are from 1 until 20 because there are 20 search results per page

    # NOTE: Change range to 21 to scrape total number of links
    for number in range(1, NO_OF_LINKS + 1):
        print("debate", number)

        # Check if link exists, if it is a page that shows less than 20 results
        if len(driver.find_elements_by_xpath(f'//*[@id="searchResults"]/table/tbody[{number}]/tr[1]/td[2]/a')) != 0 and number != NO_OF_LINKS:    
            # Go to each link
            link = driver.find_element_by_xpath(f'//*[@id="searchResults"]/table/tbody[{number}]/tr[1]/td[2]/a')
            driver.execute_script('arguments[0].click();', link)
            driver.switch_to.window(driver.window_handles[2])
            

            # Wait until title has loaded
            WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="right1"]/div[2]/span/h1/strong')))

            title = driver.find_element_by_xpath('//*[@id="right1"]/div[2]/span/h1/strong').text
            print(title)
            print("Scraping...")

            # Find all bolded elements and paragraphs
            bolded = driver.find_elements_by_tag_name('strong')
            paras = driver.find_elements_by_tag_name('p')

            names, para_text = tag_mp_name_to_text(bolded, paras)

            # Add new dictionary entry
            HANSARD_BY_MP[number] = {"title" : title, "names" : names, "text" : para_text}

            print("Debate scraped")

            # Go back to results page
            driver.close()
            driver.switch_to_window(search_page_handle)

        # TODO: How to stop the loop after accessing all the links on the first page
        elif number == NO_OF_LINKS :
            break
        

        #TODO: Scenario where there is only 1 result on the page, xpath of link changes

    # Go to next page
    driver.switch_to_window(search_page_handle)
    
    # TODO: Scraper clicks the next page, but does not scrape the links

    # Next page xpath reference changes after 1st page, so check if it is first iteration of loop
    if index == 0:
        next_page = driver.find_element_by_xpath('//*[@id="searchResults"]/div[3]/section/ul/li[1]/a/em')
        driver.execute_script('arguments[0].click();', next_page)
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div/div[1]/h3')))
    
    elif (index > 0) and (index < last_page_index - 1):
        next_page = driver.find_element_by_xpath('//*[@id="searchResults"]/div[3]/section/ul/li[3]/a/em')
        driver.execute_script('arguments[0].click();', next_page)
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div/div[1]/h3')))
    
    # If on last page, don't search for next page button
    elif index == last_page_index - 1:
        pass

# Export to csv

# df_HANSARD = {}

# for number in range(1, 21) :
#     df_HANSARD[number] = pd.DataFrame({
#         "title" : HANSARD_BY_MP[number]["title"],
#         "names" : HANSARD_BY_MP[number]["names"],
#         "text" : HANSARD_BY_MP[number]["text"]
#     })

# for number in range(1, 21) :
#     df_HANSARD[number].to_csv(rf"C:\Users\Tristan\Desktop\Projects\hansard-dashboard\hansard-dashboard-repo\Data\{number}.csv", encoding = "utf-8-sig")



# Dictionary structure to store scraped data - Search by MP
# one dictionary for each link (running index)

# HANSARD_BY_MP = {

#     1 : {
#         "parliament_no" : [],
#         "session_no" : [],
#         "volume_no" : [],
#         "sitting_no" : []
#         "sitting_date" : [],
#         "section_name" : [],
#         "title" : [],
#         "MPs_speaking" : [],
#         "text" : [],
#         "names" : []
#         }

#     2 : {
#         "parliament_no" : [],
#         "session_no" : [],
#         "volume_no" : [],
#         "sitting_no" : []
#         "sitting_date" : [],
#         "section_name" : [],
#         "title" : [],
#         "MPs_speaking" : [],
#         "text" : [],
#         "names" : []
#         }

#     # etc

# }
