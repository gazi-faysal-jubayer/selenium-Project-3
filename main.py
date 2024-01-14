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
driver.get("https://www.qualitycheck.org/search/?keyword=#accreditationprogram=Home%20Care&deemedprogram_parent=Home%20Health%20Agency,Home%20Infusion%20Therapy,Hospice%20Agency&addoncertification=Community-Based%20Palliative%20Care%20Certification&pg=4")
driver.implicitly_wait(20)
time.sleep(5)
providers_data = []

items = driver.find_elements(By.CSS_SELECTOR, "div.item.hawk-contentItem")
print(len(items))

for i in range(len(items)):
    items = driver.find_elements(By.CSS_SELECTOR, "div.item.hawk-contentItem")
    parent = items[i].find_element(By.CSS_SELECTOR, "div.parent")
    title = parent.find_element(By.CSS_SELECTOR, "a.svg-ikon-base64-gold-seal").text
    kk = parent.find_element(By.CSS_SELECTOR, "div.hawki").text.split('\n')
    if len(kk) == 3:
        hco = kk[0].replace('HCO ID: ', '')
        street = kk[1]
        city = kk[2].split(', ')[0]
        state = kk[2].split(', ')[1].split(' ')[0]
        gip = kk[2].split(', ')[1].split(' ')[1]
    elif len(kk) == 4:
        hco = kk[0].replace('HCO ID: ', '')
        street = kk[2]
        city = kk[3].split(', ')[0]
        state = kk[3].split(', ')[1].split(' ')[0]
        gip = kk[3].split(', ')[1].split(' ')[1]
        
    time.sleep(4)
    btn = parent.find_element(By.XPATH, f"//a[@id='HawkSearchItems_lvItems_ctrl{i}_ctl00_link_lnkViewReport']")
    driver.execute_script("arguments[0].click();", btn)
    # time.sleep(4)
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
    time.sleep(10)
    try:
        items = driver.find_elements(By.CSS_SELECTOR, "div.item.hawk-contentItem")
        child = items[i].find_element(By.CSS_SELECTOR, "div.child")
        childs = child.find_elements(By.CSS_SELECTOR, "div.hawk-childContent")
        print(len(childs))

        for k in range(len(childs)):
            Ctitle = childs[k].find_element(By.CSS_SELECTOR, "h3.title.hawk-contentTitle.hawki").text
            key = childs[k].find_element(By.CSS_SELECTOR, "div.hawki").text.split('\n')
            if len(key) == 2:
                Cstreet = key[0]
                Ccity = key[1].split(',')[0]
                Cstate = key[1].split(',')[1]
                Cgip = key[1].split(',')[2]
            elif len(key) == 3:
                Cstreet = key[1]
                Ccity = key[2].split(',')[0]
                Cstate = key[2].split(',')[1]
                Cgip = key[2].split(',')[2]
            
            Cdata = {
                'Title': Ctitle,
                'HCO': '',
                'Subheading': '',
                'Street': Cstreet,
                'City': Ccity,
                'State': Cstate,
                'GIP': Cgip,
                'Accreditation': '',
                'Accreditation Decision': '',
                'Effective Date': '',
                'Last Full Survey Date': '',
                'Last On-Site Survey Date': ''
            }
            print(Cdata)
            providers_data.append(Cdata)
    except (TimeoutException, StaleElementReferenceException) as e:
        # print(f"Exception: {e}")
        print(f"Element for page not found. Exiting the loop.")
        # break
        

x = '3'
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
