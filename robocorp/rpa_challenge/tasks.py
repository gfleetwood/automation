from robocorp.tasks import task
from RPA.HTTP import HTTP
from RPA.Excel.Files import Files
from robocorp import browser
import time

browser.configure(
browser_engine = "chromium",
screenshot = "only-on-failure",
headless = False
)

page = browser.goto("https://rpachallenge.com")
#page.click("text=Start")
page.click('.waves-effect.col.s12.m12.l12.btn-large.uiColorButton')

@task
def rpa_form_challenge():
  download_file()
  data = read_data()
  fill_the_forms(data)
  collect_the_results()

def download_file():
  path = HTTP().download("https://rpachallenge.com/assets/downloadFiles/challenge.xlsx", "./output/download.xlsx", overwrite = True)
  print(f"Downloaded file to: {path}")

def read_data():
  lib = Files()
  workbook = lib.open_workbook("./output/download.xlsx")
  #worksheet = workbook.worksheet("Sheet1")
  worksheet = lib.read_worksheet_as_table(header = True)
  lib.close_workbook()

  #for row in worksheet: print(row)
  return(worksheet)
    
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
            #set_value_by_xpath(f'//input[@ng-reflect-name="{name}"]', person[key])
            page.fill('//input[@ng-reflect-name="{}"]'.format(name), str(person[key]))    
        page.click('input[value="Submit"]')
    
def collect_the_results():
    #browser.screenshot("css:div.congratulations", "./output/congratulations.png")
    page.screenshot(path = "./output/congratulations.png")
