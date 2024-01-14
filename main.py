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
providers_data = []

items = driver.find_elements(By.CSS_SELECTOR, "div.item.hawk-contentItem")
print(len(items))

for i in range(len(items)):
    items = driver.find_elements(By.CSS_SELECTOR, "div.item.hawk-contentItem")
    parent = items[i].find_element(By.CSS_SELECTOR, "div.parent")
    title = parent.find_element(By.CSS_SELECTOR, "a.svg-ikon-base64-gold-seal").text
    hco = parent.find_element(By.XPATH, "(//div[@class='hawki'])").text.split('\n')[0].replace('HCO ID: ', '')
    street = parent.find_element(By.XPATH, "(//div[@class='hawki'])").text.split('\n')[1]
    city = parent.find_element(By.XPATH, "(//div[@class='hawki'])").text.split('\n')[2].split(', ')[0]
    state = parent.find_element(By.XPATH, "(//div[@class='hawki'])").text.split('\n')[2].split(', ')[1].split(' ')[0]
    gip = parent.find_element(By.XPATH, "(//div[@class='hawki'])").text.split('\n')[2].split(', ')[1].split(' ')[1]
    time.sleep(4)
    btn = parent.find_element(By.XPATH, f"//a[@id='HawkSearchItems_lvItems_ctrl{i}_ctl00_link_lnkViewReport']")
    driver.execute_script("arguments[0].click();", btn)
    
    e = driver.find_element(By.XPATH, "//table[@class='x-table x-border x-frilled x-seal x-first-left-mobi']")
    els = e.find_elements(By.CLASS_NAME, "x-row")
    for j in range(len(els)):
        eld = els[j].find_elements(By.CLASS_NAME, "x-cell")
        aName = eld[1].text
        aDecision = eld[2].text.split('\n')[1]
        eDate = eld[3].text.split('\n')[1]
        lfsDate = eld[4].text.split('\n')[1]
        lossDate = eld[5].text.split('\n')[1]
        data = {
            'Title': title,
            'HCO': hco,
            'Subheading': '',
            'Street': street,
            'City': city,
            'State': state,
            'GIP': gip,
            'Accreditation': aName,
            'Accreditation Decision': aDecision,
            'Effective Date': eDate,
            'Last Full Survey Date': lfsDate,
            'Last On-Site Survey Date': lossDate
        }
        providers_data.append(data)
        print(data)
    
    time.sleep(5)
    driver.back()
    # print(data)
    time.sleep(4)
    
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
        providers_data.append(data)
        

x = '1'
# Specify the CSV file path
csv_file_path = f'output-{x}.csv'

# Open the CSV file in write mode
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.DictWriter(csv_file, fieldnames=providers_data[0].keys())

    # Write the header
    csv_writer.writeheader()

    # Write the data rows
    csv_writer.writerows(providers_data)

print(f'CSV file "{csv_file_path}" has been created.')

# Close the browser window
driver.quit()