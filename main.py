from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup


# Create dataframe and csv to store all scrapped information
df = pd.DataFrame({'post_title': [],
                   'post_url': [],
                   'account_username': [],
                   'account_rating': [],
                   'account_url': [],
                   'account_sales': [],
                   'account_local_store': []
                   })
df.to_csv('etsy.csv', index=False)

# User Input: Put the url in the line below
# User Input: Put the number of pages to be searched
etsy_url = str(input("Enter the etsy url to be scrapped:"))
number_of_pages = int(input("Enter the number of pages to be scrapped:"))

# Initiate Selenium
ser = Service("/Users/satyaprakashsahoo/Documents/Chrome Driver/chromedriver")
driver = webdriver.Chrome(service=ser)
# driver.get(etsy_url)
driver.get("https://www.etsy.com/ca/search?q=plants")
time.sleep(2)
cookie_accept = driver.find_element(By.XPATH, '//*[@id="gdpr-single-choice-overlay"]/div/div[2]/div[2]/button')
cookie_accept.click()
time.sleep(2)

for page in range(number_of_pages):
    # Find number of posts in the page
    post_elements = driver.find_elements(By.XPATH,'//*[@id="content"]/div/div[1]/div/div[4]/div[11]/div[2]/div[10]/div[1]/div/div/ul/li')
    number_post_elements = len(post_elements)

    # For each post in the page, collect the post name and the url and store in etsy.csv
    for n in range(1, number_post_elements+1):
        post_url = driver.find_element(By.XPATH, f'//*[@id="content"]/div/div[1]/div/div[4]/div[11]/div[2]/div[10]/div[1]/div/div/ul/li[{n}]/div/div/a')
        df.loc[len(df.index)] = [post_url.get_attribute("title"), post_url.get_attribute("href"), "", "", "", "", ""]

    df.to_csv('etsy.csv', index=False)

    # Click to go to next page and collect the posts and their url
    next_page_element = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div/div[4]/div[11]/div[2]/div[13]/div/div/div/div[2]/nav/ul/li[11]/a')
    driver.get(next_page_element.get_attribute("href"))
    time.sleep(2)
    page += 1

# Go through the collected urls and collect the account information using bs4
for count in range(len(df.index)):
    search_url = df["post_url"][count]
    response = requests.get(search_url).text
    soup = BeautifulSoup(response, "html.parser")
    account_name_element = soup.find(name="p", class_="wt-text-body-01 wt-mr-xs-1")
    account_name_string = account_name_element.getText()
    account_name = "".join([s for s in account_name_string.strip().splitlines(True) if s.strip()])
    df["account_username"][count] = account_name
    account_url = account_name_element.find(name="a").get("href")
    df["account_url"][count] = account_url
    sales_element = soup.find(name="div", class_="wt-display-inline-flex-xs wt-align-items-center wt-flex-wrap wt-mb-xs-2")
    sales_string = sales_element.getText()
    sales_string = "".join([s for s in sales_string.strip().splitlines(True) if s.strip()])
    sales = sales_string.splitlines()[0].split()[0]
    df["account_sales"][count] = sales
    rating = sales_string.splitlines()[-1].split()[0]
    df["account_rating"][count] = rating
    count += 1

df.to_csv('etsy.csv', index=False)
