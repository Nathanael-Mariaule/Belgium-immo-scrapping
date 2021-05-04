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
from page_scrapping import b_soup_immo

with open('data.csv', 'w') as file:
    file.write("adid, bedrooms, city, price, transaction_type, subtype, "
               "zipcode, adresse, surface, type_prop, etat, facades, surface_terrain, garden, "
               "garden_surface, terrasse, terrasse_surface, piscine, nombre_chambres, garage, surface_habitable, "
               "meuble, salles_de_bain, toilettes, cuisine_equipee, cheminee\n")

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
        with open('data.csv', 'a') as file:
            file.write(b_soup_immo(html_page)+"\n")
    next_page_test = my_scrapper.next_page(next_page_xpath)
    if not next_page_test:
        break