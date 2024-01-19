from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import csv
from urllib3.exceptions import NewConnectionError, MaxRetryError
from time import sleep
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# use this command to install the dependencies
# pip install -r requirements.txt

# influx DB info
bucket = "Ack-Env"
org="SON"
token="f52IO-Tw8RiLTyc-lYUzCqpvBkybtNcvHCvrkJVvb7MREFUwAgPYueLKjfurQTXVI26i8qSn-2SuLwDY7xI3zg=="
url="http://localhost:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

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
        pl1 = f'{network_printer[0]} ({network_printer[3]}) '
        print(pl1, end=' ')
        try:
            driver.get(network_printer[3])
        except NewConnectionError:
            print(f'Error connecting to {network_printer[3]}')
            pstatus = "Error connecting"
            continue
        except MaxRetryError:
            print("max retry error")
            pstatus = "max retry error"
            continue
        except ConnectionRefusedError:
            print("Connection Refused Error")
            pstatus = "connection refused error"
            continue
        except:
            # assume any other error is host unreachable
            print("Host unreachable")
            pstatus = "host unreachable"
        sleep(1)
        try:
            driver.switch_to.frame('work')
            elem = driver.find_element(By.XPATH, "//dd[@class='word-wrap']")
            # next_elem = driver.find_element(By.XPATH, "following-sibling::element_selector")
            # if next_elem.text != 'Status OK':
            #    print(f'{elem.text} ({next_elem.text})')
            # else:
            pstatus = elem.text
            print(pstatus)
        except NoSuchElementException:
            print("can't find element")
            pstatus = "cant find element"
        except NoSuchFrameException:
            print("Cant find frame")
            pstatus = "cant find frame"
        p = influxdb_client.Point("printer_status").tag("Room", network_printer[0]).tag("IP_Addr", network_printer[3]).field("status", pstatus)
        write_api.write(bucket=bucket, org=org, record=p)
driver.close()
