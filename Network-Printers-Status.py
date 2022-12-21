from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException
from selenium.webdriver.common.by import By
import csv
from urllib3.exceptions import NewConnectionError, MaxRetryError
from time import sleep
from selenium.webdriver import ChromeOptions

# Setup chrome webdriver
options = ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

# load from csv list of printers
with open('NetworkPrinters.csv', newline='') as f:
    reader = csv.reader(f)
    network_printers = list(reader)

# retrieve and print printer status for all printers
for network_printer in network_printers[1:]:
    if len(network_printer[3]) != 0:
        print(f'Ackerson {network_printer[0]} ({network_printer[3]}) ', end=' ')
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
            # assume any other error is host unreachable
            print("Host unreachable")
        sleep(1)
        try:
            driver.switch_to.frame('work')
            elem = driver.find_element(By.XPATH, "//dd[@class='word-wrap']")
            print(elem.text)
        except NoSuchElementException:
            print("can't find element")
        except NoSuchFrameException:
            print("Cant find frame")
driver.close()
