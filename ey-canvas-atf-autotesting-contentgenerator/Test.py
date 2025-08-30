from selenium import webdriver
from time import sleep
from selenium.webdriver.edge.service import Service

driver = webdriver.Edge(service=Service(executable_path="C:\\SeleniumWebDrivers\\EdgeDriver\\msedgedriver.exe"))
driver.get("https://www.google.com")
sleep(10)
driver.quit()