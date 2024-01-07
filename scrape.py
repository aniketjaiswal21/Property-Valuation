import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Automatically install and set up Chromedriver
chromedriver_autoinstaller.install()

# Set Chrome options to disable notifications
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)

#url of the website to scrape from
website_url = 'https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment&cityName=Pune'

# use Chrome WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Open the website
driver.get(website_url)

# Wait for the element to be present
# try:
#     element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, '//*[@id="propertiesAction69977885"]/div[1]/div[5]/div[2]'))
#     )
#     print('Society: ',element.text)  # Print the text content of the element

#      # Fetching the second XPath information
#     element2 = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, '//*[@id="cardid69977885"]/div/div[2]/div[1]/div[2]'))
#     )
#     print("Price per square feet:", element2.text)

# except Exception as e:
#     print(f"Error: {e}")

try:
    # Find all elements representing individual property containers
    property_containers = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'm-srp-card__container'))
    )

    for container in property_containers[:20]:  # Loop through the first 20 property containers
        # Extract Carpet Area and Society
        carpet_area_element = container.find_element(By.XPATH, './/div[@data-summary="carpet-area"]/div[@class="mb-srp__card__summary--value"]')
        society_element = container.find_element(By.XPATH, './/div[@data-summary="society"]/div[@class="mb-srp__card__summary--value"]')
        carpet_area = carpet_area_element.text
        society = society_element.text

        # Extract Price and Price per sqft
        price_element = container.find_element(By.XPATH, './/div[@class="mb-srp__card__price--amount"]')
        price_per_sqft_element = container.find_element(By.XPATH, './/div[@class="mb-srp__card__price--size"]')
        price = price_element.text
        price_per_sqft = price_per_sqft_element.text

        # Print or process the extracted information
        print(f"Carpet Area: {carpet_area}")
        print(f"Society: {society}")
        print(f"Price: {price}")
        print(f"Price per sqft: {price_per_sqft}")
        print("------------")  # Separator between properties

except Exception as e:
    print(f"Error: {e}")
