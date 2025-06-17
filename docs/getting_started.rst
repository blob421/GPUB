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

Required dependencies are included in requirements.txt and must be installed
in your python environment before proceeding.

With your python environment activated in the terminal:

- 1. Navigate to the directory where `requirements.txt` is located. 
     e.g. cd /desktop/project

- 2. pip install -r requirements.txt 


Starting GPUB
---------------
- 1. Launch run.bat or buyer.py . The program will ask for the number of pages to scan, I recommend 3-4 . The lower the faster .

- 2. The program will asks for a GPU model, the spacing is important. E.g.: 

    - tuf 5070 ti 
    - 5070 ti super 
    - xfx 6700 xt  
    - TUF 5080 ,
    - 6800

- 3. When the bot finds an in-stock GPU, it will display its price and attempt to purchase the 
     first one available. If someone was quicker , it'll try the other ones.
 