
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pickle
import random
import pandas as pd
from immoweb_page_scrapping import scrap_page

class ImmoWebScrapping:
    def __init__(self, url, save_cookies=False):
        self.driver = webdriver.Chrome()
        self.pages_to_scrap = []
        self.last = 0
        self.number_page_scrapped = 0
        self.driver.get(url)
        time.sleep(5)
        if not save_cookies:
            cookies = pickle.load(open("cookies_immoweb.pkl", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            print('cookies loaded')
        self.change_page = False
        time.sleep(10)
        if save_cookies:
            time.sleep(5)
            pickle.dump(self.driver.get_cookies(), open("cookies_immoweb.pkl", "wb"))
            print('cookies ready')
        self.driver.maximize_window()
        print('ready')

    def start_research(self, xpath, research_sentence, pushbutton=None):
        current_url = self.driver.current_url
        elem = self.driver.find_element_by_xpath(xpath)
        elem.clear()
        elem.send_keys(research_sentence)
        elem.send_keys(Keys.RETURN)
        time.sleep(3)
        elem.send_keys(Keys.RETURN)
        time.sleep(3)
        if pushbutton!= None:
            button = self.driver.find_element_by_xpath(pushbutton)
            actions = ActionChains(self.driver)
            actions.move_to_element(elem)
            actions.key_down(Keys.LEFT_CONTROL)
            actions.click(elem)
            actions.perform()
        WebDriverWait(self.driver, 15).until(EC.url_changes(current_url))

    def get_number_pages(self, last_entry_location):
        my_soup = BeautifulSoup(self.driver.page_source, features="html.parser")
        links = my_soup.find_all(last_entry_location[0], last_entry_location[1])
        self.last = int(links[-1].get_text())

    def scrap_page(self, xpaths, next_page_xpath):
        for i in range(self.last):
            print('scrapping page ', i + 1)
            elements = []
            for xpath in xpaths:
                wait = WebDriverWait(self.driver, 60)
                elements_for_xpath = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
                # elements_for_xpath = self.driver.find_elements_by_xpath(xpath)
                elements += elements_for_xpath
            for j in range(len(elements)):
                elem = elements[j]
                windows_before = self.driver.window_handles
                actions = ActionChains(self.driver)
                actions.move_to_element(elem)
                actions.key_down(Keys.LEFT_CONTROL)
                actions.click(elem)
                actions.perform()
                WebDriverWait(self.driver, 20).until(EC.new_window_is_opened(windows_before))
                self.driver.switch_to.window(self.driver.window_handles[1])
                time.sleep(2 * random.random())
                source_page = self.driver.page_source
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                with open('data_immoweb.csv', 'a') as file:
                    file.write(scrap_page(source_page))
            self.next_page(next_page_xpath)
            # self.change_page=True
            # self.number_page_scrapped += 1

    def list_complete(self):
        return self.change_page

    def next_page(self, xpath):
        current_url = self.driver.current_url
        self.driver.maximize_window()
        wait = WebDriverWait(self.driver, 30)
        elem = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        actions = ActionChains(self.driver)
        actions.click(elem)
        actions.perform()
        time.sleep(10)
        # elem = self.driver.find_element_by_xpath(xpath)
        # actions = ActionChains(self.driver)
        # actions.click(elem)
        # actions.perform()
        WebDriverWait(self.driver, 15).until(EC.url_changes(current_url))
        self.change_page = False

    def research_completed(self):
        return self.number_page_scrapped == self.last

    def change_research(self, url):
        print('changing research')
        self.driver.get(url)
        time.sleep(5)

    def close(self):
        self.driver.quit()

if __name__=='__main__':

    def scrap_city(house_kind, city, postcode):
        url = "https://www.immoweb.be/fr/recherche/{}/a-vendre/{}/{}?countries=BE&orderBy=relevance".format(house_kind, city, postcode)
        my_scrapper.change_research(url)
        my_scrapper.get_number_pages(last_entry_location)
        my_scrapper.scrap_page(xpaths, next_page_xpath)



    arguments = ["Surface habitable", 'Surface du terrain', 'Chambres', 'Meublé', 'Type de cuisine',
                 'Surface du jardin', 'Terrasse', 'Surface de la terrasse', 'Nombre de façades',
                 'État du bâtiment', 'Combien de feux ouverts ?', 'Piscine', 'Salles de bains', 'Toilettes', 'Dressing',
                 'Cave', 'Bureau', "Salon", 'Parkings intérieurs',
                 'Parkings extérieurs', 'Salle à manger', 'Salles de douche', 'Buanderie', 'Année de construction']
    mot_cle = ["id", "transactionType", "type", "subtype", "zip", 'price']
    first_csv_line = ""
    for arg in arguments:
        first_csv_line += arg+','
    for mot in mot_cle:
        first_csv_line += mot + ','
    first_csv_line+='état\n'

    with open('data_immoweb.csv', 'w') as file:
        file.write(first_csv_line)
    my_scrapper = ImmoWebScrapping(
        'https://www.immoweb.be/fr/recherche/maison-et-appartement/a-vendre?countries=BE&page=1&orderBy=relevance')
    path_to_research_field = '//input[@placeholder="Entrez une ville ou un code postal"]'
    button_xpath = '//button[@id="searchBoxSubmitButton"]'  # <button id="searchBoxSubmitButton" type="submit" class="button button--primary"><span class="button__label">Rechercher</span></button>
    input_sentence = 'Mons'
    # my_scrapper.start_research(path_to_research_field, input_sentence)
    xpaths = ["//a[@class='card__title-link']"]
    last_entry_location = ('span', {'class': 'button__label'})
    next_page_xpath = "//a[@class='pagination__link pagination__link--next button button--text button--size-small']"
    my_scrapper.get_number_pages(last_entry_location)

    housing_types = ['maison', 'appartement']
    cities_data = pd.read_csv("post_codes.csv", sep=';')
    cities = list(cities_data.iloc[:, 1].str.lower()[::-1])
    postcodes = list(cities_data.iloc[:, 0].astype(str)[::-1])

    while True:
        for housing_type in housing_types:
            for city, postcode in zip(cities, postcodes):
                try:
                    scrap_city(housing_type, city, postcode)
                except:
                    print('error with ', city)
                    continue
                print(city, ' done')





