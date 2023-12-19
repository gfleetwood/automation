from playwright.sync_api import Playwright, sync_playwright, expect
import requests
from bs4 import BeautifulSoup
import string
import pandas as pd

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless = True)
    context = browser.new_context()
    page = context.new_page()
    data = []
    
    for i in range(1):
        page.goto("https://www.larvf.com/,domaine-de-l-a,10476,403953.asp", timeout = 60000)
        content = page.content()
        payload = make_soup(content)
        #data.append(payload)

    # ---------------------
    context.close()
    browser.close()

def make_soup(content):

    payload = {}
    soup = BeautifulSoup(content, 'html.parser')
    
    meta_elements = soup.find_all('div', class_ = 'Article-metaElement')

    for element in meta_elements:
        label = element.find('label', class_='Article-metaLabel').get_text(strip=True)
        value = element.find('span', class_='Article-metaValue').get_text(strip=True)
        payload[label] = value
        
    contact_div = soup.find('div', class_='ContactInformationsDataList')

    # Initialize an empty string to hold the text
    contact_text = ""

    # Iterate over each element in the div
    for content in contact_div:
        if content.name == 'span':
            contact_text += content.get_text(strip=True) + " "
        elif content.name == 'br':
            contact_text += '\n'
        else:
            contact_text += content if content else ""

    payload['Address'] = contact_text.strip()
    
    email_span = soup.find('div', class_='ContactInformationsDataListItem').find('span', class_='ContactInformationsDataListItemValue')
    email_text = email_span.get_text(strip=True)
    payload['Email'] = email_text        
        
    print(payload)
    return(payload)
    
df = pd.read_csv("wineries.csv").to_dict(orient = 'records')[:5]

with sync_playwright() as playwright:
    run(playwright)

