import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv
import os

# Set up Chrome WebDriver
driver = webdriver.Chrome()

# URL of the website to scrape from
website_url = 'https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment&cityName=Pune'

# Open the website
driver.get(website_url)

# Check if the CSV file exists
if not os.path.isfile('scraped_df.csv'):
 # If the CSV file does not exist, create it and write the headers
 f = open('scraped_df.csv', 'w', newline='', encoding='utf-8')
 writer = csv.writer(f)
 writer.writerow(['Society', 'Card Title','Carpet Area', 'Price', 'Price Per Sqft', 'Floor'])
else:
 # If the CSV file exists, open it in append mode
 f = open('scraped_df.csv', 'a', newline='', encoding='utf-8')
 writer = csv.writer(f)

# List to store already written data
written_data = []

# Continue scrolling until we have fetched 3000 properties
while len(written_data) < 3000:
 try:
   # Scroll down to bottom
   driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
 except Exception as e:
   print(f"An error occurred: {str(e)}")
   continue

 # Wait to load page
 time.sleep(5)

 # Get the updated page source
 page_source = driver.page_source

 # Parse the HTML content using BeautifulSoup
 soup = BeautifulSoup(page_source, 'html.parser')

 # Find all property cards
 property_cards = soup.find_all('div', class_='mb-srp__card__info mb-srp__card__info-withoutburger')
 price_amount_elements = soup.find_all('div', class_='mb-srp__card__estimate')

 # Process new property cards
 for card, price_amount_element in zip(property_cards[-60:], price_amount_elements[-60:]): # Process the last 10 property cards
   # Initialize variables
   carpet_area = None
   society = None
   card_title = None
   price = None
   price_per_sqft = None
   floor = None

   # Extract Carpet Area, Society details and Card title and floor
   carpet_area_element = card.find('div', {'class': 'mb-srp__card__summary__list--item', 'data-summary': 'carpet-area'})
   society_element = card.find('div', {'class': 'mb-srp__card__summary__list--item', 'data-summary': 'society'})
   card_title_element = card.find('h2', class_='mb-srp__card--title')
   floor_element = card.find('div', {'class': 'mb-srp__card__summary__list--item', 'data-summary': 'floor'})

   if carpet_area_element:
       carpet_area = carpet_area_element.find('div', class_='mb-srp__card__summary--value').text.strip()

   if society_element:
       society = society_element.find('div', class_='mb-srp__card__summary--value').text.strip()

   if card_title_element:
       card_title = card_title_element.text.strip()

   if floor_element:
      floor = floor_element.find('div', class_='mb-srp__card__summary--value').text.strip()

   # Extract Price amount details from 'mb-srp__card__estimate' class
   price_element = price_amount_element.find('div', class_='mb-srp__card__price--amount')
   price_per_sqft_element = price_amount_element.find('div', class_='mb-srp__card__price--size')

   if price_element:
       price = price_element.text.strip()

   if price_per_sqft_element:
       price_per_sqft = price_per_sqft_element.text.strip()

   # Extract data
   data = [society, card_title, carpet_area, price, price_per_sqft, floor]

   # Only write data to CSV if it hasn't been written before
   if data not in written_data:
       writer.writerow(data)
       written_data.append(data)

 # Delay between requests to avoid detection
 time.sleep(1)

# Close the CSV file
f.close()

# Close the browser session
driver.quit()

