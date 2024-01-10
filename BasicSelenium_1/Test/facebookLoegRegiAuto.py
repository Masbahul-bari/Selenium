from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
import time


option = Options()
option.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=option)
driver.implicitly_wait(1)

# driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.facebook.com/")

driver.find_element(By.XPATH, "//a[@rel='async']").click()
driver.implicitly_wait(3)

driver.find_element(By.XPATH, "//*[@name='firstname']").send_keys("Abul")
driver.find_element(By.XPATH, "//*[@name='lastname']").send_keys("Khan")
driver.find_element(By.XPATH, "//*[@name='reg_email__']").send_keys("ab@gmail.com")
driver.implicitly_wait(3)
driver.find_element(By.XPATH, "//*[@name='reg_email_confirmation__']").send_keys("ab@gmail.com")
driver.find_element(By.XPATH, "//*[@name='reg_passwd__']").send_keys("abul123")

Select(driver.find_element(By.XPATH, "//select[@id='day']")).select_by_visible_text("13")
Select(driver.find_element(By.XPATH, "//select[@id='month']")).select_by_visible_text("Apr")
Select(driver.find_element(By.XPATH, "//select[@id='year']")).select_by_visible_text("2000")


driver.find_element(By.XPATH, "//*[text()='Female']").click()
driver.find_element(By.XPATH, "//button[@name='websubmit']").click()
# //button[@name='websubmit']


# Number = input(int(print("Enter a number between 1 to 3")))
# if Number==1:
    # driver.find_element(By.XPATH, "//*[text()='Female']").click()
# if Number==2:
    # driver.find_element(By.XPATH, "//*[text()='Male']").click()
# if Number==3:
    # driver.find_element(By.XPATH, "//*[text()='Custom']").click()
    # x = Select(driver.find_element(By.XPATH, "//*[@name='preferred_pronoun']"))
    # Number1 = input(int(print("if She: Wish her a happy birthday! enter 1, if  He: Wish him a happy birthday! enter 2, or if They: Wish them a happy birthday! enter 3")))
    # if Number1==1:
    #     driver.find_element(By.XPATH, "//*[text()='She: "Wish her a happy birthday!"']").click()
    # if Number1==2:
    #     driver.find_element(By.XPATH, "//*[text()='Male']").click()
    # if Number1==3:
    #     driver.find_element(By.XPATH, "//*[text()='Custom']").click()
    
