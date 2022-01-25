from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

driver = webdriver.Chrome()
driver.get("http://10.124.132.72/")
sleep(5)
driver.switch_to.frame(0)
driver.find_element(By.XPATH, "//div[@id='rightAreaBox']/div/ul/li[4]/a/span").click()
sleep(3)
driver.switch_to.default_content()
driver.find_element(By.XPATH, "//input[@name='userid_work']").clear()
driver.find_element(By.XPATH, "//input[@name='userid_work']").send_keys("admin")
driver.find_element(By.XPATH, "//input[@value='Login']").click()
driver.switch_to.frame(1)
sleep(3)
my_element = driver.find_element(By.XPATH, "//a[contains(.,'Address Book')]")
javas = my_element.get_attribute('href')
driver.execute_script(javas)
driver.find_element(By.XPATH, "//div[@id='parentFrame']/div[4]/ul/li[3]/a/nobr").click()
driver.find_element(By.XPATH, "//input[@value='Backup']").click()
sleep(30)
driver.close()
