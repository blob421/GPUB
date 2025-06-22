import re
from bs4 import BeautifulSoup
import sqlite3

import asyncio
import aiohttp
import aiosqlite

#import cProfile

DB_PATH = 'site.sqlite'

#Mocking parameters
search_string = "TUF 5070 ti"
word_0 = "TUF"
word_1 = "5070"
word_2 = "ti"
number_of_pages = 1 


async def add_to_db(n):
 

  # Database init
  conn = sqlite3.connect('site.sqlite')
  cursor = conn.cursor()
  cursor.executescript('''
  DROP TABLE IF EXISTS links;
  ''')
  cursor.execute('''CREATE TABLE IF NOT EXISTS links
  (id INTEGER PRIMARY KEY AUTOINCREMENT, links TEXT UNIQUE)''')

  #Retreives n pages
  async with aiohttp.ClientSession() as requests:
    async with requests.get(f'https://www.newegg.ca/p/pl?N=100006663&page={n}') as response:
        response_text = await response.text()
        assert "GPU & Video Graphics Device" in response_text
        print('Still the gpu category endpoint')
        soup = BeautifulSoup(response_text, 'html.parser')
        anchors = soup('a')
    
        for anchor in anchors:
           href = anchor.get('href')
           if ( href is None ) : 
              continue  #Avoids the first none in source_page and fetch the hrefs in 'a'
           
           elif word_2:
             if re.search(word_0.lower(), href.lower()) and re.search(word_1.lower(), href.lower()) and re.search(word_2.lower(), href.lower()):
               
                if not "ti" in search_string.lower() and "ti" in href.lower():
                  continue
                if not "super" in search_string.lower() and "super" in href.lower():
                  continue   
                if not "xt" in search_string.lower() and "xt" in href.lower():
                  continue       
                
                if not '#IsFeed' in href:
                 if not '?Item=' in href:
                    async with aiosqlite.connect(DB_PATH) as db:
                     await db.execute('INSERT OR IGNORE INTO links (links) VALUES ( ? )', ( (href), ) )
                     await db.commit()    
           elif word_1:
             if re.search(word_0.lower(), href.lower()) and re.search(word_1.lower(), href.lower()):
               
                if not "ti" in search_string.lower() and "ti" in href.lower():
                  continue
                if not "super" in search_string.lower() and "super" in href.lower():
                  continue     
                if not "xt" in search_string.lower() and "xt" in href.lower():
                  continue  
                if not '#IsFeed' in href:
                 if not '?Item=' in href:
                   
                   async with aiosqlite.connect(DB_PATH) as db:
                     await db.execute('INSERT OR IGNORE INTO links (links) VALUES ( ? )', ( (href), ) )
                     await db.commit()    
           
           else:
            
             if re.search(search_string.lower(), href.lower()):
             
              if not "ti" in search_string.lower() and "ti" in href.lower():
                  continue
              if not "super" in search_string.lower() and "super" in href.lower():
                  continue   
              if not "xt" in search_string.lower() and "xt" in href.lower():
                  continue  
              
              if not '#IsFeed' in href:
                 if not '?Item=' in href:
          
                   async with aiosqlite.connect(DB_PATH) as db:
                     await db.execute('INSERT OR IGNORE INTO links (links) VALUES ( ? )', ( (href), ) )
                     await db.commit()    
  

async def main():
   
   """
    Executes multiple asynchronous scraping tasks concurrently.

    This function initializes search parameters and launches asynchronous tasks to scrape multiple 
    pages from Newegg using `add_to_db(numb)`. It efficiently manages multiple tasks via `asyncio.gather()`, 
    ensuring pages are processed simultaneously. The event loop is executed using `asyncio.run()`.

    Returns:
        None: The function performs asynchronous operations but does not return a value.

    Raises:
        ValueError: If `number_of_pages` cannot be converted to an integer.
        asyncio.CancelledError: If any scraping task is interrupted before completion.

    Process Overview:
     - 1. Calls `get_parameters()` to retrieve user-defined search criteria.
     - 2. Iterates over a range from `0` to `number_of_pages` to create scraping tasks.
     - 3. Launches each task asynchronously via `add_to_db(numb)`.
     - 4. Uses `asyncio.gather()` to execute all tasks concurrently.
     - 5. Runs the event loop using `asyncio.run(main())`.

    Notes:
     - Assumes `number_of_pages` is a valid integer retrieved from `get_parameters()`.
     - Requires `add_to_db(numb)` to be implemented and working correctly.
     - Optimized for concurrent execution to speed up data collection.

    Example Usage:
        >>> asyncio.run(main())  # Initiates multiple concurrent scraping tasks.
   """

   
   tasks = [add_to_db(numb) for numb in range(int(number_of_pages))]
   await asyncio.gather(*tasks)


def test_fetch():
   """Starts the asynchronous scraping process by running `main()`.

      This function ensures the module is importable in buyer.py.
   """
   global search_string, number_of_pages
    
  
    
   asyncio.run(main())
 


#cProfile.run("fetch()")

 


 
   






         
         
      
      
      




