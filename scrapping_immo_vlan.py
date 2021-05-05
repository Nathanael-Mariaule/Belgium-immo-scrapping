from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from page_scrapping import b_soup_immo
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import pickle
import random

class ImmoVlanScrapping:
    def __init__(self, url, save_cookies=False):
        options = Options()
        ua = UserAgent()
        options.add_argument(f'user-agent={ua}')
        userAgent = ua.random
        self.driver = webdriver.Chrome(chrome_options=options)
        #self.driver = webdriver.Chrome()
        self.pages_to_scrap = []
        self.last = 167
        self.number_page_scrapped = 0
        self.driver.get(url)
        if not save_cookies:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
        self.change_page = False
        time.sleep(5)
        if save_cookies:
            time.sleep(120)
            pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
            print('cookies ready')
        print('ready')

    def start_research(self, xpath, research_sentence):
        current_url = self.driver.current_url
        elem = self.driver.find_element_by_xpath(xpath)
        elem.clear()
        elem.send_keys(research_sentence)
        elem.send_keys(Keys.RETURN)
        WebDriverWait(self.driver, 15).until(EC.url_changes(current_url))

    def get_number_pages(self, last_entry_location):
        my_soup = BeautifulSoup(self.driver.page_source, features="html.parser")
        links = my_soup.find_all(last_entry_location[0], last_entry_location[1])
        self.last = 0
        for i in range(len(links)):
            if links[i].get('title') == 'suivant':
                self.last = int(links[i - 1].get_text())
        print(self.last, 'page to scrap')

    def scrap_page2(self, xpaths, next_page_xpath):
        for i in range(self.last):
            print('scrapping page ', i + 1)
            elements = []
            for xpath in xpaths:
                wait = WebDriverWait(self.driver, 60)
                elements_for_xpath = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
                #elements_for_xpath = self.driver.find_elements_by_xpath(xpath)
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
                source_page = self.driver.page_source
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                yield source_page
            self.next_page(next_page_xpath)
            #self.change_page=True
            #self.number_page_scrapped += 1

    def list_complete(self):
        return self.change_page

    def next_page(self, xpath):
        current_url = self.driver.current_url
        elem = self.driver.find_element_by_xpath(xpath)
        actions = ActionChains(self.driver)
        actions.click(elem)
        actions.perform()
        time.sleep(10)
        #elem = self.driver.find_element_by_xpath(xpath)
        #actions = ActionChains(self.driver)
        #actions.click(elem)
        #actions.perform()
        WebDriverWait(self.driver, 15).until(EC.url_changes(current_url))
        self.change_page=False

    def next_page2(self, xpath):
        print('change page')
        driver = self.driver
        time.sleep(5)
        elem = driver.find_element_by_xpath("//i[@class='fa fa-angle-right']")
        actions = ActionChains(driver)
        actions.click(elem)
        actions.perform()
        time.sleep(5)
        #elem = driver.find_element_by_xpath("//i[@class='fa fa-angle-right']")
        #actions = ActionChains(driver)
        #actions.click(elem)
        #actions.perform()
        #time.sleep(5)
        print('done')


    def research_completed(self):
        return self.number_page_scrapped == self.last

    def close(self):
        self.driver.quit()

    def scrap_page(self, xpaths, next_page_xpath):
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
            time.sleep(2*random.random())
            source_page = self.driver.page_source
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            yield source_page
        self.next_page(next_page_xpath)
        # self.change_page=True
        # self.number_page_scrapped += 1









if __name__=='__main__':

    with open('data_vlan.csv', 'w') as file:
        file.write("adid, bedrooms, city, price, transaction_type, subtype, "
                   "zipcode, adresse, surface, type_prop, etat, facades, surface_terrain, garden, "
                   "garden_surface, terrasse, terrasse_surface, piscine, nombre_chambres, garage, surface_habitable, "
                   "meuble, salles_de_bain, toilettes, cuisine_equipee, cheminee\n")


    path_to_research_field = "//input[@placeholder='Où ? Ville, Code Postal, Province ou Région.']"
    input_sentence = '8000'
    #my_scrapper.start_research(path_to_research_field, input_sentence)
    xpaths_flat = "//h2[@class='card-title text-ellipsis mb-1 d-inline with-small-icon appartment']"
    xpath_house = "//h2[@class='card-title text-ellipsis mb-1 d-inline with-small-icon house']"
    xpaths =[xpaths_flat, xpath_house]
    last_entry_location = ('a', {'rel': 'nofollow'})
    next_page_xpath = "//i[@class='fa fa-angle-right']"
    #print('compute number of page')
    #my_scrapper.get_number_pages(last_entry_location)
    my_scrapper = ImmoVlanScrapping("https://immo.vlan.be/fr", False)
    my_scrapper.close()
    for i in range(10, 168):
        url_flat = "https://immo.vlan.be/fr/immobilier/appartement?transactiontypes=a-vendre,en-vente-publique&propertysubtypes=appartement,rez-de-chaussee,penthouse,duplex,studio,loft,triplex&countries=belgique&pageOffset={}&noindex=1".format(i)
        url_house = "https://immo.vlan.be/fr/immobilier/maison?transactiontypes=a-vendre,en-vente-publique&propertysubtypes=maison,villa,immeuble-mixte,maison-de-maitre,fermette,bungalow,chalet,chateau&countries=belgique&pageOffset={}&noindex=1".format(i)
        urls = [url_flat, url_house]
        print('scrapping page ', i)
        for index in [0, 1]:
            scrapper = ImmoVlanScrapping(urls[index])
            for html_page in scrapper.scrap_page([xpaths[index]], next_page_xpath):
                try:
                    with open('data_vlan.csv', 'a') as file:
                        file.write(b_soup_immo(html_page) + "\n")
                except:
                    continue
            scrapper.close()
