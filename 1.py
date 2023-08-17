import os, sys
import datetime
import ssl
import urllib.request
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

EXTENSION_PATH = os.getcwd() + '/metamaskExtension.crx'
EXTENSION_ID = 'nkbihfbeogaeaoehlefnkodbefgpgknn'
recoveryPhrase = 'city blind canvas deal crisp behind worry hill slender long tray forum'
metamask_password = '1211998hA@'
script_path = os.path.realpath(os.path.dirname(__file__))
parent_path = os.path.dirname(script_path)
log_path = os.path.join(parent_path, "logs", "sync-nft-data")

def downloadMetamaskExtension():    
    print("Empty")

def launchSeleniumWebdriver():
    print('path', EXTENSION_PATH)
    chrome_options = Options()
    chrome_options.add_extension(EXTENSION_PATH)
    global driver
    
    driver_service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=driver_service, options=chrome_options)
 
    driver.maximize_window()
    sleep(2)
    return driver

    
def metamaskSetup(driver, recoveryPhrase, password):
    try:
       wait = WebDriverWait(driver, 10)

       # Switch to the second tab
       driver.switch_to.window(driver.window_handles[1])
       sleep(2)
       
       get_started_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Get Started"]')))
       driver.execute_script("arguments[0].click();", get_started_button)
       sleep(2)

       import_wallet_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Import wallet"]')))
       driver.execute_script("arguments[0].click();", import_wallet_button)
       sleep(2)

       no_thanks_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="No Thanks"]')))
       driver.execute_script("arguments[0].click();", no_thanks_button)
       sleep(2)

       secret_recovery_phrase = driver.find_element(By.XPATH, '//input[@placeholder="Paste Secret Recovery Phrase from clipboard"]')
       secret_recovery_phrase.send_keys(recoveryPhrase)
       checkbox1 = driver.find_element(By.XPATH, '//div[@class="first-time-flow__checkbox"]')
       driver.execute_script("arguments[0].click();", checkbox1) 
       sleep(2)

       password_new = driver.find_element(By.XPATH, '//input[@id="password"]')
       password_new.send_keys(password)
       password_confirm = driver.find_element(By.XPATH, '//input[@id="confirm-password"]')
       password_confirm.send_keys(password)
       checkbox2 = driver.find_element(By.XPATH, '//div[@class="first-time-flow__checkbox first-time-flow__terms"]')
       driver.execute_script("arguments[0].click();", checkbox2) 


       import_wallet_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Import"]')))
       driver.execute_script("arguments[0].click();", import_wallet_button)       
       sleep(7)
       
       all_done_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="All Done"]')))
       driver.execute_script("arguments[0].click();", all_done_button)       
       sleep(5)
       
       # closing the message popup after all done metamask screen
       close_popup = driver.find_element(By.XPATH, '//*[@id="popover-content"]/div/div/section/header/div/button')
       driver.execute_script("arguments[0].click();", close_popup)  
       sleep(2)

       eth_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='eth-overview__primary-currency']")))
       eth_element = eth_element.text
       output = eth_element.replace('\n', ' ')
       print("ETH: " + str(output))
    
       usd_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='eth-overview__secondary-currency']")))
       usd_element = usd_element.text
       output = usd_element.replace('\n', ' ')
       print("USD: " + str(output))

       print("Wallet has been imported successfully")
       sleep(2)
       # Switch to the first tab
       driver.switch_to.window(driver.window_handles[0])
       sleep(1)

    except TimeoutException:
       print("Timeout occurred while waiting for elements.")

    except Exception as e:
       print(f"An error occurred: {str(e)}")

def connectToWebsite(driver, url):
    try:
        print(url)
        # To open the website
        driver.get(url)
        sleep(5)

        # Connect to Metamask
        connect_metamask_button = driver.find_element(By.XPATH, '//*[@id="navbarSupportedContent"]/div/ul/li/button')
        driver.execute_script("arguments[0].click();", connect_metamask_button)
        sleep(1)
        print("Metamask connection initiated")

        connect_metamask_button1 = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div/div[3]/div/div[1]')
        driver.execute_script("arguments[0].click();", connect_metamask_button1)
        sleep(1)
        print("Metamask connection initiated")

        driver.switch_to.window(driver.window_handles[1])

        driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
        sleep(5)
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
        sleep(3)

        next_button = driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[4]/div[2]/button[2]')
        driver.execute_script("arguments[0].click();", next_button)
        sleep(2)
        connect_button = driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/footer/button[2]')
        driver.execute_script("arguments[0].click();", connect_button)
        sleep(2)
        
        # Successful connection
        status = 200
        message = "Metamask connection is successful"
        print('Site connected to Metamask')
        
    except Exception as e:
        status = 500
        message = f"Metamask connection failed: {str(e)}"
        print('Metamask connection failed:', str(e))
    
    finally:
        close_popup = driver.find_element(By.XPATH, '//*[@id="popover-content"]/div/div/section/header/div/button')
        driver.execute_script("arguments[0].click();", close_popup)
        sleep(2)
        driver.switch_to.window(driver.window_handles[0])
        sleep(2)
        
    return url, status, message

def main():
    try:       
        downloadMetamaskExtension()
        driver = launchSeleniumWebdriver()
        print(driver)
        # To import wallet
        metamaskSetup(driver, recoveryPhrase, metamask_password)
        sleep(2)

        url = "https://fxdex.tngbl.xyz/"
        message = connectToWebsite(driver, url)
        print(message)

    except Exception as e:
        print("An error occurred:", str(e))


if __name__ == '__main__':  
       main()