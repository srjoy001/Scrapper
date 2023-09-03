import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from filter import is_relevant, has_image_relevance, has_ear_relevance
import csv

# Configure Chrome WebDriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.maximize_window()

# Variables
base_url = "https://journals.plos.org/plosone/browse/medicine_and_health_sciences?page="
start_page = 0
end_page = 2586

try:
    with open('output.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Check if the file is empty (no header row)
        if csvfile.tell() == 0:
            writer.writerow(['Title', 'Link'])  # Write the header row

except FileExistsError:
    pass

# Main scraping function


def scrape_page(url):
    driver.get(url)
    time.sleep(10)  # Allow time for the page to load

    # Find and collect desired elements
    titles = driver.find_elements(By.CSS_SELECTOR, 'h2.title > a')
    for title in titles:
        value = title.get_attribute("innerHTML")
        if not is_relevant(value) or not has_image_relevance(value):
            continue
        else:
            href = title.get_attribute("href")
            print("Value:", value)
            print("Href:", href)
            print("-" * 50)

            with open('output.csv', 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([value, href])


# Scrape pages from start_page to end_page
for page in range(start_page, end_page + 1):
    page_url = base_url + str(page)
    print("Scraping page:", page)
    scrape_page(page_url)

# Clean up
driver.quit()
