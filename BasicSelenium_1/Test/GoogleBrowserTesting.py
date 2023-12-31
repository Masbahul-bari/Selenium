import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

option = Options()
option.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=option)
driver.get("http://www.google.com")
# driver.maximize_window()

driver.find_element(By.NAME, "q").send_keys("selenium") #\ue007 ---> this for enter
driver.implicitly_wait(1)
driver.find_element(By.NAME, "btnK").click()
# driver.find_element(By.XPATH, "//div[@class='FPdoLc lJ9FBc']//input[@name='btnK']").click()  --> using xpath
# driver.execute_script("window.scrollTo(0, Y)")
# driver.find_element(By.NAME, "btnK").click()

# time.sleep(3)
# driver.close()

# import time
# time.sleep(5)
# button = driver.find_element(by=By.NAME,value="Google Search")
# button.click
# driver.findElement(By.NAME("q")).send_keys
# driver.find_element(By.NAME("btnK")).