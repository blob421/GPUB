import re
from bs4 import BeautifulSoup
import sqlite3
import yaml
import asyncio
import aiohttp
import aiosqlite
#import cProfile


DB_PATH = 'site.sqlite'


def get_parameters():

 """
    Retrieves search parameters from `parameters.txt` or prompts the user for input.

    This function loads item search parameters (`number_of_pages`, `search_string`) from an external file.  
    If the file is missing, it prompts the user for input, validates the responses, and saves the data  
    for future use. It then extracts keywords from the search string and assigns them to global variables.

    Returns:
        None: Updates global variables but does not return a value.

    Raises:
        FileNotFoundError: If `parameters.txt` is missing, user input is requested.
        ValueError: If an invalid non-numeric entry is provided for `number_of_pages`.
        KeyError: If expected keys (`n`, `item`) are missing from the parameter file.

    Process Overview:
     - 1. Attempts to load `number_of_pages` and `search_string` from `parameters.txt`.
     - 2. If missing, prompts the user to enter a valid number of pages (integer).
     - 3. Prompts the user to enter the GPU search term and confirms input validity.
     - 4. Saves the validated parameters in a dictionary and writes them to `parameters.txt`.
     - 5. Extracts up to three keywords (`word_0`, `word_1`, `word_2`) for filtering.

    Notes:
     - `parameters.txt` must be formatted as a YAML dictionary.
     - If fewer than three keywords are provided, missing values default to `None`.
     - User input for `number_of_pages` is validated to prevent non-numeric entries.
     - Ensures proper formatting for search terms before storing them.

    Example Usage:
        >>> get_parameters()  # Loads parameters, validates input, and initializes global variables.
 """
 global number_of_pages, search_string, word_0, word_1, word_2

 try:
   
   with open("parameters.txt", "r") as file:
      parameters = yaml.safe_load(file.read())
      number_of_pages = parameters["n"]
      search_string = parameters["item"]


 except FileNotFoundError:  
    while True:   
     
      try:
        number_of_pages = int(input("How many pages to search (0-10)? 3 is recommended: "))
        break 
   
      except ValueError:
        print("This is not a valid number, try again.")

    
    
    while True:
     search_string = input('What are you looking for ? (6700 xt , tuf 5080 ti, 4070 ti super, astral) : ')
     proceed = input(f'Confirm search for : {search_string} ? Input (y) or (n) ')
   
     if proceed.lower() == 'y':
       break
    

    parameters = dict()
    parameters["n"] = number_of_pages
    parameters["item"] = search_string
    
    with open("parameters.txt", "w") as file:
       file.write(str(parameters))
    


 string_words = search_string.split()

 word_0 = string_words[0]

 try:
   word_1 = string_words[1]
 except IndexError:
   word_1 = None

 try: 
  word_2 = string_words[2]
 except IndexError:
   word_2= None





async def add_to_db(n):
  """
    Scrapes product listing pages from Newegg and stores valid item links in a SQLite database.

    This asynchronous function retrieves the specified page (`n`) from Newegg, 
    extracts `<a>` elements, filters product links based on search keywords (`word_0`, `word_1`, `word_2`), 
    and inserts unique links into the database.

    Args:
        n (int): The page number to retrieve and scrape from Newegg.

    Returns:
        None: The function performs asynchronous database operations but does not return a value.

    Raises:
        aiohttp.ClientError: If the request to Newegg fails.
        aiosqlite.Error: If there is an issue inserting data into the database.
        sqlite3.DatabaseError: If database initialization fails.

    Process Overview:
     - 1. Connects to a SQLite database (`site.sqlite`) and initializes the `links` table.
     - 2. Fetches product listings from Newegg using `aiohttp`.
     - 3. Parses the page with `BeautifulSoup` to extract `<a>` elements.
     - 4. Filters links based on predefined keywords (`word_0`, `word_1`, `word_2`).
     - 5. Applies exclusions (`ti`, `super`, `xt`) based on user input.
     - 6. Ensures links do not contain unwanted query strings (`#IsFeed`, `?Item=`).
     - 7. Inserts filtered URLs into the database asynchronously.

    Notes:
     - The function assumes `DB_PATH = 'site.sqlite'` as the database location.
     - Keywords (`word_0`, `word_1`, `word_2`) must be defined globally before calling this function.
     - Filtering logic ensures **only relevant product links** are stored in the database.

    Example Usage:
        >>> await add_to_db(5)  # Scrapes page 5 from Newegg and stores valid links
  """


  
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

   get_parameters()
   tasks = [add_to_db(numb) for numb in range(int(number_of_pages))]
   await asyncio.gather(*tasks)


def fetch():
   """Starts the asynchronous scraping process by running `main()`.

      This function ensures the module is importable in buyer.py.
   """
    
   asyncio.run(main())
 


#cProfile.run("fetch()")

 


 
   






         
         
      
      
      




