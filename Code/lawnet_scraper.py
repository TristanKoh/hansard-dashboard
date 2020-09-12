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

# Set your login credentials and search parameters
USERNAME = 'e0335719'
PASSWORD = ''
SEARCH_TERM = "spandeck"

driver = webdriver.Chrome(ChromeDriverManager().install())
url = 'https://proxylogin.nus.edu.sg/lawproxy1/public/login.asp?logup=false&url=http://www.lawnet.sg/lawnet/ip-access'
driver.get(url)

## Login page
# Select network_domain
network_domain_select = Select(driver.find_element_by_xpath('//*[@id="main-content"]/table/tbody/tr/td/form/table/tbody/tr[1]/td[3]/select'))
network_domain_select.select_by_value('NUSSTU')

username_field = driver.find_element_by_xpath('//*[@id="main-content"]/table/tbody/tr/td/form/table/tbody/tr[2]/td[3]/input')
username_field.send_keys(USERNAME)

password_field = driver.find_element_by_xpath('//*[@id="main-content"]/table/tbody/tr/td/form/table/tbody/tr[3]/td[3]/input')
password_field.send_keys(PASSWORD)

# Click submit
driver.find_element_by_xpath('//*[@id="main-content"]/table/tbody/tr/td/form/div/input').click()

## NUS Proxy Accept page
driver.find_element_by_xpath('//*[@id="main-content"]/table/tbody/tr[2]/td[4]/div/form/input').click()

## Lawnet main search page

# Search box
search_box = driver.find_element_by_xpath('//*[@id="basicSearchKey"]')
search_box.send_keys(SEARCH_TERM)
driver.find_element_by_link_text('Search').click()

## Main results page

# As long there is a next page button, continue scraping

# TODO: Figure out control flow
while driver.find_element_by_xpath('//*[@id="tabs-1"]/div[3]/form[2]/div/div/ul/li[8]/a').get_attribute('href') != None:
    
    # Get the next page link
    next_page = driver.find_element_by_xpath('//*[@id="tabs-1"]/div[3]/form[2]/div/div/ul/li[8]/a').get_attribute('href')

    # Get all the case links in the first page
    links = driver.find_elements_by_class_name('document-title')
    links = [link.get_attribute('href') for link in links]

    # Scrape each case for each link
    # TODO: Find a way to save the text in a structured way
    for link in links:
        driver.get(link)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'contentsOfFile')))
        case_web_element = driver.find_element_by_class_name('contentsOfFile')
        case = case_web_element.get_attribute('innerHTML')
    
    # Go to next page
    driver.get(next_page)


# Switch tabs
# driver.switch_to.window(driver.window_handles[1])

text_file = open(r"C:\Users\Tristan\Desktop\Projects\blackstone\sample.txt", "w", encoding= "utf-8")
n = text_file.write(case)
text_file.close()