from http.client import PAYMENT_REQUIRED
from bs4 import BeautifulSoup
import requests
import re

product = ("Input product you want to search for?")#can put into url and search for that product
url = f"https://www.newegg.ca/p/pl?d=3070&N=4131"
page = requests.get(url).text
soup = BeautifulSoup(page, 'html.parser')

page_text = soup.find(class_="list-tool-pagination-text").strong
pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])
print(pages)

items_found = {}

for page in range(1, pages + 1):
    url = f"https://www.newegg.ca/p/pl?d=3070&N=4131&page={page}"
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    
    #cause all the products are inside div
    div = soup.find(class_="item-cells-wrap border-cells itme-grid-view four cells explusion-one-cell")
    # now we gotta look for the just the product, cause not all product on page is our product
    items = div.find_all(text = re.compile(product))
    #used re as just finding product name wouldn't return us the names with product + " some string", it's strict, so we use re
    
    for item in items:
        parent = item.parent
        
        if parent.name != 'a':
            continue
        
        link = parent['href']
        # to find parent with specific class
        next_parent = parent.find_parent(class_= "item-container")
        try:
            price = next_parent.find(class_="price-current").strong.string
            items_found[item] = {"price" : int(price.replace(",","")), "link" : link}
        except:
            pass

#items() returns a tuple, we gonna sort it using 1(dictionary inside) and then access the price and sort it accordingly)
sorted_items = sorted(items_found.items(), key = lambda x: x[1]['price'])

#[('3090 FTW', {"price": 231, "link" : www.blablabla})]
for item in item_found:
    print(item[0])
    print(f"$ {item[1]['price']}")
    print(item[1]['link'])
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")