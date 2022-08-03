from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver=webdriver.Chrome()
driver.get("https://www.facebook.com/")
print("opened Facebook")

user_name="playsi17"
password="test"

element = driver.find_element_by_id("email")
element.send_keys(user_name)
print("email id enter")
time.sleep(1)
element = driver.find_element_by_id("pass")
element.send_keys(password)
print("password id enter")
time.sleep(1)
element.send_keys(Keys.RETURN)
element.close()
