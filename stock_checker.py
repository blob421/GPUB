from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import sqlite3
import re


def is_in_stock():
  """
    Checks product availability for stored links and updates the database accordingly.

    This function retrieves stored product URLs from a SQLite database, loads each page using 
    Selenium WebDriver, and parses the content with BeautifulSoup. It verifies stock availability 
    using structured JSON (`ld+json`) and extracts the product price if available. Out-of-stock 
    links are removed from the database.

    Returns:
        None: The function operates directly on stored links in the database.

    Raises:
        sqlite3.DatabaseError: If database queries fail.
        selenium.common.exceptions.WebDriverException: If Chrome WebDriver encounters an issue.
        AttributeError: If the parsed data does not contain expected JSON stock information.

    Process Overview:
      - 1. Retrieves stored product URLs from `site.sqlite`.
      - 2. Loads each product page using a headless Chrome WebDriver.
      - 3. Extracts page content and searches for structured JSON (`ld+json` scripts).
      - 4. Determines stock status based on "InStock" keyword presence.
      - 5. Displays product price if available.
      - 6. Deletes out-of-stock items from the database.

    Note:
     - The function leverages structured data (`application/ld+json`) for precise stock tracking.
     - Database entries are modified dynamically based on availability.
     - Uses optimized Chrome WebDriver settings to improve performance.

    Example Usage:
       >>> is_in_stock()  # Scans product links and updates stock status.
  """
  
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

           if "InStock" in script_text:
             found = True
             match = re.search(r'"price":"([\d\.]+)"', script_text)
            
             if match:
                sell_price = match.group(1)  # Extracts the price value
                break
                    
     if found == True:
        print(f"Found one at ${sell_price}")   
      
     else: 
        print('Out of stock')
        cursor.execute('DELETE FROM links WHERE links = ?', (url,))
        
      
    conn.commit()
    cursor.close()  
    conn.close()           
      

def checker():
   """Starts the stock-checking process by running `is_in_stock()`.
   
      This function ensures the module is importable in buyer.py.
   """
   is_in_stock()
   
