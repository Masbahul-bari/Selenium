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


driver.find_element(By.XPATH,"//input[@id='datepicker']").click() # select the box
driver.implicitly_wait(2)
driver.find_element(By.XPATH,"//div[@id='ui-datepicker-div']") # select the calender

driver.implicitly_wait(1)
current_month = driver.find_element(By.XPATH,"//span[@class='ui-datepicker-month']").text
current_year = driver.find_element(By.XPATH,"//span[@class='ui-datepicker-year']").text
driver.implicitly_wait(1)

while not(current_month.__eq__("May") and current_year.__eq__("2080")):
    driver.find_element(By.XPATH,"//span[text()='Next']").click() #Prev button
    current_month = driver.find_element(By.XPATH,"//span[@class='ui-datepicker-month']").text
    current_year = driver.find_element(By.XPATH,"//span[@class='ui-datepicker-year']").text

# day = input()
# driver.find_element(By.XPATH,f"//a[text()='{day}']").click()
    # abov line of code are use for usre input 
driver.find_element(By.XPATH,"//a[text()=17]").click()




