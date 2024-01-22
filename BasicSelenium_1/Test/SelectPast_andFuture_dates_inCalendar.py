from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd 
from datetime import datetime
import time

# Function to parse and compare dates
def compare_dates(given_date):
    today = datetime.now()
    given_date_obj = datetime.strptime(given_date, "%d/%m/%Y")
    return given_date_obj < today, given_date_obj

# Initialize WebDriver
option = Options()
option.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=option)
driver.maximize_window()
driver.get("https://seleniumpractise.blogspot.com/2016/08/how-to-handle-calendar-in-selenium.html")
driver.implicitly_wait(3)

# Input date
input_date = "23/01/3024"  # Format: DD/MM/YYYY
is_past, given_date_obj = compare_dates(input_date)

# Open calendar
driver.find_element(By.XPATH, "//input[@id='datepicker']").click()
driver.implicitly_wait(2)

# Navigate calendar
while True:
    current_month = driver.find_element(By.XPATH, "//span[@class='ui-datepicker-month']").text
    current_year = driver.find_element(By.XPATH, "//span[@class='ui-datepicker-year']").text

    if (given_date_obj.year == int(current_year) and 
        datetime.strptime(current_month, "%B").month == given_date_obj.month):
        break
    elif is_past:
        driver.find_element(By.XPATH, "//span[@class='ui-icon ui-icon-circle-triangle-w']").click()
    else:
        driver.find_element(By.XPATH, "//span[text()='Next']").click()
    # time.sleep(1)

# Select day
driver.find_element(By.XPATH, f"//a[text()='{given_date_obj.day}']").click()
