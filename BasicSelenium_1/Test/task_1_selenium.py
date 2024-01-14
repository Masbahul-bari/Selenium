from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd 

option = Options()
option.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=option)
driver.maximize_window()
driver.get("https://oilprice.com/oil-price-charts/#prices")
driver.implicitly_wait(1)

# prices = driver.find_elements(By.XPATH,"//table[@data-id='1'] //tr")
prices = driver.find_elements(By.XPATH,"(//table//tbody[@class='row_holder'])[1]//tr")

symbol = []
Futures_and_Indexes = []
Last = []
Change = []
Per_Change = []
Last_Update = []

driver.implicitly_wait(1)
for price in prices:
    symbol.append(price.find_element(By.XPATH,"./td[1]").text)
    Futures_and_Indexes.append(price.find_element(By.XPATH,"./td[2]").text)
    Last.append(price.find_element(By.XPATH,"./td[3]").text)
    Change.append(price.find_element(By.XPATH,"./td[4]").text)
    Per_Change.append(price.find_element(By.XPATH,"./td[5]").text)
    Last_Update.append(price.find_element(By.XPATH,"./td[6]").text)

driver.implicitly_wait(1)
df = pd.DataFrame({'sylbol':symbol, 'Futures_and_Indexes':Futures_and_Indexes,'Last':Last, 'Change':Change, '%Change':Per_Change, 'Last_Update':Last_Update})
df.to_csv('oil_price.csv', index=False)
driver.quit()


# if table has any table header and that table we want to scraping then we have to start without table head
 
