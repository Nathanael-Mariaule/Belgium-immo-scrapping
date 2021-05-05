from bs4 import BeautifulSoup
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
    html = return_one_page()

def b_soup_immo_web(html):
    soup = BeautifulSoup(html,'lxml')
    json = soup.find_all("script")
    print(json[2])
    start, end = find_brackets(json[2])
    json_clean = json[2][start:end+1]
    print(json_clean)
    
    """headers = soup.find_all("th", {"class":"classified-table__header"})
    
    adid, bedrooms, city, price, transaction_type, subtype, zipcode, adresse, surface, type_prop,
    etat, facades, surface_terrain, garden, garden_surface, terrasse, terrasse_surface, piscine,
    nombre_chambres, garage, surface_habitable, meuble, salles_de_bain, toilettes, cuisine_equipee, cheminee = None *27
    
    for header in headers:
        text = header.string.strip()
        print(text)
        if text == "Surface habitable":
            surface_habitable = header.find_next_sibling().text.strip()[0:4].strip()
        elif text == "Nombre de façades":
            facades = header.find_next_sibling().text.strip()
        elif text == "État du bâtiment":
            etat = header.find_next_sibling().text.strip()
        elif text == "Quartier ou lieu-dit":
            = header.find_next_sibling().text.strip()"""
        
        
    print(facades, surface_habitable)

def find_brackets(text){
    index1, index2 = -1, -1
    
    for i, c in enumerate(text):
          if c == "{":
            index1 = i
            break
    
    for i in range(len(text), 0, -1):
          if text[i] == "}":
            index2 = i
            break
    
    return index1, index2
}
"""        
adid, bedrooms, city, price, transaction_type, subtype, zipcode, adresse, surface, type_prop,
etat, facades, surface_terrain, garden, garden_surface, terrasse, terrasse_surface, piscine,
nombre_chambres, garage, surface_habitable, meuble, salles_de_bain, toilettes, cuisine_equipee, cheminee"""
b_soup_immo_web(html)