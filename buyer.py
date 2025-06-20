from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sqlite3
import time 
import json
import os
from fetch_links import fetch
from stock_checker import checker
import atexit


def load_parameters():
   """
    Loads user credentials from 'account.txt' into global variables.

    Reads email, password, and CVV from a JSON-formatted credentials file 
    and assigns them to global variables for authentication use.

    Raises:
      - FileNotFoundError: If 'account.txt' does not exist.
      - json.JSONDecodeError: If the file content is not valid JSON.
      - KeyError: If expected keys ('email', 'password', 'cvv') are missing.

    Note:
      - This function mutates global state and assumes the presence of valid keys in the credentials file.
   """
   global email, password, cvv
   with open("account.txt", "r") as credentials:
    data = json.load(credentials)
    email = data["email"]
    password = data["password"]
    cvv = data["cvv"]
  

def buy(email, password, cvv):
 """
    Automates the process of purchasing a product from Newegg using Selenium WebDriver.

    This function connects to a local SQLite database to retrieve product links, checks stock availability,
    and completes the checkout process using user credentials and CVV input. It handles cart interactions,
    form submission, and basic exception handling, aiming to finalize the transaction if an item is available.

    Args:
      - email (str): User's Newegg account email.
      - password (str): Corresponding account password.
      - cvv (str): 3-digit security code for the credit card on file.

    Returns:
        None

    Raises:
      - sqlite3.DatabaseError: If there is an issue reading from the product link database.
      - selenium.common.exceptions.TimeoutException: If page elements fail to load.
      - selenium.common.exceptions.WebDriverException: If the Selenium WebDriver fails.
      - json.JSONDecodeError: If account information in `account.txt` is improperly formatted.

    Flow:
      - 1. Connects to `site.sqlite` and retrieves stored product URLs.
      - 2. For each URL:
            - Loads product page.
            - Attempts to add item to cart.
            - Skips unavailable or error-prone products.
      - 3. Navigates to the cart and initiates the checkout.
      - 4. If not logged in:
            - Submits email and password.
      - 5. Inputs CVV and confirms order.
      - 6. Stops execution if a purchase is successful or skips to next if unsuccessful.

    Notes:
      - Requires a headless Chrome WebDriver.
      - Assumes account details are stored in `account.txt`.
      - Uses global flags (`bought`, `error`, `connected`) for external status signaling.
      - Designed for repeated execution in purchasing loops.

    Example:
       >>> buy("user@example.com", "hunter2", "123")
    """

 global bought, error, connected
 
 # Database init 
 conn = sqlite3.connect("site.sqlite")
 cursor = conn.cursor()

 cursor.execute('SELECT links FROM links')
 all_links = cursor.fetchall()
 
 try:
  
  if all_links and len(all_links[0][0]) > 5:
  
    pass
  
  else:
    print("Nothing was found in stock matching your criterias")
    print("Waiting...")
    return

 except IndexError:
  print("Nothing was found in stock matching your criterias")
  print("Waiting...")
  return


## Add to cart and skips warranty , skips if not in stock 
  
 for link in all_links:#[qty1 -1:qty2]:
    url = link[0]
    driver.get(url)

    try:
    
     add_to_cart = WebDriverWait(driver, 10).until(
     EC.element_to_be_clickable((By.CLASS_NAME, "btn-wide")))
     add_to_cart.click()
    
     
    
     button = WebDriverWait(driver, 10).until(
     EC.element_to_be_clickable((By.XPATH, "//*[@id='modal-intermediary']/div/div/div/div[3]/button[1]"))
      )
     button.click()
   
    except Exception as e:
     print(f'Error, going to the next link: {e}')
     continue
  
    ##Goes to the cart , handle the case when nothing is in the cart 
  
    try:
   
     driver.get("https://secure.newegg.ca/shop/cart")

     

     buy_button =WebDriverWait(driver, 10).until(
     EC.element_to_be_clickable((By.CLASS_NAME, "btn-wide")))
     buy_button.click()
  
     
     #refresh_button = driver.find_element(By.CLASS_NAME, "btn-orange")
     #refresh_button.click()
  
    except Exception as e:
     print(f'Error, going to the next link: {e}')
     continue
  
    
    if connected == 0:
     
     try:
      time.sleep(1)
      email_input = driver.find_element(By.ID, "labeled-input-signEmail")
      email_input.send_keys(email)
  
      refresh_button = WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable((By.CLASS_NAME, "btn-orange")))
      refresh_button.click()
      time.sleep(1)
    
      email_input = driver.find_element(By.ID, "labeled-input-password")
      email_input.send_keys(password)
  
      refresh_button = WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable((By.CLASS_NAME, "btn-orange")))
      refresh_button.click()
     
     except Exception:
      print("Wrong email or password")
      error = 1
      return
    
    if connected == 0:
      time.sleep(1)
      address_btn = WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable((By.CLASS_NAME, "checkout-step-action-done")))
      address_btn.click()
      connected = 1

    try:
     connected = 1
     time.sleep(2)
 
     cvv_input = WebDriverWait(driver, 10).until(
     EC.element_to_be_clickable((By.NAME, "cvvNumber")))
     cvv_input.click()
  
     for digit in cvv:
      cvv_input.send_keys(digit)
      time.sleep(0.5)
     
     try:
      address_btn = WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable((By.CLASS_NAME, "checkout-step-action-done")))
      address_btn.click()
      time.sleep(1)
     
     except:
      pass
     
     confirm_order_button = WebDriverWait(driver, 10).until(
     EC.element_to_be_clickable((By.CLASS_NAME, "bg-orange")))
     confirm_order_button.click()
     print("A GPU was bought, program exiting")
     bought = 1
     return
    
    except Exception:
     print("Looking for an other one ...")
     continue
   ### This part in the event of card needing an update , then loads the iframe 
   ### Shouldn't happen if a new card has been entered recently 
  
    """WebDriverWait(driver, 20).until(
      EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, "zoid-visible"))
  ) 
    card_details = WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable((By.CLASS_NAME, "mask-cardnumber"))
    )
  
    for digit in card_number:
      card_details.send_keys(digit)
      time.sleep(0.5)
  
    last = driver.find_element(By.CLASS_NAME, "button-m")
    last.click()"""
  ## IF nothing was bought 
  
 print("Nothing was bought")
 print("Waiting...")
  
## Deletes parameters.txt when exiting 

def delete():
  """
    Closes the Selenium WebDriver, terminates all Chrome processes, and deletes stored parameters.

    This function ensures a clean shutdown of browser automation by quitting the WebDriver 
    and forcefully terminating all active Chrome processes. Additionally, it removes the 
    `parameters.txt` file if it exists.

    Example:
        >>> delete()  # Stops browser automation and cleans up temporary data.
  """
  
  driver.quit()
  #os.system("taskkill /f /im chrome.exe")  # disabled for headless-mode
  if os.path.exists("parameters.txt"):
   os.remove("parameters.txt")
   
   
## Main program
atexit.register(delete)

## Will run in headless mode 
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # comment to disable
chrome_options.add_argument("--disable-crash-reporter")
chrome_options.add_argument("--disable-logging")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--disable-in-process-stack-traces")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--output=/dev/null")
chrome_options.add_argument("--blink-settings=imagesEnabled=false")
driver = webdriver.Chrome(options=chrome_options)

connected = 0
bought = 0
error = 0
email = None
password = None
cvv = None


def buy_main():
 """
    Repeatedly automates GPU purchasing until success or error.

    Executes an infinite loop to fetch product listings, check stock, and initiate
    automated purchases. On success or failure, it performs cleanup and exits.

    Raises:
      - SystemExit: When a GPU is purchased or an unrecoverable error occurs.

    Notes:
      - Calls supporting functions: fetch(), checker(), buy().
      - Waits 5 minutes between cycles if no purchase is made.
      - Ensures cleanup via delete() before termination.

    Example:
        >>> buy_main()
 """
 global bought, error
 load_parameters()

 while True:
  
  fetch()
  checker()
  buy(email, password, cvv)
  
  if bought == 1:
   delete()
   os._exit(0)

  if error == 1:
   delete()
   os._exit(0)
 
  else:
   time.sleep(300)

if __name__ == '__main__':
 buy_main()
  

