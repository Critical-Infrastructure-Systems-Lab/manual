---
layout: post
title: How to Scrap a Website to Gather Reservoir Storage Data?
description: >
  Scraping a website with Python
sitemap: false
hide_last_modified: true
---

# How to Scrap a Website to Gather Reservoir Storage Data?
>**Edited by: Shanti Shwarup Mahto**

### **Do you need to extract information from a website that doesn't offer a download feature? This post is for you!**

Imagine you need to access observed reservoir storage data that is publicly available. While it's not common to find such data publicly due to government restrictions, the Thailand government shares daily observed storage data (and other water-related information) of their reservoirs. This data is displayed on [Thai Water](https://www.thaiwater.net/water/dam/large/).

Although you can visualize and obtain maps in image format from the website, downloading the data directly used to create these maps and figures is not possible. This is where “web scraping” comes in handy. Web scraping allows you to extract and save data displayed on a webpage. For example, if you want to scrape reservoir storage data from an HTML table into an Excel sheet, you could manually copy-paste it. However, when dealing with thousands of webpages where data changes dynamically daily, this approach is impractical. The data updates with changes in dates, making automation necessary.

So, how do you do it? Let’s dive in!

In this blog post, I'll walk you through the steps of scraping a website to collect reservoir storage data. We'll cover the basics of web scraping, the tools you'll need, and provide a step-by-step guide to get you started. But before we get into the specifics, let's understand some basic fundamentals. 

## What is Web Scraping?

Web scraping is a powerful technique for gathering data that isn't readily available through APIs or other conventional means. It involves automatically extracting information from websites using software that simulates human browsing. This allows you to collect large amounts of data quickly and efficiently.

## Tools You’ll Need

Before we dive into the process, let's go over the tools you'll need:

1. **Python**: A versatile programming language that's great for web scraping.
2. **BeautifulSoup**: A Python library for parsing HTML and XML documents.
3. **Requests**: A Python library for making HTTP requests.
4. **Selenium**: A Python library for automating web browsers.
5. **Pandas**: A Python library for data manipulation and analysis.

You can install the above libraries using conda or pip:

>**conda install -c conda-forge requests beautifulsoup4 selenium pandas**

You will also need a web driver for Selenium. For example, if you're using Chrome, you can download the ChromeDriver from [here](https://sites.google.com/chromium.org/driver/downloads).

## Step-by-Step Guide

### Step 1: Setup the Environment

Ensure you have the necessary libraries installed and the ChromeDriver downloaded. Place the ChromeDriver in a directory you can easily reference in your script.

### Step 2: Define Helper Functions

Define functions to handle the extraction of table data, writing data to a CSV file, navigating the website, and processing data for specific dates.

- **Extract Table Data**: This function parses the HTML content and extracts table data.
- **Write Table to CSV**: This function writes the extracted table data to a CSV file.
- **Go Back One Day**: This function navigates to the previous day's data on the website.
- **Process Date**: This function processes the data for a specific date, extracting and saving it.

### Step 3: Main Scraping Function

Create a main function to handle the overall process of scraping data over a date range. This function will:

- Initialize the Selenium WebDriver.
- Navigate to the target website.
- Loop through the specified date range, processing data for each date.
- Save the data to CSV files in the specified directory.

### Step 4: Run the Script

Run your script to start the scraping process. Ensure your target directory for saving the CSV files exists.

## Complete Code Example

Here is the complete python code for reference:

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
import os
from datetime import datetime, timedelta

# Function to extract table data from the HTML content
def extract_table_data(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    table_container = soup.find('div', class_='MuiTableContainer-root')
    table_data = []

    if table_container:
        table = table_container.find('table', class_='MuiTable-root')
        headers = [header.text for header in table.find_all('th')]
        rows = table.find_all('tr')

        for row in rows:
            cells = row.find_all('td')
            if cells:
                row_data = [cell.text.strip() for cell in cells]
                table_data.append(row_data)
    
    return headers, table_data

# Function to write table data to CSV
def write_table_to_csv(headers, table_data, csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for row in table_data:
            writer.writerow(row)

# Function to go back one day
def go_back_one_day(driver):
    back_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="วันก่อนหน้า"]')
    back_button.click()
    time.sleep(3)  # Adjust sleep time if necessary

# Function to process data for a specific date
def process_date(driver, date, base_directory):
    print(f"Processing date: {date}")
    csv_file_path = os.path.join(base_directory, f"{date}.csv")

    # Check if the CSV file already exists to avoid reprocessing
    if os.path.exists(csv_file_path):
        print(f"CSV file for {date} already exists. Skipping...")
        return

    # Set the date in the date picker
    date_picker = driver.find_element(By.ID, 'date-picker-dialog-rid-daily')
    driver.execute_script("arguments[0].removeAttribute('readonly')", date_picker)
    date_picker.clear()
    date_picker.send_keys(date)
    time.sleep(3)  # Adjust sleep time if necessary

    # Extract HTML content
    html_content = driver.page_source
    headers, table_data = extract_table_data(html_content)

    # Write table data to CSV file
    write_table_to_csv(headers, table_data, csv_file_path)
    print(f"Data saved to {csv_file_path}")

# Main function to scrape data for the specified date range
def main(base_url, start_date, end_date, base_directory):
    driver_path = "D:/chromedriver_win64/chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode for no GUI
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(base_url)
    time.sleep(3)  # Adjust sleep time if necessary

    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    while current_date >= end_date:
        process_date(driver, current_date.strftime('%Y-%m-%d'), base_directory)
        go_back_one_day(driver)
        current_date -= timedelta(days=1)

    driver.quit()
# Base URL for the target website
base_url = "https://www.thaiwater.net/water/dam/large"  # Replace with the actual URL

# Date range for data extraction
start_date = "2024-06-07"    # NOTE: This date should be the most recent date for which data is available in Thai website
end_date = "1985-01-01"

# Base directory to save CSV files
base_directory = 'D:/Thai_website_scrape/'  # Replace with the actual path

# Ensure the base directory exists
os.makedirs(base_directory, exist_ok=True)

# Run the main function
main(base_url, start_date, end_date, base_directory)
```

## Conclusion
Web scraping is a valuable skill that can help you gather data from various sources. By following the steps outlined in this post, you should be able to scrape reservoir storage data and use it for your projects. Happy scraping!
