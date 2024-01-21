from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd 

option = Options()
option.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=option)
driver.maximize_window()
driver.get("https://seleniumpractise.blogspot.com/2016/08/how-to-handle-calendar-in-selenium.html")
driver.implicitly_wait(1)

# # typ 1
driver.find_element(By.XPATH,"//input[@id='datepicker']").click()
driver.find_element(By.XPATH,"//a[text()=22]").click()

# #typ 2 
driver.find_element(By.XPATH,"//input[@id='datepicker']").click()
AllDate = driver.find_elements(By.XPATH,"//table[@class='ui-datepicker-calendar']//a")

for date in AllDate:
    if date.text == '22':
        date.click()
        break








