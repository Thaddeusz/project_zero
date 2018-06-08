from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Firefox()
browser.get("http://bonuszbrigad.hu/bonuszkerek")
time.sleep(30)
browser.find_element_by_xpath("//*[@id=startButton]").click()
