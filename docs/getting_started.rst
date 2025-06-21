Getting started
================

Saving a credit card 
---------------------
Before using the bot, you must create an account on Newegg.ca (if you don't already have one).
To ensure the bot can complete checkout, log in and save a credit card to your account.


Setting up account.txt
-----------------------
Before proceeding, you'll need to set up your credentials. 
Navigate to the root folder of the repository. 
Edit account.txt and replace the following fields to include these details:

 - YOUR_EMAIL : Your Newegg account email  
 - YOUR_PASSWORD : Your Newegg account password  
 - 123 : The CVV on the back of your credit card  


Required dependencies
----------------------
This program requires Python.

- Download the latest version of Python and ensure the "Add Python to PATH" option is checked 
  during installation.

- Required dependencies are included in requirements.txt and must be installed
  in your python environment before proceeding.

- With your python environment activated in the terminal:

   - 1. Navigate to the directory where `requirements.txt` is located. e.g. cd /desktop/project

   - 2. pip install -r requirements.txt 


Starting GPUB
---------------
- 1. Launch run.bat or buyer.py.  (Preferably 5 minutes before a release so the bot is logged-in)

- 2. The program will ask for the number of pages to scan, 3-4 is recommended. Input a number 
     and press enter.

- 3. The program will asks for a GPU model, the spacing is important. E.g.: 

    - tuf 5070 ti 
    - 5070 ti super 
    - xfx 6700 xt   
    - TUF 5080
    - 6800
   
- 4. If you're using GPUB for a release, you can pre-configure your search criteria by 
     creating a parameters.txt file in the root directory. Make sure it follows this format:
     
      - {"item": "Tuf 6070", "n": 3}
       
     Be more specific if you want to prioritize speed e.g. TUF 6070 rather than just 6070. 

- 5. When the bot finds in-stock GPUs, it will display their prices and attempt to purchase the 
     first one available. If someone was quicker , it'll try the other ones.
 