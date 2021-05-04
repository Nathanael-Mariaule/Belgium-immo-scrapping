from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

class ImmoScrapping:
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.pages_to_scrap = []
        self.last = 0
        self.number_page_scrapped = 0
        self.driver.get(url)
        time.sleep(10)
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

    def scrap_page(self, xpaths):
        print('scrapping page ', self.number_page_scrapped+1)
        for i in range(self.last):
            elements = []
            for xpath in xpaths:
                elements_for_xpath = self.driver.find_elements_by_xpath(xpath)
                elements += elements_for_xpath
            for i in range(len(elements)):
                elem = elements[i]
                windows_before = self.driver.window_handles
                actions = ActionChains(self.driver)
                actions.move_to_element(elem)
                actions.key_down(Keys.LEFT_CONTROL)
                actions.click(elem)
                actions.perform()
                WebDriverWait(self.driver, 20).until(EC.new_window_is_opened(windows_before))
                self.driver.switch_to.window(self.driver.window_handles[1])
                source_page = self.driver.page_source
                source_pages_url = self.driver.current_url
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                yield source_page
        self.number_page_scrapped += 1

    def next_page(self, xpath):
        if self.number_page_scrapped == self.last:
            return False
        current_url = self.driver.current_url
        elem = self.driver.find_element_by_xpath(xpath)
        actions = ActionChains(self.driver)
        actions.click(elem)
        actions.perform()
        WebDriverWait(self.driver, 15).until(EC.url_changes(current_url))
        return True
















if __name__=='__main__':
    url='https://immo.vlan.be/fr'
    print('ready')
    source_pages = []  # contains the html
    source_pages_url = []
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(url)
    time.sleep(7)
 #try:
    ##elem = driver.find_element_by_xpath("//input[@placeholder='Où ? Ville, Code Postal, Province ou Région.']")
     #elemn = WebDriverWait(driver, 1000).until(
     #   EC.presence_of_all_elements_located((By.XPATH, "//input[@placeholder='Où ? Ville, Code Postal, Province ou Région.']")))
#except:
     #print('error')
    elem = driver.find_element_by_xpath("//input[@placeholder='Où ? Ville, Code Postal, Province ou Région.']")
    elem.clear()
    elem.send_keys("8000")
    elem.send_keys(Keys.RETURN)
    time.sleep(7)
    my_soup=BeautifulSoup(driver.page_source)
    links = my_soup.find_all('a', attrs = {'rel':'nofollow'})
    last = 0
    for i in range(len(links)):
        if links[i].get('title') == 'suivant':
            last = int(links[i - 1].get_text())
    print(last)
    for i in range(last):
        xpath_flat = "//h2[@class='card-title text-ellipsis mb-1 d-inline with-small-icon appartment']"
        xpath_house = "//h2[@class='card-title text-ellipsis mb-1 d-inline with-small-icon house']"
        elements_house = driver.find_elements_by_xpath(xpath_house)
        elements_flat = driver.find_elements_by_xpath(xpath_flat)

        elements = elements_flat + elements_house

        print(len(elements))
        for i in range(len(elements)):
            elem = elements[i]
            actions = ActionChains(driver)
            actions.move_to_element(elem)
            actions.key_down(Keys.LEFT_CONTROL)
            actions.click(elem)
            actions.perform()
            time.sleep(3)
            driver.switch_to.window(driver.window_handles[1])
            source_pages.append(driver.page_source)
            source_pages_url.append(driver.current_url)
            driver.close()
            # add_to_csv(source_pages[-1])
            driver.switch_to.window(driver.window_handles[0])
        time.sleep(5)
        elem = driver.find_element_by_xpath("//i[@class='fa fa-angle-right']")
        actions = ActionChains(driver)
        actions.click(elem)
        actions.perform()
        time.sleep(5)
        elem = driver.find_element_by_xpath("//i[@class='fa fa-angle-right']")
        actions = ActionChains(driver)
        actions.click(elem)
        actions.perform()
        time.sleep(5)

    driver.close()