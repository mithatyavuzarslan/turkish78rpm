##########################
#  This Python script is to create the dataset of Turkish 78 rpm recordings published between 1905-1965. #
# The collection is the appendix of the book "Git Zaman Gel Zaman" written by Cemal Unlu. #
# Selenium package in Python was used to pull data from each page on http://tasplak.pankitap.com where users can access the data contains more than 16000 entries in a JS table #
# Reference to the book: Ünlü, C. (2016). Git zaman gel zaman: Fonograf-gramofon-taş plak. Pan Yayıncılık. #
# Reference to the digital appendix: http://tasplak.pankitap.com #
# Script by: mithatyavuzarslan@gmail.com #
##########################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

import numpy as np
import pandas as pd

# Initialize the WebDriver
service = Service('C:/Users/Dell/.cache/selenium/chromedriver/win64/126.0.6478.182/chromedriver.exe')  # Change this to the path of your chromedriver
driver = webdriver.Chrome(service=service)
# Open the target web page
driver.get('http://tasplak.pankitap.com')

# DEFINE ARRAY
array_records=np.array([])


# Define the number of pages to scrape. Someho the page needs to be clicked on the next button twice.
num_pages = 807*2

for i in range(num_pages):
    try:
        # Wait for the grid cells to be present
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'td[role="gridcell"]'))
        )

        # Extract the data
        data = [element.text for element in elements]
        array_records=np.append(array_records,data)
        #print(data)


        if i < num_pages - 1:  # Avoid clicking "Next" on the last iteration
            # Wait until the "Next" button is clickable
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.k-link.k-pager-nav[title="Bir sonraki sayfaya git"]'))
            )

            # Click the "Next" button
            next_button.click()

            # Wait for the new content to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'td[role="gridcell"]'))
            )
    except Exception as e:
        continue

# Close the WebDriver
driver.quit()

# Define column names
columns = ['Company', 'CatalogNo', 'TrackName', 'Makam', 'Singer', 'PublishNo', 'Description']


# Create the DataFrame
reshaped_array = np.array(array_records).reshape(-1, 7)
dataFrame_records=pd.DataFrame(reshaped_array,columns=columns)

