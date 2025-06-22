from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import sqlite3
import re


def test_is_in_stock():
  
  # Database init 

  conn = sqlite3.connect("site.sqlite")

  cursor = conn.cursor()

  cursor.execute('SELECT links FROM links')

  all_links = cursor.fetchall() 

  # Chrome options

  chrome_options = Options()
  chrome_options.add_argument("--headless=new")
  chrome_options.add_argument("--disable-crash-reporter")
  chrome_options.add_argument("--disable-logging")
  chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
  chrome_options.add_argument("--blink-settings=imagesEnabled=false")
  chrome_options.add_argument("--disable-in-process-stack-traces")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--log-level=3")
  chrome_options.add_argument("--output=/dev/null")
  
  # Stock checker

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
           
         try:   
           
           if "InStock" in script_text:
             found = True
             match = re.search(r'"price":"([\d\.]+)"', script_text)
             print('"Instock" is in scripts')

             try:
               assert '{"@context":"http://schema.org/","@type":"Product"' in script_text

             except:
               raise Exception('WARNING, Script format for "InStock" changed')
          
             try:
                if match:            
                  sell_price = match.group(1)  # Extracts the price value
                  print("Price is where expected")
                  break
                         
             except:    
               raise Exception('WARNING, "price" is not where expected!')
            
         except:
           raise Exception('WARNING, "InStock" not in scripts')

             
              
     if found == True:
        print(f"Found one at ${sell_price}")   
      
        
      
    conn.commit()
    cursor.close()  
    conn.close()           
      

   