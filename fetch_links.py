from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
from bs4 import BeautifulSoup
import sqlite3
import yaml

# Input part , spacing is important
def fetch():
 try:
   with open("parameters.txt", "r") as params:
      dictio = yaml.safe_load(params.read())
      n = dictio["n"]
      item = dictio["item"]

 except FileNotFoundError:
    n = input('How many pages to search (0-10) ? 3 is recommended : ')
    item = input('What are you looking for ? (6700 xt , tuf 5080 ti, 4070 ti super, astral) : ')
    list = dict()
    list["n"] = n
    list["item"] = item
    
    with open("parameters.txt", "w") as file:
     file.write(str(list))
    


 item_word_list = item.split()
 item0 = item_word_list[0]

 try:
   item1 = item_word_list[1]
 except IndexError:
   item1 = None

 try: 
  item2 = item_word_list[2]
 except IndexError:
   item2= None



 # Database init
 conn = sqlite3.connect('site.sqlite')
 cursor = conn.cursor()
 cursor.executescript('''
 DROP TABLE IF EXISTS links;
 ''')
 cursor.execute('''CREATE TABLE IF NOT EXISTS links
 (id INTEGER PRIMARY KEY AUTOINCREMENT, links TEXT UNIQUE)''')


 ## Function to add desired links to the database

 def add_to_db():
  
  chrome_options = Options()
  chrome_options.add_argument("--headless=new")
  chrome_options.add_argument("--disable-crash-reporter")
  chrome_options.add_argument("--disable-logging")
  chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

  chrome_options.add_argument("--disable-in-process-stack-traces")

  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--log-level=3")
  chrome_options.add_argument("--output=/dev/null")
  
  page = 1
  while page <= int(n):             #Retreives n pages
 
       with webdriver.Chrome(options=chrome_options) as driver:

      
        driver.get(f'https://www.newegg.ca/p/pl?N=100006663&page={page}')
      

        # Switch to the new tab
      
        page_source = driver.page_source
    
        soup = BeautifulSoup(page_source, 'html.parser')
        anchors = soup('a')
    
        for anchor in anchors:
           href = anchor.get('href')
           if ( href is None ) : 
              continue  #Avoids the first none in source_page and fetch the hrefs in 'a'
           
           elif item2:
             if re.search(item0.lower(), href.lower()) and re.search(item1.lower(), href.lower()) and re.search(item2.lower(), href.lower()):
               
                if not "ti" in item.lower() and "ti" in href.lower():
                  continue
                if not "super" in item.lower() and "super" in href.lower():
                  continue   
                if not "xt" in item.lower() and "xt" in href.lower():
                  continue       
                
                if not '#IsFeed' in href:
                 if not '?Item=' in href:
                   
                    cursor.execute('INSERT OR IGNORE INTO links (links) VALUES ( ? )', ( (href), ) )
           
           elif item1:
             if re.search(item0.lower(), href.lower()) and re.search(item1.lower(), href.lower()):
               
                if not "ti" in item.lower() and "ti" in href.lower():
                  continue
                if not "super" in item.lower() and "super" in href.lower():
                  continue     
                if not "xt" in item.lower() and "xt" in href.lower():
                  continue  
                if not '#IsFeed' in href:
                 if not '?Item=' in href:
                   
                    cursor.execute('INSERT OR IGNORE INTO links (links) VALUES ( ? )', ( (href), ) )
           
           else:
             if re.search(item.lower(), href.lower()):
             
              if not "ti" in item.lower() and "ti" in href.lower():
                  continue
              if not "super" in item.lower() and "super" in href.lower():
                  continue   
              if not "xt" in item.lower() and "xt" in href.lower():
                  continue  
              
              if not '#IsFeed' in href:
                 if not '?Item=' in href:
          
                   cursor.execute('INSERT OR IGNORE INTO links (links) VALUES ( ? )', ( (href), ) )
        conn.commit()    #Add links to the db 

      
        page += 1
 
  
  conn.close()
  
 add_to_db()








 


 
   






         
         
      
      
      




