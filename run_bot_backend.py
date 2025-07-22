from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import logging
import json
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_webdriver(proxy_config, headless=False):
    """Initializes the Chrome webdriver with proxy settings."""
    options = Options()
    if proxy_config.get("enabled") and proxy_config.get("host") and proxy_config.get("port"):
        host = proxy_config["host"]
        port = proxy_config["port"]
        username = proxy_config.get("username")
        password = proxy_config.get("password")

        if username and password:
            proxy_server = f"http://{username}:{password}@{host}:{port}"
            logging.info(f"🚀 Using authenticated proxy: {host}:{port}")
        else:
            proxy_server = f"http://{host}:{port}"
            logging.info(f"🚀 Using proxy server: {host}:{port}")
        
        options.add_argument(f'--proxy-server={proxy_server}')
    
    if headless:
        logging.info("👻 Running in headless mode.")
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def find_element(wait, selector_info, clickable=False):
    """Finds an element based on selector info from config."""
    by = getattr(By, selector_info['by'])
    if clickable:
        return wait.until(EC.element_to_be_clickable((by, selector_info['value'])))
    return wait.until(EC.presence_of_element_located((by, selector_info['value'])))

def login(driver, profile_data, almaviva_url, selectors):
    """Navigates to the login page, waits for CAPTCHA, and logs the user in."""
    try:
        logging.info(f"Navigating to home page: {almaviva_url}")
        driver.get(almaviva_url)

        wait_for_home_page = WebDriverWait(driver, 30)
        login_selectors = selectors['login_page']
        
        logging.info("Attempting to find and click profile icon.")
        go_to_login_btn = find_element(wait_for_home_page, login_selectors['go_to_login_button'], clickable=True)
        go_to_login_btn.click()
        
        email_selector = login_selectors['email_input']

        logging.info("Waiting for the login page to load...")
        logging.info(f"The script will wait for the email field ('{email_selector['value']}') to appear before continuing.")

        wait_for_login_page = WebDriverWait(driver, 300)
        email_input = find_element(wait_for_login_page, email_selector)

        wait_for_elements = WebDriverWait(driver, 20)
        password_input = find_element(wait_for_elements, login_selectors['password_input'])
        login_button = find_element(wait_for_elements, login_selectors['login_button'], clickable=True)

        email_input.send_keys(profile_data['email'])
        password_input.send_keys(profile_data['password'])
        login_button.click()
        
        logging.info("✅ Login successful for %s", profile_data['email'])
        return True
    except Exception as e:
        logging.error("❌ Failed to login for profile %s: %s", profile_data.get('email', 'N/A'), e)
        logging.error("This could be due to a timeout waiting for the login page, or incorrect credentials/selectors.")
        return False

def navigate_to_appointments(driver, wait, selectors):
    """Navigates from the dashboard to the appointment booking page."""
    try:
        nav_selectors = selectors['navigation']
        take_appointment_btn = find_element(wait, nav_selectors['take_appointment_button'], clickable=True)
        take_appointment_btn.click()
        logging.info("✅ Navigated to the 'Take an appointment' page.")
        return True
    except Exception as e:
        logging.error("❌ Failed to navigate to the appointment page: %s", e)
        return False

def book_visa_appointment(driver, wait, profile_data, selectors):
    """Fills the visa form in a two-step process and handles the appointment booking loop."""
    try:
        logging.info("📝 Starting appointment booking process...")
        form_selectors = selectors['booking_form']
        
        # --- Page 1: Fill Initial Form ---
        logging.info("Filling out the first page of the appointment form.")
        
        Select(find_element(wait, form_selectors['center_select'])).select_by_visible_text(profile_data['center'])
        Select(find_element(wait, form_selectors['service_level_select'])).select_by_visible_text(profile_data['service_level'])
        Select(find_element(wait, form_selectors['visa_type_select'])).select_by_visible_text(profile_data['visa_type'])
        find_element(wait, form_selectors['num_visas_input']).send_keys(profile_data['num_visas'])
        
        find_element(wait, form_selectors['terms_checkbox'], clickable=True).click()
        find_element(wait, form_selectors['privacy_checkbox'], clickable=True).click()
        
        find_element(wait, form_selectors['check_availability_button'], clickable=True).click()
        logging.info("✅ First page of form submitted successfully.")
        
        # --- Page 2: Enter Trip Date and Find Slot ---
        logging.info("On the second page, entering trip date.")
        
        # Wait for the trip date input to be present on the new page
        trip_date_input = find_element(wait, form_selectors['trip_date_input'])
        trip_date_input.clear()
        trip_date_input.send_keys(profile_data['trip_date'])
        
        logging.info("Trip date entered. Now searching for available slots...")

    except Exception as e:
        logging.error("❌ Failed to fill form for profile %s: %s", profile_data.get('email', 'N/A'), e)
        return

    time.sleep(5) # Allow time for the page to update after entering date

    booking_selectors = selectors['booking_page']
    while True:
        try:
            if booking_selectors['no_appointments_text'] in driver.page_source:
                logging.info("🔄 No appointments available. Retrying in 30 seconds...")
                time.sleep(30)
                driver.refresh()
                continue

            earliest_slot = find_element(wait, booking_selectors['book_button'], clickable=True)
            earliest_slot.click()
            logging.info("🎉 SUCCESS! Booked the earliest available appointment!")
            break
        except Exception:
            logging.warning("⚠️ No bookable slots found on the page. Refreshing in 30 seconds...")
            time.sleep(30)
            driver.refresh()

def run_automation(profile_data, proxy_config, almaviva_url, selectors, headless=False):
    """Main function to run the entire visa bot automation process."""
    driver = None
    try:
        driver = get_webdriver(proxy_config, headless=headless)
        
        if not login(driver, profile_data, almaviva_url, selectors):
            return

        # Create the standard wait object only after login is successful
        wait = WebDriverWait(driver, 20)

        if not navigate_to_appointments(driver, wait, selectors):
            return
        
        book_visa_appointment(driver, wait, profile_data, selectors)

    except Exception as e:
        logging.error("❌ An unexpected error occurred during automation: %s", e)
    finally:
        if driver:
            logging.info("Automation finished. Browser will remain open for inspection.")
            # driver.quit()

def main():
    """Entry point for command-line execution."""
    parser = argparse.ArgumentParser(description="Visa Appointment Bot")
    parser.add_argument("--user", required=True, help="The user profile name from config.json to run.")
    parser.add_argument("--headless", action="store_true", help="Run the browser in headless mode.")
    args = parser.parse_args()

    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        logging.error("❌ config.json not found. Please create it.")
        return

    profile_data = config.get('profiles', {}).get(args.user)
    if not profile_data:
        logging.error(f"❌ User '{args.user}' not found in config.json.")
        return
        
    proxy_config = config.get('proxy', {})
    almaviva_url = config.get('almaviva_url')
    selectors = config.get('selectors', {})

    logging.info(f"Starting bot for user: {args.user}")
    run_automation(profile_data, proxy_config, almaviva_url, selectors, headless=args.headless)

if __name__ == "__main__":
    main()
