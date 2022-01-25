from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException
from selenium.webdriver.common.by import By
import csv
from urllib3.exceptions import NewConnectionError, MaxRetryError
from time import sleep

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
            # assume any other error is host unreachable
            print("Host unreachable")
        # driver.implicitly_wait(30)
        sleep(10)
        frames = [0, 1, 2, 3, 4]
        element = "//dd[@class='word-wrap']"
        for frame in frames:
            try:
                driver.switch_to.frame(frame)
                if driver.find_element(By.XPATH, element).is_displayed():
                    print("found element " + element + " in frame " + str(frame))
                    driver.switch_to.parent_frame()
            except:
                driver.switch_to.parent_frame()
                print(" element: " + element + " was not found in frame: " + str(frame))


# driver.quit()
driver.close()
