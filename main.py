# This script should display status summary of network printers listed in a CSV file

import csv
import requests
from bs4 import BeautifulSoup

headers = {"User-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/97.0.4692.71 Safari/537.36'}

if __name__ == '__main__':
    with open('NetworkPrinters.csv', newline='') as f:
        reader = csv.reader(f)
        network_printers = list(reader)

    for network_printer in network_printers[1:]:
        if len(network_printer[3]) != 0:
            try:
                page = requests.get(network_printer[3] + 'web/guest/en/websys/webArch/mainFrame.cgi', headers=headers)
            except requests.exceptions.RequestException as error:
                # print("Error: ", error)
                print(f'No response from printer at {network_printer[3]},'
                      f' go to Ackerson Hall, Room {network_printer[0]} to check it out')
            else:
                if page.status_code == 200:
                    soup = BeautifulSoup(page.content, 'lxml')
                    # status = soup.find('dd', class_='word-wrap').get_text()
                    title = soup.find('title').get_text()
                    print(f'Printer {title.split()[0]} was found')
