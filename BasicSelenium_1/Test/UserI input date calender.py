from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd 

option = Options()
option.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=option)
driver.maximize_window()
driver.get("https://www.hyrtutorials.com/p/calendar-practice.html")
driver.implicitly_wait(1)

#user i/p date
day = input()
driver.find_element(By.XPATH,"//input[@id='first_date_picker']").click()
driver.find_element(By.XPATH,f"//a[text()='{day}']").click()

# day_xpath = f"//a[text()='{day}']"
