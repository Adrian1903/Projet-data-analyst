import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from random import random

f = open("csv\\4-catalog_rakuten_ean.csv", "w")
f.write("ean,value,quantity\n")
f.close()

df_sales = pd.read_csv("C:\Adrian - GDrive\Professionnel\Formation\Informatique - Digital\Data University\Projet certification\csv\\3-sales.csv")
df_sales = df_sales[df_sales["isbn"].notna()]
print(df_sales["ean"].count())
df_sales["ean"] = df_sales["ean"].astype(str).str.slice(0,-2)

for isbn in df_sales["ean"]:
    sleep(1)
    
    url = "***" + isbn
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    
    try:
        quantity = soup.response.products.offercounts.used.string
    except:
        quantity = "None"
        value = "None"
    else:
        #print(isbn, " " , quantity)
        if (quantity != "0"):
            value = soup.response.products.bestprices.used.advertprice.amount.string
        else: 
            value = "None"
        
    print(f"{isbn},{value},{quantity}")

    f = open("csv\\4-catalog_rakuten_ean.csv", "a")
    f.write(isbn+","+value+","+quantity+"\n")
    f.close()


