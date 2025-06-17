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

user_data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "chrome_profile"))

def buy():
 """
    Automates the purchase of a product from Newegg using Selenium.

    This function connects to a SQLite database to retrieve available product links, 
    verifies stock availability, and proceeds through the checkout process using Selenium WebDriver. 
    It handles authentication, adds items to the cart, enters payment details, and attempts to confirm 
    the order.

    Returns:
        None: The function modifies the database and interacts with the web interface, but does not return a value.

    Raises:
        sqlite3.DatabaseError: If database queries fail.
        selenium.common.exceptions.TimeoutException: If an element fails to load within the expected time.
        selenium.common.exceptions.WebDriverException: If the Chrome WebDriver encounters an issue.
        json.JSONDecodeError: If `account.txt` contains malformed JSON.

    Process Overview:
    1. Connects to `site.sqlite` and retrieves stored product links.
    2. Checks for availability and skips items that are out of stock.
    3. Uses Selenium to navigate to the product page and add items to the cart.
    4. Handles login authentication using stored credentials (`account.txt`).
    5. Proceeds through the checkout process, entering CVV and confirming the order.
    6. Removes out-of-stock items from the database.

    Note:
    - Requires Chrome WebDriver with appropriate configurations (`--headless`, `--disable-logging`, etc.).
    - Assumes user credentials (`email`, `password`, `cvv`, `card_number`) are stored in `account.txt`.
    - Filtering logic ensures only relevant and available products are purchased.

    Example Usage:
        buy()  # Executes the automated purchasing process.
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


 """quantity = how_many.split()
 qty1 = int(quantity[0])

 try:
  qty2 = int(quantity[1])

 except IndexError:
  qty2 = int(quantity[0])"""

 
 with open("account.txt", "r") as credentials:
  
  data = json.load(credentials)
  email = data["email"]
  password = data["password"]
  cvv = data["cvv"]
  card_number = data["card_number"]

## Add to cart and skips warranty , skips if not in stock 
  
  for link in all_links:#[qty1 -1:qty2]:
    url = link[0]
    driver.get(url)

    try:
    
     add_to_cart = WebDriverWait(driver, 10).until(
     EC.element_to_be_clickable((By.CLASS_NAME, "btn-wide")))
     add_to_cart.click()
    
     
    
     button = WebDriverWait(driver, 10).until(
     EC.element_to_be_clickable((By.XPATH, "//*[@id='modal-intermediary']/div/div/div/div[4]/button[1]"))
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

    Example Usage:
        delete()  # Stops browser automation and cleans up temporary data.
  """
  
  driver.quit()
  #os.system("taskkill /f /im chrome.exe")  # disabled for headless-mode
  if os.path.exists("parameters.txt"):
   os.remove("parameters.txt")
   
   


atexit.register(delete)

## Main program

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
chrome_options.add_argument(f"--user-data-dir={user_data_path}")
driver = webdriver.Chrome(options=chrome_options)

connected = 0
bought = 0
error = 0


def buy_main():
 """
    Continuously executes product retrieval, stock checking, and purchasing automation.

    This function runs an infinite loop that sequentially:
    1. Fetches product listings from Newegg.
    2. Checks their stock availability.
    3. Attempts to purchase available items.
    4. If a purchase is successful (`bought == 1`), it cleans up and exits.
    5. If an error occurs (`error == 1`), it performs cleanup and exits.
    6. Otherwise, it waits 5 minutes before repeating the cycle.

    Returns:
        None: The function runs indefinitely until a purchase or error triggers exit.

    Raises:
        SystemExit: If a GPU is successfully bought or an error occurs.
    
    Note:
    - Runs continuously until an item is purchased or an error occurs.
    - The cleanup process (`delete()`) ensures browser shutdown and removal of temporary files.
    - Optimized for repeated execution at 5-minute intervals.

    Example Usage:
        buy_main()  # Initiates automated purchasing loop.
 """
 global bought, error
 while True:
  
  fetch()
  checker()
  buy()
  
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
  

