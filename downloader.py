from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


# Load CSV file
with open('output.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row
    for row in reader:
        title = row[0]
        link = row[1]

        # Configure Chrome options
        options = Options()
        options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("prefs", {
            "download.default_directory": "C:\Users\SR Joy\Documents\Projects\PlosOne\pdf",  # Replace with your desired download directory
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True  # Ensure that PDFs are downloaded instead of opening in a new tab
        })

        # Start Chrome WebDriver with modified options
        driver = webdriver.Chrome(service=Service("path/to/chromedriver"), options=options)  # Replace with the path to your chromedriver executable

        try:
            # Visit the link
            driver.get(link)

            # Wait for the cookie consent popup to appear
            cookie_popup = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'cookie-consent'))
            )

            # Click the "Accept All Cookies" button
            accept_button = cookie_popup.find_element(By.XPATH, '//button[text()="Accept All Cookies"]')
            accept_button.click()

            # Find and click the "downloadPdf" link
            download_link = driver.find_element(By.ID, 'downloadPdf')
            download_link.click()

            # Wait for the download to complete
            # Add appropriate waiting logic here

        except Exception as e:
            print(f"Error occurred while processing '{title}': {str(e)}")

        finally:
            driver.quit()

print("PDF download completed.")
