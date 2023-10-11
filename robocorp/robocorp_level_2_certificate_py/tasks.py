from robocorp.tasks import task
from robocorp import http
from robocorp import browser
from RPA.Tables import Tables
from RPA.HTTP import HTTP
from RPA.PDF import PDF
from RPA.Archive import Archive
import time
import pandas as pd
from sys import exit
from bs4 import BeautifulSoup

browser.configure(
browser_engine = "chromium",
screenshot = "only-on-failure",
headless = True
)

# dummy value for page before initialization
page = 0
pdf = PDF()

@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    
    orders = get_orders()
    open_robot_order_website()
    close_annoying_modal()
    fill_the_form(orders)
    archive_receipts()
   
def get_orders():
  path = HTTP().download("https://robotsparebinindustries.com/orders.csv", "output/orders.csv", overwrite = True)
  print(f"Downloaded file to: {path}")
  
  tables = Tables()
  table = tables.read_table_from_csv("output/orders.csv")
  
  # each row is a dictionary of col_name:value
  #for row in table: print(row)
  
  return(table)
  
def open_robot_order_website():
    """Navigates to the given URL"""
    global page
    page = browser.goto("https://robotsparebinindustries.com/#/")
    page.click("a[href='#/robot-order']")
    
def close_annoying_modal():
  global page  
  page.click('.btn.btn-danger')

def fill_the_form(orders):
    global page

    def read_html_table():
        page.click('text="Show model info"')
        html_table = page.query_selector("#model-info").inner_html()
        
        soup = BeautifulSoup(html_table, 'html.parser')
        header_columns = [th.text for th in soup.select('thead th')]
        data_rows = soup.select('tbody tr')
        
        # list of rows which are dictionaries of col_name:value
        data = [{header_columns[i]: cell.text for i, cell in enumerate(row.find_all('td'))} for row in data_rows]
            
        return(data)
            
    def process_row(data, row):
        page.select_option("#head", str(row["Head"]))
        page.click('input[type="radio"][value="{}"]'.format(row["Body"]))
        page.fill('//input[@type="number"]', row["Legs"])
        page.fill('#address', row["Address"])
        page.click('#preview')
        
        while True:
            page.click('#order')        
            element = page.query_selector('#receipt')
        
            if element:
                print("order submitted")
                break
            else:
                print("order not submitted, trying again")
                
        screenshot_path = screenshot_robot(row["Order number"]) 
        pdf_order_path = store_receipt_as_pdf(row["Order number"])
        embed_screenshot_to_receipt(pdf_order_path, pdf)
        page.click('#order-another')
        close_annoying_modal()
        
    data = read_html_table()
    for row in orders: process_row(data, row)

def screenshot_robot(order_number):
    global page
    page.screenshot(path = "./output/receipts/receipt_order_{}.png".format(order_number))
    return("./output/receipts/receipt_order_{}.png".format(order_number))
    
def store_receipt_as_pdf(order_number):
    
    pdf.add_files_to_pdf(
        files = ["./output/receipts/receipt_order_{}.png".format(order_number)],
        target_document = "./output/receipts/receipt_order_{}.pdf".format(order_number)
    )
    
    return("./output/receipts/receipt_order_{}.pdf".format(order_number))
    
def embed_screenshot_to_receipt(screenshot, pdf_file):
    pass
    
def archive_receipts():
    lib = Archive()
    lib.archive_folder_with_zip('./output/receipts/', './output/archive.zip', include = '*.pdf')
