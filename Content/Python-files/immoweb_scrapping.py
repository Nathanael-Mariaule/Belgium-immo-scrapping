import time
from bs4 import BeautifulSoup
from immoweb_page_scrapping import scrap_page
import pandas as pd
import pickle
import random
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys




class ImmoWebScrapping:
    """"
        Class that scrap a page of immoweb using Selenium
        If the url is a page obtained using research engine from immoweb, it scrap throuhg all results and
        stock informations about each sale in a csv file

        Attributes:
            driver: the webdriver.Chrome() browser
            last: contains the number of pages of the research, update it with the get_number_pages() method
    """
    def __init__(self, url, save_cookies=False):
        """
            create an object ImmoWebScrapping. It initializes the browser, open the page url and save or load cookies
            :param url: the url address of the page as string
            :param save_cookies: bool it save cooke if True otherwise, it loads them
            :return: None
        """
        self.driver = webdriver.Chrome()
        self.last = 0
        self.driver.get(url)
        time.sleep(5)
        if not save_cookies:
            #open the cookies and load the in the browser
            cookies = pickle.load(open("cookies_immoweb.pkl", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            print('cookies loaded')
        time.sleep(10)
        if save_cookies:
            # save the cookies in a file
            time.sleep(5)
            pickle.dump(self.driver.get_cookies(), open("cookies_immoweb.pkl", "wb"))
            print('cookies ready')
        self.driver.maximize_window()
        print('ready')

    def get_number_pages(self, last_entry_location):
        """
            get the number of pages of a research on ImmoWeb and save it in self.last. If it fails, the value is set
            to 1
            :param last_entry_location: tuple with the tag and attributes values of the tag that contains the
                                        value of number page in the html code
            :return: None
        """
        try:
            my_soup = BeautifulSoup(self.driver.page_source, features="html.parser")
            links = my_soup.find_all(last_entry_location[0], last_entry_location[1])
            self.last = int(links[-1].get_text())
        except:
            self.last = 1

    def scrap_page(self, xpaths, next_page_xpath):
        """
            Scrap through all results of the research in the page and save informations about each sale in a csv file
            :param xpath: xpaths locations of the urls of the result on the current page
            :param next_page_xpath: xpath location of the button to the next page of result
        """
        for i in range(self.last):  #loop through all result pages
            print('scrapping page ', i + 1)
            elements = []
            for xpath in xpaths:  #get the positions of the urls to the result on the current page
                wait = WebDriverWait(self.driver, 60)  #launch exception if no result are found
                elements_for_xpath = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
                elements += elements_for_xpath
            for j in range(len(elements)):  #loop through all result on the current page
                elem = elements[j]
                windows_before = self.driver.window_handles
                actions = ActionChains(self.driver)
                actions.move_to_element(elem)
                actions.key_down(Keys.LEFT_CONTROL)
                actions.click(elem)
                actions.perform()   #open a new tab with the jth url in the list
                WebDriverWait(self.driver, 20).until(EC.new_window_is_opened(windows_before))
                self.driver.switch_to.window(self.driver.window_handles[1])  #change tab
                time.sleep(2 * random.random())
                source_page = self.driver.page_source  #get html code from the page
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0]) #close the tab and return to the main one
                with open('data_immoweb.csv', 'a') as file:
                    file.write(scrap_page(source_page))  #save infos in the csv file
            self.next_page(next_page_xpath)


    def next_page(self, xpath):
        """
            move from the current page in the research to the next one
            :param xpath: xpath location of the button next page
            :return: None
        """
        current_url = self.driver.current_url
        self.driver.maximize_window()
        wait = WebDriverWait(self.driver, 30)
        elem = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))  #look for the next page button
        actions = ActionChains(self.driver)
        actions.click(elem)
        actions.perform()  #click on the button
        time.sleep(10)
        WebDriverWait(self.driver, 15).until(EC.url_changes(current_url))  #wait for the new page to be loaded

    def change_research(self, url):
        """"
            the driver open the page url
            :param url: url of the page
            :return: None
        """
        print('changing research')
        self.driver.get(url)   #open the page
        time.sleep(5)

    def close(self):
        """
            close the driver
            :return: None
        """
        self.driver.quit()

if __name__=='__main__':
    # create the first line of the csv line
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
    #uncomment these if the csv file does not already exits
    #with open('data_immoweb.csv', 'w') as file:
    #    file.write(first_csv_line)

    #open a page on immoweb
    my_scrapper = ImmoWebScrapping(
        'https://www.immoweb.be/fr/recherche/maison-et-appartement/a-vendre?countries=BE&page=1&orderBy=relevance')

    #xpaths used in the algo
    xpaths = ["//a[@class='card__title-link']"]
    last_entry_location = ('span', {'class': 'button__label'})
    next_page_xpath = "//a[@class='pagination__link pagination__link--next button button--text button--size-small']"
    my_scrapper.get_number_pages(last_entry_location)

    #create the list of all research field used, here we do a research for all commune in Belgium and flat or house
    housing_types = ['appartement', 'maison']
    cities_data = pd.read_csv("post_codes.csv", sep=';')
    cities = list(cities_data.iloc[:, 1].str.lower())
    postcodes = list(cities_data.iloc[:, 0].astype(str))
    #loop through all research fields
    for city, postcode in zip(cities, postcodes):
        for housing_type in housing_types:
            try:
                url = "https://www.immoweb.be/fr/recherche/{}/a-vendre/{}/{}?countries=BE&orderBy=relevance".format(
                    housing_type, city, postcode)
                my_scrapper.change_research(url)  #load the page of the research
                my_scrapper.get_number_pages(last_entry_location) #get the number of pages in the result
                if my_scrapper.last == '333':
                    break   #if number of page is 333 then there are no special result for this commune and we skip
                my_scrapper.scrap_page(xpaths, next_page_xpath)  #scrap all sales for the research
            except:   #if an error occur we move to the next research
                print('error with ', city)
                continue
            print(city, ' done')




