from ImmoScrapping import ImmoScrapping
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup


my_scrapper = ImmoScrapping('https://immo.vlan.be/fr')
path_to_research_field = "//input[@placeholder='Où ? Ville, Code Postal, Province ou Région.']"
input_sentence = '8000'
my_scrapper.start_research(path_to_research_field, input_sentence)
xpaths = ["//h2[@class='card-title text-ellipsis mb-1 d-inline with-small-icon appartment']",
          "//h2[@class='card-title text-ellipsis mb-1 d-inline with-small-icon house']"]
last_entry_location = ('a', {'rel':'nofollow'})
next_page_xpath = "//i[@class='fa fa-angle-right']"
print('compute number of page')
my_scrapper.get_number_pages(last_entry_location)
while True:
    for html_page in my_scrapper.scrap_page(xpaths):
        soup = BeautifulSoup(html_page)
        print(soup.find('title'))
    next_page_test = my_scrapper.next_page(next_page_xpath)
    if not next_page_test:
        break