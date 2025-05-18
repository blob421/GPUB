from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import sqlite3
import re

def checker():
 def is_in_stock():
  
  # Database init 

  conn = sqlite3.connect("site.sqlite")

  cursor = conn.cursor()

  cursor.execute('SELECT links FROM links')

  all_links = cursor.fetchall() #fetch from db all links 


  # Check if in stock function
  #count = 0


  chrome_options = Options()
  chrome_options.add_argument("--headless=new")
  chrome_options.add_argument("--disable-crash-reporter")
  chrome_options.add_argument("--disable-logging")
  chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

  chrome_options.add_argument("--disable-in-process-stack-traces")

  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--log-level=3")
  chrome_options.add_argument("--output=/dev/null")
  
  with webdriver.Chrome(options=chrome_options) as driver:

    for link in all_links:
     found = None
     url = link[0]
     driver.get(url)

     source = driver.page_source
 
     soup = BeautifulSoup(source, "html.parser")
 
     scripts = soup.find_all("script", {"type": "application/ld+json"}) 
   
     for script in scripts:
         
           script_text = script.string

           if "InStock" in script_text:
             found = True
             match = re.search(r'"price":"([\d\.]+)"', script_text)
             if match:
                sell_price = match.group(1)  # Extract the price value
                break
              
         
     if found == True:
        print(f"Found one at ${sell_price}")   
       # count += 1
     else: 
        print('Out of stock')
        cursor.execute('DELETE FROM links WHERE links = ?', (url,))
        
       

    conn.commit()
    cursor.close()  
    conn.close()           
   
    #if count == 0:
     # print("Nothing was found matching your criterias")
      
       
 

 is_in_stock()
   
