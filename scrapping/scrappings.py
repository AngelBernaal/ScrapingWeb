from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


website_url = "https://www.amazon.com.mx/s?k=nintendo+switch+2&crid=YJ8ITXWKWRV6&sprefix=nintendo+switch%2Caps%2C356&ref=nb_sb_ss_ts-doa-p_1_15"

driver =  webdriver.Safari()
driver.get(website_url)
time.sleep(5)

content = driver.page_source
driver.quit()

soup = BeautifulSoup(content, "html.parser")

data = []

products = soup.find_all("div", {"data-component-type": "s-search-result"})
for product in products:
    title = product.h2.text
    try:
        rating = product.find("span", class_="a-icon-alt").text
    except AttributeError:
        rating = "No rating"
    try:
        price_whole = product.find("span", class_="a-price-whole").text
        price_fraction = product.find("span", class_="a-price-fraction").text
        price = f"${price_whole}{price_fraction}"
    except AttributeError:
        price = "No price"
    print(f"Title: {title}")
    print(f"Rating: {rating}")
    print(f"Price: {price}")
    print("-" * 80)
    data.append([title, rating, price])
    
df = pd.DataFrame(data, columns=["Title", "Rating", "Price"])
df['price'] = df['Price'].str.replace('$', '').str.replace(',', '').astype(float, errors='ignore')
df['rating'] = df['Rating'].str.extract(r'(\d+\.?\d*)').astype(float, errors='ignore')
df.fillna(0, inplace=True)
print(df)
df.to_csv("nintendo_switch_products.csv", index=False)
