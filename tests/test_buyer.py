from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import time 
import json

def test_buy():
 
 try: 
 
  with open("account.txt", "r") as credentials:
    data = json.load(credentials)
    email = data["email"]
    password = data["password"]
    cvv = data["cvv"]
  
 except:
   raise Exception('Invalid credentials in account.txt')
 
 
 # Database init 

 with sqlite3.connect("site.sqlite") as conn:
  
  cursor = conn.cursor()

  cursor.execute('SELECT links FROM links')

  all_links = cursor.fetchall()
  
  url = all_links[0][0]


# Testing the buttons while adding to cart

 connected = 0

 for n in range(1):
  
    driver.get(url)

    if connected == 0:
     
     add_to_cart = WebDriverWait(driver, 10).until(
     EC.element_to_be_clickable((By.CLASS_NAME, "btn-wide")))
     assert add_to_cart.is_displayed() and add_to_cart.is_enabled()
     add_to_cart.click()
   
    
     button = WebDriverWait(driver, 10).until(
     EC.element_to_be_clickable((By.XPATH, "//*[@id='modal-intermediary']/div/div/div/div[3]/button[1]"))
      )
     assert button.is_displayed() and button.is_enabled()
     button.click()
   
    
    # Testing the buttons in the cart
  
    if connected == 0:
   
     driver.get("https://secure.newegg.ca/shop/cart")

     buy_button =WebDriverWait(driver, 10).until(
     EC.element_to_be_clickable((By.CLASS_NAME, "btn-wide")))
     assert buy_button.is_displayed() and buy_button.is_enabled()
     buy_button.click()
  
  
    if connected == 0:
     
    
      time.sleep(1)
      email_input = driver.find_element(By.ID, "labeled-input-signEmail")
      assert email_input.is_displayed() and email_input.is_enabled()
      email_input.send_keys(email)
      
      refresh_button = WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable((By.CLASS_NAME, "btn-orange")))
      assert refresh_button.is_displayed() and refresh_button.is_enabled()
      refresh_button.click()
      time.sleep(1)
      
      password_input = driver.find_element(By.ID, "labeled-input-password")
      assert password_input.is_displayed() and password_input.is_enabled()
      password_input.send_keys(password)
  
      refresh_button = WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable((By.CLASS_NAME, "btn-orange")))
      assert refresh_button.is_displayed() and refresh_button.is_enabled()
      refresh_button.click()
     
    
    
    if connected == 0:
      time.sleep(1)
      address_btn = WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable((By.CLASS_NAME, "checkout-step-action-done")))
      assert address_btn.is_displayed() and address_btn.is_enabled()
      address_btn.click()
      connected = 1

    if connected == 1:
     connected = 1
     time.sleep(2)
 
     cvv_input = WebDriverWait(driver, 10).until(
     EC.element_to_be_clickable((By.NAME, "cvvNumber")))
     assert cvv_input.is_displayed() and cvv_input.is_enabled()
     cvv_input.click()
  
     for digit in cvv:
      cvv_input.send_keys(digit)
      time.sleep(0.5)
     
     try:
      address_btn = WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable((By.CLASS_NAME, "checkout-step-action-done")))
      assert address_btn.is_displayed() and address_btn.is_enabled()
      address_btn.click()
      time.sleep(1)
     
     except:
      pass
     
     #Order confirmation disabled for testing
     """
     confirm_order_button = WebDriverWait(driver, 10).until(
     EC.element_to_be_clickable((By.CLASS_NAME, "bg-orange")))
     assert confirm_order_button.is_displayed() and confirm_order_button.is_enabled()
     confirm_order_button.click()
     print("A GPU was bought, program exiting")
     bought = 1
     return"""
    
 
 print("All test passed")
 print("Buttons working...")
  

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








