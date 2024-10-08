from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys

class MapsScraper:
    def __init__(self) -> None:
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(2)
        self.list_of_links = []
        self.list_of_data = []
        self.merchant_key = {
            'Address': '',
            'Booking link' : '',
            'Website': '',
            'Phone Number': '',
            'Opening Times': ''
        }
    
    def get_past_cookie_screen(self):
        # Get past cookie screen
        button_list = self.driver.find_elements(By.CLASS_NAME, 'VfPpkd-LgbsSe')
        if len(button_list) > 4 and button_list[4].text == 'Reject all':
            button_list[4].click()
        return
    
    def scrape_search_results(self, query:str):
        self.driver.get('https://www.google.co.uk/maps/')

        self.get_past_cookie_screen()

        # Find the search bar and enter the search query into it
        search_bar = self.driver.find_element(By.ID, 'searchboxinput')
        search_bar.send_keys(query)
        search_bar.send_keys(Keys.ENTER)

        # Get the section containing the search results
        section = self.driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')

        # Scroll down to the bottom of the results
        while len(self.driver.find_elements(By.CLASS_NAME, 'HlvSq')) == 0:
            section.send_keys(Keys.PAGE_DOWN)

            # Put a catch here to avoid an infinite loop

        # Get all the search results
        barber_link = self.driver.find_elements(By.CLASS_NAME, 'hfpxzc')
        
        # Get the links from each search result
        links = [item.get_attribute('href') for item in barber_link]

        self.driver.close()
        return links
    
    def set_list_of_links_to_crawl(self, query:str):
        self.list_of_links = self.scrape_search_results(query)

    def import_links_from_txt(self, file_path:str):
        with open(file_path, 'r') as file:
            data = file.read()
        self.list_of_links = data.split('\n') 
    
    def scrape_data_from_picture(self, picture_icon:str):
        try:
            picture_element = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{picture_icon}')]")[0]
            parent_element = picture_element.find_element(By.XPATH, "./../../..")
            result = parent_element.get_attribute('aria-label')
            result = result.split(': ')
            return result[-1]
        except:
            return 'None found.'

    def sort_opening_times(self, opening_string:str):
        opening_string = opening_string.replace("\u202f",  ' ')
        opening_string = opening_string.replace('. Hide opening hours for the week', '')
        opening_list = opening_string.split('; ')
        opening_list = [item.split(', ') for item in opening_list]
        opening_dict = {item[0]:item[1] for item in opening_list}
        return opening_dict      

    def crawl_individual_link(self, link:str):
        self.driver.get(link)
        self.get_past_cookie_screen()
        dict_of_results = {}

        name_header = self.driver.find_element(By.CLASS_NAME, 'DUwDvf')
        dict_of_results['Name'] = name_header.text

        for item in ['Address', 'Booking link', 'Website', 'Phone Number']:
            value = self.scrape_data_from_picture(self.merchant_key[item])
            dict_of_results[item] = value

        time_button = self.driver.find_elements(By.CLASS_NAME, 'puWIL')

        if len(time_button) > 0:
            time_button[0].click()
            opening_times = self.driver.find_elements(By.CLASS_NAME, 't39EBf')
            dict_of_results['Opening times'] = opening_times[0].get_attribute('aria-label')
            dict_of_results['Opening times'] = self.sort_opening_times(opening_times[0].get_attribute('aria-label'))
        else:
            dict_of_results['Opening times'] = 'None given'

        return dict_of_results
    
    def crawl_all_links(self, limit:int):
        if limit:
            self.list_of_data = [self.crawl_individual_link(link) for link in self.list_of_links if self.list_of_links.index(link) < limit]
        else:
            self.list_of_data = [self.crawl_individual_link(link) for link in self.list_of_links]
    
    def save_links_to_text_file(self, directory:str):
        with open(directory, 'w+') as file:
            for item in self.list_of_links:
                file.write(f'{item}\n')
