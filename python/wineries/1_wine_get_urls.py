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
    
    for url in urls:
        page.goto(url, timeout = 60000)
        #page.get_by_label("Agree and close: Agree to our data processing and close").click()
        content = page.content()
        payload = make_soup(content)
        data.append(payload)
        
    data_flattened = sum(data, [])
    pd.DataFrame(data_flattened).to_csv("~/wineries.csv", index = False)   
    context.close()
    browser.close()

def make_soup(content):
    soup = BeautifulSoup(content, 'html.parser')
    li_elements = soup.find_all('li', class_ = 'DomainList-domain')
    payload = []
    
    for li in li_elements:
        a_tag = li.find('a')  
        href = a_tag.get('href') if a_tag else None
        text = li.get_text(strip = True)
        payload.append({"name": text, "url": href})
        
    return(payload)
    
urls = ["https://www.larvf.com/domaines/alpha/{}".format(letter) for letter in string.ascii_lowercase]

with sync_playwright() as playwright:
    run(playwright)

