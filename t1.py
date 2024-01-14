from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time
import csv

# Opening website
driver = webdriver.Chrome()
driver.get("https://www.qualitycheck.org/search/?keyword=#accreditationprogram=Home%20Care&deemedprogram_parent=Home%20Health%20Agency,Home%20Infusion%20Therapy,Hospice%20Agency&addoncertification=Community-Based%20Palliative%20Care%20Certification")
driver.implicitly_wait(20)
time.sleep(5)
items = driver.find_elements(By.CSS_SELECTOR, "div.item.hawk-contentItem")
print(len(items))

for i in range(len(items)):
    items = driver.find_elements(By.CSS_SELECTOR, "div.item.hawk-contentItem")
    child = items[i].find_element(By.CSS_SELECTOR, "div.child")
    childs = child.find_elements(By.CSS_SELECTOR, "div.hawk-childContent")
    print(len(childs))

    for j in range(len(childs)):
        title = childs[j].find_element(By.CSS_SELECTOR, "h3.title.hawk-contentTitle.hawki").text
        key = childs[j].find_element(By.CSS_SELECTOR, "div.hawki").text.split('\n')
        if len(key) == 2:
            street = key[0]
            city = key[1].split(',')[0]
            state = key[1].split(',')[1]
            gip = key[1].split(',')[2]
        elif len(key) == 3:
            street = key[1]
            city = key[2].split(',')[0]
            state = key[2].split(',')[1]
            gip = key[2].split(',')[2]
        print(title)
        
        data = {
            'Title': title,
            'HCO': '',
            'Subheading': '',
            'Street': street,
            'City': city,
            'State': state,
            'GIP': gip,
            'Accreditation': '',
            'Accreditation Decision': '',
            'Effective Date': '',
            'Last Full Survey Date': '',
            'Last On-Site Survey Date': ''
        }
        print(data)
    

driver.quit()