import pandas as pd
import requests
import urllib.request
import time
from bs4 import BeautifulSoup

# Initialize an empty list to store all the scraped data
all_data = []

for char_code in range(ord('A'), ord('Z')+1):
    url = 'https://www.malaysiastock.biz/Listed-Companies.aspx?type=A&value=' + chr(char_code)
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.findAll('table', {'class': 'marketWatch'})

    # Extract data from the table and append to all_data list
    if table:
        example = list(table[0])
        example2 = [x for x in example if x != "\n"]
        prices = []
        for i in range(1, len(example2)):
            entry = example2[i].get_text(separator="\n").split("\n")
            entry_filtered = [x for x in entry if x]
            prices.append(entry_filtered)
        all_data.extend(prices)
        
    print("Done the process of scraping from " + url)

# Create DataFrame from the accumulated data
complete_table = pd.DataFrame(all_data, columns=["Company Code", "Market", "Company Name", "Sector", "Market Cap", "Last Price", "PE", "DY", "ROE"])

complete_table.to_csv('complete_data.csv', index=False)