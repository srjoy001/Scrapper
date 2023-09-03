import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from transformers import pipeline
import time

summarizer = pipeline("summarization")

rows = []
with open('output.csv', 'r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    fieldnames = reader.fieldnames + ['contact', 'dataset_links', 'abstract_summary']
    for row in reader:
        rows.append(row)


# Configure Chrome WebDriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.maximize_window()

popup_closed = False       
with open('datasets.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        try:
            driver.get(row['Link'])

            time.sleep(6)  # Allow time for the page to load

            

            if popup_closed ==False:
                # Handle the cookie consent popup
                cookie_popup = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'cookie-consent'))
                )

                if cookie_popup:
                    accept_button = cookie_popup.find_element(By.XPATH, '//button[text()="Accept All Cookies"]')
                if accept_button:
                    accept_button.click()
                    popup_closed = True

            abstract_content = driver.find_element(By.CSS_SELECTOR, 'div.abstract-content')
            p_tags = abstract_content.find_elements(By.TAG_NAME, 'p')
            abstract_text = ''

            for p_tag in p_tags:
                abstract_text += p_tag.text.strip()

            row['abstract_summary'] = abstract_text

            article_info = driver.find_element(By.CSS_SELECTOR, 'div.articleinfo')
            p_tags = article_info.find_elements(By.TAG_NAME, 'p')
            dataset_links = []
            contact = ''

            print('dataset-links',dataset_links)
            print('contacts--->',contact)

            for p_tag in p_tags:
                strong_tag = p_tag.find_element(By.TAG_NAME, 'strong')
                if strong_tag.text == 'Data Availability:':
                    links = p_tag.find_elements(By.TAG_NAME, 'a')
                    dataset_links = [link.get_attribute('href') for link in links]
                elif '@' in p_tag.text:
                    contact = p_tag.text.strip()

            row['dataset_links'] = ', '.join(dataset_links)
            row['contact'] = contact

            writer.writerow(row)

        except Exception as e:
            print(f"Error occurred while processing '{row['Link']}': {str(e)}")


        
