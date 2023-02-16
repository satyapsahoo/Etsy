import pandas as pd
import requests
from bs4 import BeautifulSoup

df = pd.read_csv("etsy.csv")
# print(df["post_title"][0], df["post_url"][0])
# search_url = df["post_url"][2]
local_search_url = "https://www.etsy.com/listing/1323531601/1-rhizome-oxalis-black-rhizome?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=plants&ref=sr_gallery-1-2&edd=1&pop=1&organic_search_click=1"
normal_search_url = "https://www.etsy.com/listing/1323241714/50-monstera-deliciosa-albo-variegated?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=plants&ref=sr_gallery-1-1&pro=1&frs=1&edd=1&organic_search_click=1"
star_search_url = "https://www.etsy.com/listing/1333649210/just-one-more-plant-shirt-unisex-funny?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=plants&ref=sc_gallery-1-2&pro=1&edd=1&sts=1&plkey=ba7632347144d18b606d01b19ae1d382b05a2933%3A1333649210"
response = requests.get(local_search_url).text
soup = BeautifulSoup(response, "html.parser")
account_name_element = soup.find(name="p", class_="wt-text-body-01 wt-mr-xs-1")
account_name_string = account_name_element.getText()
account_name = "".join([s for s in account_name_string.strip().splitlines(True) if s.strip()])
print(account_name)
account_url = account_name_element.find(name="a").get("href")
print(account_url)
sales_element = soup.find(name="div", class_="wt-display-inline-flex-xs wt-align-items-center wt-flex-wrap wt-mb-xs-2")
sales_string = sales_element.find(name="span", class_="wt-text-caption").getText()
sales_string = "".join([s for s in sales_string.strip().splitlines(True) if s.strip()])
sales = sales_string.splitlines()[0].split()[0]
print("Sales is:", sales)
rating_element = soup.find(name="span", class_="wt-display-inline-block wt-mr-xs-1")
rating = rating_element.find(name="input").get("value")
print(rating)

c_response = requests.get(account_url).text
c_soup = BeautifulSoup(c_response, "html.parser")
# c_element = soup.find(name="div", class_="shop-info")
c_element = soup.find(name="div", class_="shop-location wt-display-flex-xs wt-mb-xs-1 center-md-down")
print(c_element)
# location = c_element.getText()
# print(location)


