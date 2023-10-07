import requests
from bs4 import BeautifulSoup
import os
import json

def fetch_retail_links(url):
    # Send a GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all <a> tags with 'href' attribute
    all_links = [a['href'] for a in soup.find_all('a', href=True)]

    # Filter links containing the string "/retail/"
    retail_links = ["https://www.apple.com" + link for link in all_links if '/retail/' in link and link!= "/retail/"]

    return retail_links

url = "https://www.apple.com/retail/storelist/"
links = fetch_retail_links(url)
for link in links: print(link)

home_directory = os.path.expanduser("~")
file_path = os.path.join(home_directory, "scraped_data.json")
with open(file_path, "w") as file: json.dump(links, file)





