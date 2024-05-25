# ##static page 
# from selenium import webdriver
# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# import pandas as pd 

# option = Options()
# option.add_experimental_option("detach", True)
# driver = webdriver.Chrome(options=option)
# driver.get("https://www.youtube.com/watch?v=aqXkKgkyk2I")
# driver.maximize_window()

# # 1. scroll down page by pixel
# # driver.execute_script("window.scrollBy(0,1000)", "")
# time.sleep(10)
# # 2. scroll down page till the element is visible 
# # table = driver.find_element(By.XPATH,"//*[@id='page-wrapper']/div/div[4]/div[19]/detailed-team/div/div/div[2]")
# table = driver.find_element(By.XPATH,"//*[@id='sections']")
# driver.execute_script("arguments[0].scrollIntoView();", table)

# # driver.execute_script("window.scrollBy(0,500)")

# # time.sleep(10)
# # 3. scroll down page till the end
# # driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")

# # #dynamic

# # from selenium import webdriver
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.common.keys import Keys
# # from selenium.webdriver.common.action_chains import ActionChains
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# # import time

# # # Set up the webdriver
# # options = webdriver.ChromeOptions()
# # options.add_experimental_option("detach", True)
# # driver = webdriver.Chrome(options=options)

# # # Open the YouTube video page
# # driver.get("https://www.youtube.com/watch?v=XTjtPc0uiG8")
# # driver.maximize_window()
# # # Wait for the page to load (you might need to adjust the time)
# # driver.implicitly_wait(10)

# # # Simulate scrolling by sending PAGE_DOWN keys
# # # You can adjust the number of times you send the keys to control the amount of scrolling
# # for i in range(10): # Scroll down 5 times, you can adjust this number
# #     ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
# #     time.sleep(2)  # Adjust the sleep time based on your page loading speed

# # driver.find_element
# # # //*[@id="count"]/yt-formatted-string/span[1]

# # # Alternatively, you can use JavaScript to scroll
# # # For example, scroll to the bottom of the page
# # # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# # # Wait for the dynamically loaded content to appear
# # # You may need to adjust the locator based on your specific page structure
# # wait = WebDriverWait(driver, 10)
# # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "your_css_selector_here")))

# # # Perform further actions with the loaded content if needed

# # # Close the browser window
# # time.sleep(10)
# # driver.quit()



# from selenium import webdriver
# import time
# from selenium.webdriver.chrome.options import Options

# option = Options()
# option.add_experimental_option("detach", True)
# driver = webdriver.Chrome(options=option)
# driver.get("https://www.youtube.com/watch?v=xDXU6Jkzol4")
# driver.maximize_window()
# time.sleep(5)

# # Scroll down to load comments
# last_height = driver.execute_script("return document.documentElement.scrollHeight")
# while True:
#     # Scroll down
#     driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
#     # Wait for some time to let comments load
#     time.sleep(2)
#     # Calculate new scroll height
#     new_height = driver.execute_script("return document.documentElement.scrollHeight")
#     # Compare new scroll height with last scroll height
#     if new_height <= last_height:
#         # If scroll height hasn't increased or decreased, break the loop (no more comments to load)
#         break
#     last_height = new_height

# from selenium import webdriver
# import time
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By

# option = Options()
# option.add_experimental_option("detach", True)
# driver = webdriver.Chrome(options=option)
# driver.get("https://www.youtube.com/watch?v=xDXU6Jkzol4")
# driver.maximize_window()
# time.sleep(5)

# for i in range(2):
#     # Scroll down to load comments
#     last_height = driver.execute_script("return document.documentElement.scrollHeight")
#     scrolled_up_once = False  # Flag to track if already scrolled up once
#     # driver.find_element(By.XPATH,"//*[@id='description']").click()

#     while True:
#         # Scroll down
#         driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
#         # Wait for some time to let comments load
#         time.sleep(2)
#         # Calculate new scroll height
#         new_height = driver.execute_script("return document.documentElement.scrollHeight")
        
#         # Check if we need to scroll up once
#         if not scrolled_up_once:
#             # Scroll up once
#             driver.execute_script("window.scrollTo(0, 0);")
#             scrolled_up_once = True  # Update flag to indicate we've scrolled up once
#             # driver.find_element(By.XPATH,"//*[@id='description']").click()
#         else:
#             # Compare new scroll height with last scroll height
#             if new_height <= last_height:
#                 # If scroll height hasn't increased or decreased, break the loop (no more comments to load)
#                 break
     
#         last_height = new_height

# from selenium import webdriver
# import time
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By

# option = Options()
# option.add_experimental_option("detach", True)
# driver = webdriver.Chrome(options=option)
# driver.get("https://www.youtube.com/watch?v=xDXU6Jkzol4")
# driver.maximize_window()
# time.sleep(5)

# driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
# time.sleep(3)
# driver.execute_script("window.scrollTo(0, 0);")
# driver.implicitly_wait(2)
# driver.execute_script("window.scrollTo(0, 500);")
# driver.find_element(By.XPATH,"//*[@id='body']")

# from selenium import webdriver
# import time
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException

# option = Options()
# option.add_experimental_option("detach", True)
# driver = webdriver.Chrome(options=option)
# driver.get("https://www.youtube.com/watch?v=xDXU6Jkzol4")
# driver.maximize_window()
# time.sleep(5)



from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

option = Options()
option.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=option)
driver.get("https://www.youtube.com/watch?v=xDXU6Jkzol4")
# driver.get("https://www.youtube.com/watch?v=czrig0X-7OI")
driver.maximize_window()
time.sleep(5)

try:
    # Wait for the like button to be loaded and get the number of likes
    comments = driver.find_element(By.XPATH, '//*[@id="count"]/yt-formatted-string/span[1]').text
    print(f"Number of comments: {comments}")
    # Get the number of comments
    Like = driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[2]/div/div/ytd-menu-renderer/div[1]/segmented-like-dislike-button-view-model/yt-smartimation/div/div/like-button-view-model/toggle-button-view-model/button-view-model/button/div[2]').text
    print(f"Number of Like: {Like}")

except Exception as e:
    print(f"An error occurred: {e}")




# Scroll to the bottom of the page
driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
time.sleep(3)

# Scroll back to the top of the page
driver.execute_script("window.scrollTo(0, 0);")
time.sleep(3)

# Define the scroll amount
scroll_amount = 400

# Keep scrolling until the bottom of the page is reached
while True:
    # Get the current scroll position
    current_scroll_position = driver.execute_script("return window.pageYOffset;")
    
    # Scroll down by the defined amount
    driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
    
    # Wait for a short while for the content to load
    time.sleep(1)
    
    # Get the new scroll position
    new_scroll_position = driver.execute_script("return window.pageYOffset;")
    
    # If the scroll position hasn't changed, we've reached the bottom
    if new_scroll_position == current_scroll_position:
        print("Reached the bottom of the page. Stopping the scroll.")
        break

print("Loop Out")

# Locate and print the number of likes and comments


# N = scroll_number = driver.find_element(By.XPATH, "//*[@id='count']/yt-formatted-string/span[1]").text
# print(N)
# Clean up or add more interactions as needed
# driver.quit()  # Uncomment this line if you want to close the browser at the end
