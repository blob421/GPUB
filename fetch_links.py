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
 """
    Loads search parameters from parameters.txt or prompts the user for input, then initializes the SQLite database.

    This function attempts to read item search parameters (`n`, `item`) from `parameters.txt`. 
    If the file is missing, it asks the user to input values and stores them for future runs.

    Additionally, it extracts keywords from the search item and sets up the `links` table in the database.

    Returns:
        None: The function modifies global variables and writes to the database, but does not return a value.

    Raises:
        FileNotFoundError: If `parameters.txt` is missing, the user is prompted for manual input.
        sqlite3.DatabaseError: If there is an issue initializing the database.

    Process Overview:

      - 1. Attempts to read search parameters (`n`, `item`) from `parameters.txt`.
      - 2. If missing, prompts the user to manually enter `n` (pages to search) and `item` (search keywords).
      - 3. Extracts up to three keywords (`item0`, `item1`, `item2`) for filtering.
      - 4. Initializes a SQLite database (`site.sqlite`).
      - 5. Creates or resets the `links` table for storing unique product links.

    Note:
    - `parameters.txt` must be formatted as a YAML dictionary.
    - Keywords (`item0`, `item1`, `item2`) are extracted dynamically from the user's input.
    - The function **drops** the `links` table before creating a fresh one.

    Example:
       >>> fetch()  # Loads parameters and initializes the database
    """
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
  """
    Scrapes product listing pages from Newegg and stores valid item links in a SQLite database.

    This asynchronous function retrieves the specified number of pages (`n`) from Newegg, 
    extracts `<a>` elements, filters links based on search keywords (`item0`, `item1`, `item2`), 
    and inserts unique links into the database.

    Args:
        n (int): The page number to retrieve from Newegg.

    Returns:
        None: The function performs asynchronous database operations but does not return a value.

    Raises:
        aiohttp.ClientError: If the request to Newegg fails.
        aiosqlite.Error: If there is an issue inserting data into the database.

    Process Overview:
       - 1. Fetches product listings from Newegg using `aiohttp`.
       - 2. Parses the page using `BeautifulSoup` to extract `<a>` elements.
       - 3. Filters links based on keywords (`item0`, `item1`, `item2`).
       - 4. Ensures exclusions (`ti`, `super`, `xt`) based on user input.
       - 5. Checks if links contain unwanted query strings (`#IsFeed`, `?Item=`).
       - 6. Inserts the filtered URLs into the SQLite database asynchronously.

    Note:
       - The function assumes `DB_PATH = 'site.sqlite'` as the database location.
       - Items (`item0`, `item1`, `item2`) must be defined globally before calling this function.
       - Filtering logic ensures only relevant product links are stored.

    Example:
       >>> await add_to_db(5)  # Scrapes page 5 from Newegg and stores valid links
  """

  
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
   """
    Executes multiple asynchronous scraping tasks concurrently.

    This function creates and gathers a list of asynchronous tasks that call `add_to_db(numb)`, 
    ensuring multiple pages are scraped simultaneously using `asyncio.gather()`. 
    The function runs asynchronously and is executed via `asyncio.run()`.

    Args:
        None: The function does not take any parameters but relies on the global `num` variable.

    Returns:
        None: The function runs asynchronously and does not return a value.

    Raises:
        ValueError: If `num` cannot be converted to an integer.
        asyncio.CancelledError: If any task is interrupted before completion.

    Process Overview:
      - 1. Iterates over a range from `0` to `num` to create scraping tasks.
      - 2. Calls `add_to_db(numb)` for each page asynchronously.
      - 3. Uses `asyncio.gather()` to execute all tasks concurrently.
      - 4. Runs the event loop using `asyncio.run()`.

    Note:
      - The function assumes `num` is a valid integer.
      - Requires `add_to_db(numb)` to be implemented and working.
      - Ensures efficient parallel execution to optimize scraping.

    Example Usage:
       >>>  asyncio.run(main())  # Runs asynchronous scraping for multiple pages.
   """


   tasks = [add_to_db(numb) for numb in range(int(num))]
   await asyncio.gather(*tasks)
    
 asyncio.run(main())
 

#cProfile.run("fetch()")


 


 
   






         
         
      
      
      




