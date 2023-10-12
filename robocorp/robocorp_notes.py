'''
rcc pull github.com/robocorp/example-google-image-search
rcc create my-robot
rcc run

rcc robot initialize -d my-robot
rcc robot libs -a numpy -p --conda conda.yaml
rcc environment setup --conda conda.yaml
rcc run --task "<name of tasks>"
rcc env update

rcc task testrun
rcc cloud push -r YOUR_ROBOT_ID_ON_ROBOCORP_CLOUD -w YOUR_WORKSPACE_ID
'''

from robocorp.tasks import task
from robocorp import browser, http, excel
from RPA.PDF import PDF
from robocorp.tasks import task
from robocorp import http
from RPA.Excel.Files import Files
from RPA.Tables import Tables
from RPA.Browser.Selenium import Selenium
from RPA.PDF import PDF

browser = Selenium()
    
@task
def robot_spare_bin_python():
    """Insert the sales data for the week and export it as a PDF"""
    browser.configure(
        slowmo=100,
    )
    open_the_intranet_website()
    log_in()
    download_excel_file()
    fill_form_with_excel_data()
    collect_results()
    export_as_pdf()
    log_out()

def log_in():
    """Fills in the login form and clicks the 'Log in' button"""
    page = browser.page()
    page.fill("#username", "maria")
    page.fill("#password", "thoushallnotpass")
    page.click("button:text('Log in')")

def fill_and_submit_sales_form():
    """Fills in the sales data and click the 'Submit' button"""
    page = browser.page()

    page.fill("#firstname", "John")
    page.fill("#lastname", "Smith")
    page.fill("#salesresult", "123")
    page.select_option("#salestarget", "10000")
    page.click("text=Submit")
    
def open_website(url):
    """Navigates to the given URL"""
    browser.open_available_browser(url)
    
def download_file(url, save_loc):
  path = http.download(url, save_loc, overwrite = True)
  print(f"Downloaded file to: {path}")
  
def read_data(path):

  lib = Files()
  workbook = lib.open_workbook(path)
  #worksheet = workbook.worksheet("Sheet1")
  worksheet = lib.read_worksheet_as_table(header = True)
  lib.close_workbook()

  #for row in worksheet: print(row)
  return(worksheet)
    
def clean_up():
    browser.close_all_browsers()

def open_the_intranet_website():
    """Navigates to the given URL"""
    browser.goto("https://robotsparebinindustries.com/")

def log_in():
    """Fills in the login form and clicks the 'Log in' button"""
    page = browser.page()
    page.fill("#username", "maria")
    page.fill("#password", "thoushallnotpass")
    page.click("button:text('Log in')")

def fill_and_submit_sales_form(sales_rep):
    """Fills in the sales data and click the 'Submit' button"""
    page = browser.page()

    page.fill("#firstname", sales_rep["First Name"])
    page.fill("#lastname", sales_rep["Last Name"])
    page.select_option("#salestarget", str(sales_rep["Sales Target"]))
    page.fill("#salesresult", str(sales_rep["Sales"]))
    page.click("text=Submit")

def download_excel_file():
    """Downloads excel file from the given URL"""
    http.download(url="https://robotsparebinindustries.com/SalesData.xlsx", overwrite=True)

def fill_form_with_excel_data():
    """Read data from excel and fill in the sales form"""
    excel = Files()
    excel.open_workbook("SalesData.xlsx")
    worksheet = excel.read_worksheet_as_table("data", header=True)
    excel.close_workbook()

    for row in worksheet:
        fill_and_submit_sales_form(row)

def collect_results():
    """Take a screenshot of the page"""
    page = browser.page()
    page.screenshot(path="output/sales_summary.png")

def export_as_pdf():
    """Export the data to a pdf file"""
    page = browser.page()
    sales_results_html = page.locator("#sales-results").inner_html()

    pdf = PDF()
    pdf.html_to_pdf(sales_results_html, "output/sales_results.pdf")    

def log_out():
    """Presses the 'Log out' button"""
    page = browser.page()  
    page.click("text=Log out")
    
def download_file():
  path = http.download("https://rpachallenge.com/assets/downloadFiles/challenge.xlsx", "/home/ray/download.xlsx", overwrite = True)
  print(f"Downloaded file to: {path}")

def read_data():
  lib = Files()
  workbook = lib.open_workbook("/home/ray/download.xlsx")
  #worksheet = workbook.worksheet("Sheet1")
  worksheet = lib.read_worksheet_as_table(header = True)
  lib.close_workbook()

  #for row in worksheet: print(row)
  return(worksheet)
    
def open_browser():
    """Navigates to the given URL"""
    browser.open_available_browser("https://rpachallenge.com")
    browser.click_button("Start")

def fill_the_forms(data):

    def set_value_by_xpath(xpath, value):
        script = f"document.evaluate('{xpath}',document.body,null,9,null).singleNodeValue.value='{value}';"
        return browser.execute_javascript(script)
    
    names_and_keys = {
        "labelFirstName": "First Name",
        "labelLastName": "Last Name",
        "labelCompanyName": "Company Name",
        "labelRole": "Role in Company",
        "labelAddress": "Address",
        "labelEmail": "Email",
        "labelPhone": "Phone Number",
    }
    
    for person in data:
        for name, key in names_and_keys.items():
            set_value_by_xpath(f'//input[@ng-reflect-name="{name}"]', person[key])
            
    browser.click_button("Submit")
