from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver=webdriver.Chrome()
driver.get("https://twitter.com/login")
print("opened CARA mail")

adress_mail="test246545"

element = driver.find_element_by_css_selector("input[type=text]")
print(element)
element.send_keys(adress_mail)
