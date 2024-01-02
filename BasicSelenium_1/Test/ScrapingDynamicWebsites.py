from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd 

option = Options()
option.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=option)
driver.get("https://www.adamchoi.co.uk/overs/detailed")
driver.maximize_window()

time.sleep(2)
driver.find_element(By.XPATH, "//label[@analytics-event='All matches']").click()
matches = driver.find_elements(By.XPATH, "//tr")

date = []
home_team = []
score = []
away_team =[]

for match in matches:
    # print(match.text)
    date.append(match.find_element(By.XPATH, "./td[1]").text)
    home_team.append(match.find_element(By.XPATH, "./td[2]").text)
    score.append((match.find_element(By.XPATH, "./td[3]").text).replace('-','v'))
    away_team.append(match.find_element(By.XPATH, "./td[4]").text)
    print(score)
    match.find_element(By.XPATH, "//tr/td[2]")
    
df = pd.DataFrame({'date':date,'home_team':home_team, 'score':score, 'away_team':away_team})
df.to_csv('football_1.csv', index=False)
driver.quit()