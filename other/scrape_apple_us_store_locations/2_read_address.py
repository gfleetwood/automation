import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import json

def get_address_and_phone(index, url):
    # Fetch the content from the given URL
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful

    # Parse the fetched content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    try:
      # Find the required element using its class name
        element = soup.find('div', class_='store-address-block').find('address')

      # Check if the element was found and return its text, else return None
        if element:
            print(index, url)
            return ' '.join(element.stripped_strings)  # Join all the strings inside the element, removing extra whitespaces
        else:
            return None
    except:
        print("no address")

url = "https://www.apple.com/retail/cumberlandmall/"
with open("scraped_data.json", "r") as file: urls = json.load(file)
payload = [{"store_link": url, "address": get_address_and_phone(index, url)} for index, url in enumerate(urls)]

df = pd.DataFrame(payload)
home_directory = os.path.expanduser("~")
file_path = os.path.join(home_directory, "apple_us_store_address.csv")
df.to_csv(file_path, index = False)
