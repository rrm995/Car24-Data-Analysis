#!/usr/bin/env python
# coding: utf-8

# In[3]:


pip install requests --q


# In[6]:


import requests


# In[8]:


pip install BeautifulSoup4


# In[8]:


import requests as re
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from selenium import webdriver                  
from selenium.webdriver.common.by import By


# In[9]:


# Define an empty list as a constant to store all car data
ALL_CAR_DATA = []


# In[10]:


# Function to initialize the WebDriver and perform scrolling
def initialize_driver(url):
    driver = webdriver.Chrome()
    driver.get(url)
    SCROLL_PAUSE_DURATION = 3
    previous_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_DURATION)
        current_height = driver.execute_script("return document.body.scrollHeight")
        if current_height == previous_height:
            break
        previous_height = current_height

    return driver


# In[11]:


# Function to extract links from the webpage
def extract_links(driver):
    link_elements = driver.find_elements(By.CSS_SELECTOR, 'a.IIJDn')
    links = [element.get_attribute("href") for element in link_elements if element.get_attribute("href")]
    return links


# In[12]:


# Function to extract data from each car listing
def extract_car_data(link):
    response = re.get(link)
    soup = bs(response.content, 'html.parser')

    car_details = {}  # Initialize an empty dictionary to store car details

    try:
        # Extract car details
        header_text = soup.find('h1', class_='_2Ximl').text.split()
        car_details['Car_Model'] = header_text[0]
        car_details['Brand'] = header_text[1]
        car_details['Car_Name'] = header_text[2]
        car_details['Car_Variant'] = " ".join(header_text[3:])

        # Extract list details
        list_items = [li.get_text() for li in soup.find('ul', class_='_2JSmz').find_all('li')]
        car_details['Car_Transmission'] = list_items[3]
        car_details['KM_Driven'] = list_items[0]
        car_details['Owner_Type'] = list_items[1]
        car_details['Fuel_Type'] = list_items[2]

        # Extract additional details
        more_details = soup.find_all('strong', class_='_3gHeV')
        if len(more_details) > 2:
            car_details['Registration_ID'] = more_details[2].get_text()
        else:
            car_details['Registration_ID'] = ""

        car_details['Monthly_EMI'] = soup.find('strong', class_='_3i9_p _3d4o3').text.split('/')[0]
        car_details['Car_Price'] = soup.find_all('strong', class_='_3i9_p')[1].text
        car_details['Downpayment_Amount'] = soup.find('label', class_='F6S7B').text.replace(" down payment", "").strip()
        car_details['Location'] = soup.find('li', class_='_1Rvdw').find('strong').text

    except Exception as e:
        print(f"Error processing {link}: {e}")

    return car_details


# In[13]:


# Function to process a URL
def process_url(url, max_links=500):
    driver = initialize_driver(url)
    links = extract_links(driver)
    driver.quit()

    # Extract data from each link and append it to the constant list
    for link in links[:max_links]:
        car_data = extract_car_data(link)
        if car_data:
            ALL_CAR_DATA.append(car_data)


# In[14]:


# Main function to run the extraction process for both URLs and save to CSV
def main():
    urls = [
        "https://www.cars24.com/buy-used-cars-new-delhi/",
        "https://www.cars24.com/buy-used-car/?sort=bestmatch&serveWarrantyCount=true&storeCityId=2378"
    ]

    for url in urls:
        process_url(url)

    # Create a DataFrame and save it to a CSV file
    df = pd.DataFrame(ALL_CAR_DATA)
    df.to_csv('car_data.csv', index=False)
    print("Data has been written to 'car_data.csv'")


# In[15]:


if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:




