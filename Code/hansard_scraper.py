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





# TODO: How to tag each body paragraph with the MPs name, given that not all of the paragraphs have the MPs name in it as string

# Click first link on results page
link = driver.find_element_by_xpath('//*[@id="searchResults"]/table/tbody[1]/tr[1]/td[2]/a')
driver.execute_script('arguments[0].click();', link)
driver.switch_to.window(driver.window_handles[2])

bolded = driver.find_elements_by_tag_name('strong')
para_text = driver.find_elements_by_tag_name('p')

# Two lists, one with the para_text, the other as MP tag, same length as para_text
# Use regex to find the name of the minister in between html <strong> MP_name <\strong>
# For para in para_text, if there is anything in between <strong> <\strong>, assign to the relevant corresponding index in MP tag
# After scraping, can forward fill all the blank indices.

for bold in bolded:
    print(bold.text)

tag_bold = []
string_test = [""]

for index, para in enumerate(para_text):
    if "<strong>" in para.get_attribute('innerHTML'):
        tag_bold.append(index)

for index, para in enumerate(para_text):
    if index not in tag_bold:


for row in string_test:
    print(row)
    print("-" * 40)






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

            titles.append(driver.find_element_by_xpath('//*[@id="right1"]/div[2]/span/h1/strong').text)

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

HANSARD_BY_MP = {

    1 : {
        "parliament_no" : [],
        "session_no" : [],
        "volume_no" : [],
        "sitting_no" : []
        "sitting_date" : [],
        "section_name" : [],
        "title" : [],
        "MPs_speaking" : [],
        "raw_text" : [],
        "speaking_sequence" : []
        }

    2 : {
        "parliament_no" : [],
        "session_no" : [],
        "volume_no" : [],
        "sitting_no" : []
        "sitting_date" : [],
        "section_name" : [],
        "title" : [],
        "MPs_speaking" : [],
        "raw_text" : [],
        "speaking_sequence" : []
        }

    # etc

}


test_dict = {}

test_dict["cat1"] = 1
test_dict["cat1"] = 2


test_dict["cat1"]
