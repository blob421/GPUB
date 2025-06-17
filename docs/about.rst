About GPUB
============

GPUB: Fast & Automated GPU Purchasing Bot
-------------------------------------------
GPUB is a high-speed Python-based bot designed to automate the purchase of GPUs on Newegg.ca. 
Using Selenium WebDriver, GPUB efficiently scans product listings, checks for
availability, and executes purchases automatically—ensuring you secure the GPU you want before
it runs out of stock.

Key Features
--------------
- Automated Inventory Check: Scours product pages to find in-stock GPUs matching user-defined criterias.

- Fast Purchase Execution: Buys the first available GPU as fast as possible.

- Customizable Search: Users define search parameters, including keywords and number of pages to check.

- Optimized Efficiency: Runs every 5 minutes (adjustable) to stay ahead of market fluctuations.

- Headless Browser Mode: Uses Selenium in headless mode for stealthy and rapid interactions.

How It Works
-------------

- 1. Retrieves Search Parameters: GPUB loads user-defined search criteria (GPU model and pages to scan) from parameters.txt.

- 2. Asynchronous Scraping:

      - GPUB launches multiple scraping tasks concurrently using Python's asyncio.

      - Each task fetches a product listing from Newegg, ensuring rapid data collection.

- 3. Efficient Database Storage (aiosqlite)

      - GPUB leverages aiosqlite, an asynchronous SQLite wrapper, to store and update GPU links without blocking execution. 
        This allows simultaneous web scraping while writing to the database, minimizing delays.

- 4. Inventory Checking:

      - Extracts relevant product links using BeautifulSoup.

      - Applies keyword filtering to match user-defined GPU models.

- 5. Rapid Purchase Execution:

      - If a matching GPU is in stock, GPUB immediately starts the checkout process.

      - Ensures fast transaction handling via Selenium WebDriver for automated form completion.














Install dependencies (pip install -r requirements.txt).

Configure account credentials in account.txt.

Launch run.bat or buyer.py.

Define search parameters (number of pages & GPU model).

GPUB scans for available GPUs and initiates the fastest possible purchase.

Why Use GPUB?
In today's competitive GPU market, securing high-demand models can be challenging. GPUB automates the process, ensuring you never miss out on a restock and can secure your GPU before others do