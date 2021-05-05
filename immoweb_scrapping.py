
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup


class ImmoWebScrapping:
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.pages_to_scrap = []
        self.last = 0
        self.number_page_scrapped = 0
        self.driver.get(url)
        self.change_page = False
        time.sleep(10)
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
            print(len(elements), elements)
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
                source_page = self.driver.page_source
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                yield source_page
            self.next_page(next_page_xpath)
            # self.change_page=True
            # self.number_page_scrapped += 1

    def list_complete(self):
        return self.change_page

    def next_page(self, xpath):
        current_url = self.driver.current_url
        self.driver.maximize_window()
        wait = WebDriverWait(self.driver, 60)
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

    def close(self):
        self.driver.quit()

if __name__=='__main__':
    with open('data.csv', 'w') as file:
     file.write("adid, bedrooms, city, price, transaction_type, subtype, "
               "zipcode, adresse, surface, type_prop, etat, facades, surface_terrain, garden, "
               "garden_surface, terrasse, terrasse_surface, piscine, nombre_chambres, garage, surface_habitable, "
               "meuble, salles_de_bain, toilettes, cuisine_equipee, cheminee\n")

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
    while True:
        for html_page in my_scrapper.scrap_page(xpaths, next_page_xpath):
            with open('data.csv', 'a') as file:
                my_soup = BeautifulSoup(html_page, features="html.parser")
                #b_soup_immo(html_page)
                file.write(my_soup.find('title').string)


