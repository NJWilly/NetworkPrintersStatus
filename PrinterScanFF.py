from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import csv
from urllib3.exceptions import NewConnectionError, MaxRetryError
from time import sleep

# use this command to install the dependencies
# pip install -r requirements.txt

# Specify the path to the GeckoDriver executable
driver_path = 'c:/users/wnoel'

# Set Firefox to run in headless mode
options = Options()
options.headless = True
options.add_argument("-headless")

# Create a Firefox driver
driver = webdriver.Firefox(options=options)
driver.implicitly_wait(10)



# # Setup chrome webdriver
# options = ChromeOptions()
# options.add_argument("--headless")
# options.add_argument("--disable-dev-shm-usage")
# driver = webdriver.Chrome(options=options)

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
            # next_elem = driver.find_element(By.XPATH, "following-sibling::element_selector")
            # if next_elem.text != 'Status OK':
            #    print(f'{elem.text} ({next_elem.text})')
            # else:
            print(elem.text)
        except NoSuchElementException:
            print("can't find element")
        except NoSuchFrameException:
            print("Cant find frame")
driver.close()
