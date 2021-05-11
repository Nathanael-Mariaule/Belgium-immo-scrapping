from threading import Thread
from immoweb_scrapping import ImmoWebScrapping
import pandas as pd
import os


class ThreadScrapping(Thread):
    """
        class that create a thread scrapping immoweb with the class ImmoWebScrapping
    """
    def __init__(self, scrapper, url, research_list, xpaths, next_page_xpath, last_entry_location):
        """
            create an object ThreadScrapping
            :param scrapper: an object ImmoWebScrapping
            :param url: the url of a research on immoweb with city name, zip code and building type as parameters to be
                        formatted
            :param research_list: list of uple the first coordinate a  tuple with cities and zip code names that will be
                                    scrapp on this thread, the second coordinate are the building type
            :param xpaths locations of the urls of the result on the current page
            :param next_page_xpath: xpath location of the button to the next page of result
            :param last_entry_location: tuple with the tag and attributes values of the tag that contains the
                                        value of number page in the html code
            :return: None
        """
        Thread.__init__(self)
        self.scrapper = scrapper
        self.url = url
        self.research_list = research_list
        self.xpaths = xpaths
        self.next_page_xpath = next_page_xpath
        self.last_entry_location = last_entry_location

    def run(self):
        """
            thread that loops trough all cities and building type in self.research_list, scrap the results on immoweb
            and store them in a csv file
        """
        # loop through all research fields
        for city, postcode in self.research_list[0]:
            for housing_type in self.research_list[1]:
                try:
                    current_url =self.url.format(housing_type, city, postcode)
                    self.scrapper.change_research(current_url)  # load the page of the research
                    self.scrapper.get_number_pages(self.last_entry_location)  # get the number of pages in the result
                    if self.scrapper.last == 333:
                        break  # if number of page is 333 then there are no special results for this commune and we skip
                    self.scrapper.scrap_page(self.xpaths, self.next_page_xpath)  # scrap all sales for the research
                except:  # if an error occur we move to the next research
                    #print('error with ', city)
                    continue
                print(city, postcode, ' done')
        self.scrapper.close()






if __name__=='__main__':
    number_thread = 10
    # xpaths used in the algo
    xpaths = ["//a[@class='card__title-link']"]
    last_entry_location = ('span', {'class': 'button__label'})
    next_page_xpath = "//a[@class='pagination__link pagination__link--next button button--text button--size-small']"
    cookie_xpath = '//div[@class="uc-btn-accept-wrapper"]'

    # create the list of all research field used, here we do a research for all commune in Belgium and flat or house
    housing_types = ['appartement', 'maison']
    cities_data = pd.read_csv("post_codes.csv", sep=';')
    cities = list(cities_data.iloc[:, 1].str.lower())
    postcodes = list(cities_data.iloc[:, 0].astype(str))
    size = len(cities)
    url = "https://www.immoweb.be/fr/recherche/{}/a-vendre/{}/{}?countries=BE&orderBy=relevance"
    threads = []
    for i in range(number_thread):
        filename = 'immoweb_data_part{}.csv'.format(i)
        # split the list into number_thread parts
        current_cities = cities[i * (size // number_thread):(i + 1) * (size // number_thread)]
        current_postcodes = postcodes[i * (size // number_thread):(i + 1) * (size // number_thread)]
        #instanciate the scrapper
        my_scrapper = ImmoWebScrapping(
            'https://www.immoweb.be/fr/recherche/maison-et-appartement/a-vendre?countries=BE&page=1&orderBy=relevance',
            filename, cookie_xpath)
        my_scrapper.get_number_pages(last_entry_location)
        research_list = (zip(current_cities, current_postcodes), housing_types)  #create the list of research to be scrap
        thread = ThreadScrapping(my_scrapper, url, research_list, xpaths, next_page_xpath, last_entry_location)
        thread.start()  #launch scrapping
        threads.append(thread)
    if size%number_thread !=0:  #we create a new thread to scrap the remaining cities if necessary
        filename = 'immoweb_data_part{}.csv'.format(number_thread)
        current_cities = cities[number_thread * (size // number_thread):]
        current_postcodes = postcodes[number_thread * (size // number_thread):]
        my_scrapper = ImmoWebScrapping(
            'https://www.immoweb.be/fr/recherche/maison-et-appartement/a-vendre?countries=BE&page=1&orderBy=relevance',
            filename, cookie_xpath)
        my_scrapper.get_number_pages(last_entry_location)
        research_list = (zip(current_cities, current_postcodes), housing_types)
        thread = ThreadScrapping(my_scrapper, url, research_list, xpaths, next_page_xpath, last_entry_location)
        thread.start()
        threads.append(thread)

    #stop the algo until the scrapping is done
    for thread in threads:
        thread.join()

    #group all csv file into one
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
    print('Grouping files')
    columns_name = arguments+mot_cle+['état']
    final_csv = pd.DataFrame(columns=columns_name)
    for i in range(number_thread):
        filename = 'immoweb_data_part{}.csv'.format(i)
        try:
            datas = pd.read_csv(filename, header=None)
            datas.columns = columns_name
            final_csv = pd.concat([final_csv, datas])
            os.remove(filename)
        except:
            continue
    final_csv.to_csv('data_immoweb.csv', index=False)





