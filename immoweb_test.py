from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

def return_one_page():

    url = "https://www.immoweb.be/fr/annonce/immeuble-a-appartements/a-vendre/bruxelles-ville/1000/9302481?searchId=6091399b6e08f"
    driver = webdriver.Chrome()
    driver.get(url)
    return driver.page_source

if __name__=='__main__':
    print(return_one_page())