# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 22:13:01 2017

@author: binoy
"""

from bs4 import BeautifulSoup
import json
import pandas as pd
import nltk
import time

from selenium import webdriver
from selenium.webdriver.firefox.service import Service  # ✅ NEW import for Selenium 4+
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Download NLTK tokenizer
nltk.download('punkt')

# Load URLs from url.json
with open('url.json', 'r') as f:
    url = json.load(f)

data = {}
i = 1
jd_df = pd.DataFrame()

# ✅ Set up GeckoDriver correctly for Selenium 4+
service = Service(r'C:\Tools\geckodriver-v0.16.0-win64\geckodriver.exe')
driver = webdriver.Firefox(service=service)

# Loop through each job URL
for u in url:
    driver.wait = WebDriverWait(driver, 5)
    driver.maximize_window()
    driver.get(u)

    soup = BeautifulSoup(driver.page_source, "lxml")

    header = soup.find("div", {"class": "header cell info"})
    position = header.find('h2').get_text()
    company = header.find("span", {"class": "ib"}).get_text()
    location = header.find("span", {"class": "subtle ib"}).get_text()[2:]
    jd = soup.find("div", {"class": "jobDescriptionContent desc"}).get_text()

    info = soup.find_all("div", {"class": "infoEntity"})
    try:
        headquaters = info[1].find("span", {"class": "value"}).get_text().strip().replace('\\u', '')
        employees = info[2].find("span", {"class": "value"}).get_text().strip().replace('\\u', '')
        founded = info[3].find("span", {"class": "value"}).get_text().strip().replace('\\u', '')
        industry = info[5].find("span", {"class": "value"}).get_text().strip().replace('\\u', '')
    except:
        headquaters = None
        employees = None
        founded = None
        industry = None

    data[i] = {
        'url': u,
        'company': company,
        'position': position,
        'location': location,
        'headquaters': headquaters,
        'employees': employees,
        'founded': founded,
        'industry': industry,
        'Job Description': jd
    }
    print(i)
    i += 1

# Quit driver
driver.quit()

# Convert data to DataFrame and export to CSV
jd_df = pd.DataFrame(data).transpose()
jd_df = jd_df[['company', 'position', 'url', 'location', 'headquaters', 'employees', 'founded', 'industry', 'Job Description']]
jd_df.to_csv('data.csv', encoding="utf-8", index=False)
