import re
from bs4 import BeautifulSoup
import sqlite3
import yaml
import asyncio
import aiohttp
#import cProfile
import aiosqlite

# Input part 

DB_PATH = 'site.sqlite'

def fetch():
 try:
   with open("parameters.txt", "r") as params:
      dictio = yaml.safe_load(params.read())
      num = dictio["n"]
      item = dictio["item"]

 except FileNotFoundError:
    num = input('How many pages to search (0-10) ? 3 is recommended : ')
    item = input('What are you looking for ? (6700 xt , tuf 5080 ti, 4070 ti super, astral) : ')
    list = dict()
    list["n"] = num
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

 async def add_to_db(n):
                                #Retreives n pages
  async with aiohttp.ClientSession() as requests:
    async with requests.get(f'https://www.newegg.ca/p/pl?N=100006663&page={n}') as response:
        response_text = await response.text()
    
        soup = BeautifulSoup(response_text, 'html.parser')
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
                    async with aiosqlite.connect(DB_PATH) as db:
                     await db.execute('INSERT OR IGNORE INTO links (links) VALUES ( ? )', ( (href), ) )
                     await db.commit()    
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
                   
                   async with aiosqlite.connect(DB_PATH) as db:
                     await db.execute('INSERT OR IGNORE INTO links (links) VALUES ( ? )', ( (href), ) )
                     await db.commit()    
           
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
          
                   async with aiosqlite.connect(DB_PATH) as db:
                     await db.execute('INSERT OR IGNORE INTO links (links) VALUES ( ? )', ( (href), ) )
                     await db.commit()    
  

 

 async def main():

   tasks = [add_to_db(numb) for numb in range(int(num))]
   await asyncio.gather(*tasks)
    
 asyncio.run(main())
 

#cProfile.run("fetch()")


 


 
   






         
         
      
      
      




