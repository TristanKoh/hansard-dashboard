import math

import pandas as pd

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
keyword_search = False
KEYWORD = "autonomous vehicle"

# Change this to True/False if searching by parliament sitting
parliament_sitting = False

# "PARLIAMENT_NO: PARLIAMENT_NO"
PARLIAMENT_NO = "13: 13"

# Search by MP
mp_name = True
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
driver.find_element_by_xpath('//*[@id="divmpscreen2"]/div[2]/div[3]/div/button[2]').click()
driver.switch_to.window(driver.window_handles[1])

# Click first link on results page
link = driver.find_element_by_xpath('//*[@id="searchResults"]/table/tbody[1]/tr[1]/td[2]/a')
driver.execute_script('arguments[0].click();', link)
driver.switch_to.window(driver.window_handles[2])


# TODO: Abstract the structure of the scraping into a separate class
"""
We now need to tag the speaker's name to what they said: One column for the name and the other for the text

We use two lists, one with the para_text, the other as MP tag that is the same length as para_text:
In the end we will get a dataframe, one column with the MP tag, and the other with the text. 
Each row corresponds with a paragraph, and each paragraph will be labelled with the MP's name.

Implementation:
Since para_text contains the text of the MP denoted with <strong>, we save the indices of those in para_text with <strong> 
in a separate list tag_bold.

We then initialise the MP tag list that is same length as para_text and loop over the this list
If the index is in tag_bold, we know that this paragraph has a new speaker, and hence we write the speaker's name to the equivalent index
in the names list. 

We maintain a counter that increments by one everytime there is a match between the tag_bold and index, 
because the bolded list does not have empty strings and is a different length from the para_text list.
But the bolded list lists names in chronological order (ie in the order in which they speak), and hence we can follow the chronology of the
speeches as well.

We can then forward fill the empty strings with the most recent MPs name in the column.
"""

# Find all bolded elements and paragraphs
bolded = driver.find_elements_by_tag_name('strong')
para_text = driver.find_elements_by_tag_name('p')

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
        names[index] = bolded[bolded_counter].text
        bolded_counter += 1
        print(bolded_counter)
    
    elif index not in tag_bold :
        pass


# Export to csv
# df_text_w_names = pd.DataFrame(
#     {"names" : names,
#     "text" : [para.text for para in para_text]
#     }
# )

# df_text_w_names.to_csv(r"C:\Users\Tristan\Desktop\Projects\hansard-dashboard\hansard-dashboard-repo\Data\df_text_w_names.csv")


# Continue scraping
# Store current window handle
search_page_handle = driver.current_window_handle

# Get total number of results
result_string = driver.find_element_by_xpath('//*[@id="searchResults"]/div[1]/div').text
result_string = result_string.split()
total_no_of_results = int(result_string[6])

# Divide by 20 because each page only loads 20 responses, round up to nearest whole number
last_page_index = math.ceil(total_no_of_results / 20)


# TODO: Figure out control flow for headless driver
for index, pages in enumerate(range(1,(last_page_index + 1))):
    
    # Iterate through the number of links on the search page to access individual parliamentary debates
    # ints are from 1 until 20 because there are 20 search results per page

    # NOTE: Change range to 21 to scrape total number of links
    for number in range(1, NO_OF_LINKS + 1):
        print("number", number)

        # Check if link exists, if it is a page that shows less than 20 results
        if len(driver.find_elements_by_xpath(f'//*[@id="searchResults"]/table/tbody[{number}]/tr[1]/td[2]/a')) != 0:    
            # Go to each link
            link = driver.find_element_by_xpath(f'//*[@id="searchResults"]/table/tbody[{number}]/tr[1]/td[2]/a')
            driver.execute_script('arguments[0].click();', link)
            driver.switch_to.window(driver.window_handles[2])
            
            # TODO: Scrape the text
            # Wait until title has loaded
            WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="right1"]/div[2]/span/h1/strong')))


            # Go back to results page
            driver.close()
            driver.switch_to_window(search_page_handle)
        

        #TODO: Scenario where there is only 1 result on the page, xpath of link changes

    # Go to next page
    driver.switch_to_window(search_page_handle)
    
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
#         "raw_text" : [],
#         "speaking_sequence" : []
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
#         "raw_text" : [],
#         "speaking_sequence" : []
#         }

#     # etc

# }
