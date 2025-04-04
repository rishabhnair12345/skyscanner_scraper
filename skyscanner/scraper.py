import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import random

# Flight search details
SOURCE_AIRPORT = "JRG"
DESTINATION_AIRPORT = "TRV"
DEPARTURE_DATE = "10"
DEPARTURE_MONTH = "May"

# Proxy Configuration (If Needed)
PROXY = "your-proxy-ip:port"  # Change this to a working proxy

# User-Agents List for Randomization
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
]

def scrape_skyscanner():
    print("[INFO] Launching Skyscanner Scraper...")

    options = Options()
    options.add_argument("--incognito")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

    #options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--enable-javascript")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
   # options.add_argument("--headless=new")  # New headless mode
    
    # Use Proxy if provided
    if PROXY:
        options.add_argument(f"--proxy-server=http://{PROXY}")
    
    driver = uc.Chrome(options=options)
    
    try:
        driver.get("https://www.skyscanner.co.in/")
        print("[INFO] Page Loaded:", driver.title)
        time.sleep(random.uniform(5, 10))  # Random delay to avoid detection
        
        # Check for CAPTCHA / Bot detection page
        if "robot" in driver.page_source.lower():
            print("[WARNING] Bot detection triggered! Consider changing proxy or adding captcha solving.")
            return
        
        # Input source airport
        from_input = driver.find_element(By.XPATH, "//label[@id='originInput-label']//input")
        from_input.send_keys(SOURCE_AIRPORT)
        time.sleep(random.uniform(2, 5))
        from_input.send_keys(Keys.RETURN)

        # Input destination airport
        to_input = driver.find_element(By.NAME, "fsc-destination-search")
        to_input.send_keys(DESTINATION_AIRPORT)
        time.sleep(random.uniform(2, 5))
        to_input.send_keys(Keys.RETURN)

        # Select departure date
        month_text = driver.find_element(By.XPATH, "//div[@data-testid='calendar']//div/h2")
        next_month_button = driver.find_element(By.XPATH, "//button[contains(@aria-label,'Next month')]")
        date_month_selector = driver.find_element(By.XPATH, f"//div[@aria-label='{DEPARTURE_MONTH}']//button[text()='{DEPARTURE_DATE}']")

        for _ in range(5):  # Loop to find the correct month
            if month_text.text != DEPARTURE_MONTH:
                next_month_button.click()
                time.sleep(1)
        date_month_selector.click()
        time.sleep(random.uniform(2, 5))
        
        # Submit search
        search_button = driver.find_element(By.XPATH, "//button[text()='Search']")
        search_button.click()
        print("[INFO] Searching for flights...")
        time.sleep(10)
        
        # Scrape flight prices
        soup = BeautifulSoup(driver.page_source, "html.parser")
        prices = soup.find_all("span", class_="BpkText_bpk-text__1PQUi BpkText_bpk-text--lg__3_UZR")
        
        if prices:
            print("[SUCCESS] Flight Prices Found:")
            for price in prices[:5]:  # Show top 5 results
                print(price.get_text())
        else:
            print("[WARNING] No prices found!")
    
    except Exception as e:
        print("[ERROR] Scraper failed:", str(e))
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_skyscanner()
