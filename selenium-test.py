from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException
from selenium.webdriver.common.by import By
import csv

from urllib3.exceptions import NewConnectionError, MaxRetryError


driver = webdriver.Chrome()

with open('NetworkPrinters.csv', newline='') as f:
    reader = csv.reader(f)
    network_printers = list(reader)

for network_printer in network_printers[1:]:
    if len(network_printer[3]) != 0:
        print(network_printer[3], end=' ')
        try:
            driver.get(network_printer[3])
        except NewConnectionError:
            print(f'Error connecting to {network_printer[3]}')
            continue
        except MaxRetryError:
            print("max retry error")
            continue
        except ConnectionRefusedError:
            print("Connection Refused Error")
            continue
        except:
            print("other Error")

        try:
            driver.switch_to.frame('work')
            driver.implicitly_wait(3)
            elem = driver.find_element(By.XPATH, "//dd[@class='word-wrap']")
            # print("success")
            print(elem.text)
        except NoSuchElementException:
            print("can't find element")
        except NoSuchFrameException:
            pass
driver.quit()
# driver.close()
