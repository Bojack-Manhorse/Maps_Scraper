from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys

import json
import math

class MapsScraper:
    """
    Class that scrapes results from google maps.
    """
    def __init__(self) -> None:
        """
        Initilise the webdriver and other necessary objects.
        """
        # The selenium webdriver that visits the pages.
        self.driver = webdriver.Firefox()
        
        # Set the driver to always wait 2 seconds before throwing an element not found error.
        self.driver.implicitly_wait(2)

        # Init the list of links to crawl as an empty list.
        self.list_of_links = []

        # Init the list of dictionaries of merchant data as an empty list.
        self.list_of_data = []

        # Keys corresponding to the icon google maps uses for the div element containing it's respective data points.
        self.merchant_key = {
            'Address': '',
            'Booking link' : '',
            'Website': '',
            'Phone Number': '',
            'Opening Times': ''
        }
    
    def get_past_cookie_screen(self):
        """
        Helper function to get past the cookie screen if there is one
        """
        
        # Locate the element corresponding to the reject all button.
        button_list = self.driver.find_elements(By.CLASS_NAME, 'VfPpkd-LgbsSe')

        # If the reject all button does exist, click it.
        if len(button_list) > 4 and button_list[4].text == 'Reject all':
            button_list[4].click()
        return
    
    def return_scrape_search_results(self, query:str, limit:int = math.inf):
        """
        Submits a query to the search box in google maps, and extracts the links of all the results.

        Args:
            query:str - The search query to enter
            limit:int - If more than this many links appear then stop
        
        Returns:
            links:list[str] - A list of all the extracted links
        """

        # Set the driver to the google maps homepage
        self.driver.get('https://www.google.co.uk/maps/')

        # Get past the cookie screen
        self.get_past_cookie_screen()

        # Find the search bar and enter the search query into it
        search_bar = self.driver.find_element(By.ID, 'searchboxinput')
        search_bar.send_keys(query)
        search_bar.send_keys(Keys.ENTER)

        # Get the section containing the search results
        section = self.driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')

        # Init the list of div elements corresponding to each merchant listed as an empty list.
        merchant_link = []

        # Scroll down to the bottom of the results.
        while len(self.driver.find_elements(By.CLASS_NAME, 'HlvSq')) == 0 and len(merchant_link) <= limit:
            section.send_keys(Keys.PAGE_DOWN)

            merchant_link = self.driver.find_elements(By.CLASS_NAME, 'hfpxzc')

            # Put a catch here to avoid an infinite loop.
        
        # Get the links from each merchant's div element.
        links = [item.get_attribute('href') for item in merchant_link]

        return links
    
    def scrape_search_results(self, query:str, limit:int = math.inf):
        """
        Sets 'self.list_of_links' to be the result from 'return_scrape_search_results'

        Args:
            query:str - The search query to enter
            limit:int - If more than this many links appear then stop
        """
        self.list_of_links = self.return_scrape_search_results(query, limit)
    
    def save_links_to_text_file(self, directory:str):
        """
        Save the items in 'self.list_of_links' to a txt file.

        Args:
            directory:str - The path of the file to save 'self.list_of_links' to.
        """
        with open(directory, 'w+') as file:
            for item in self.list_of_links:
                file.write(f'{item}\n')

    def import_links_from_text_file(self, file_path:str):
        """
        Import a list of links from a text file.

        Args:
            directory:str - The path of thefile to load into 'self.list_of_links'.
        """
        with open(file_path, 'r') as file:
            data = file.read()
        self.list_of_links = data.split('\n') 
    
    def scrape_data_from_picture(self, picture_icon:str):
        """
        Scrape the data from a div element contaning a partiuclar picture icon.

        Args:
            picture_icon:str - We seach for div elements containing that particular icon

        Returns:
            str - The 'aria-label' attribute of the 3rd level parent element of the element containing 'picture_icon'
        """

        # Attempt to seach for 'picture_icon'
        try:
            # Find all elements with 'picture_icon', there will be atmost one.
            picture_element = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{picture_icon}')]")[0]

            # Get the 3rd level parent element.
            parent_element = picture_element.find_element(By.XPATH, "./../../..")

            # Get it's 'aria-label' attribute.
            result = parent_element.get_attribute('aria-label')

            # If it's split via a colon (e.g Address: 123 Fake Street), then get everything after the colon.
            result = result.split(': ')
            return result[-1]
        
        # If any error, just return 'None found'
        except:
            return 'None found.'

    def sort_opening_times(self, opening_string:str):
        """
        Function to sort the opening times string google maps returns into a useful dictionary

        Args:
            opening_string:str - A string of the opening times google maps returns
        
        Returns:
            opening_dict:dict - A dict of the opening times for each day of the week.
        """

        # Get rid of unneccesary elements.
        opening_string = opening_string.replace("\u202f",  ' ')
        opening_string = opening_string.replace('. Hide opening hours for the week', '')

        # Opening times of different days are split by a semi-colon e.g. Monday, 1am - 2am; Tuesday, 2am - 3am.
        opening_list = opening_string.split('; ')

        # Make the list of the format [['Monday', '1am - 7am'], ...]
        opening_list = [item.split(', ') for item in opening_list]

        # Turn opening list into a dictionary of the form {'Monday: '1am - 6am, ...}
        opening_dict = {item[0]:item[1] for item in opening_list}
        return opening_dict      

    def crawl_individual_link(self, link:str):
        """
        Get's an individual merchant's information from its link.

        Args:
            link:str - The google maps link of the marchant.
        
        Returns:
            dict_of_results:dict - A dictionary containing the merchants information.
        """

        # Set the driver to the merchants page.
        self.driver.get(link)

        # Get past the cookie screen.
        self.get_past_cookie_screen()

        # Init the results as an empty dictionary
        dict_of_results = {}

        # Get the name of the marchant
        name_header = self.driver.find_element(By.CLASS_NAME, 'DUwDvf')
        dict_of_results['Name'] = name_header.text

        # Get the Address, Booking link, website and phone number via 'scrape_data_from_picture'
        for item in ['Address', 'Booking link', 'Website', 'Phone Number']:
            value = self.scrape_data_from_picture(self.merchant_key[item])
            dict_of_results[item] = value

        # Get the element containing the opening times.
        time_button = self.driver.find_elements(By.CLASS_NAME, 'puWIL')

        # If the opening times exist, click the button so they are shown.
        try:
            time_button[0].click()

            opening_times = self.driver.find_elements(By.CLASS_NAME, 't39EBf')

            # Get the string containing the opening times.
            dict_of_results['Opening times'] = opening_times[0].get_attribute('aria-label')

            # Sort it via 'sort_opening_times'.
            dict_of_results['Opening times'] = self.sort_opening_times(opening_times[0].get_attribute('aria-label'))
        
        # If opening times do not exist, return 'None given'.
        except:
            dict_of_results['Opening times'] = 'None given'

        return dict_of_results

    def return_crawl_all_links(self, limit:int = math.inf):
        """
        Crawls all the links within 'self.list_of_links' using the 'crawl_individual_link' method.

        Args:
            limit:int - After how many merchants should the scraper stop.
        
        Returns:
            list - List of dictionaries containing the details of each merchant.
        """
        result = []
        for link in self.list_of_links:
            try:
                data = self.crawl_individual_link(link)
                result.append(data)
            except:
                pass
            if len(result) > limit:
                break
        return result

    def crawl_all_links(self, limit:int = math.inf):
        """
        Sets 'self.list_of_data' to be the results of return_crawl_all_links.

        Args:
            limit:int - After how many merchants should the scraper stop.
        """
        self.list_of_data = self.return_crawl_all_links(limit)
    
    def save_data_to_json(self, directory:str):
        """
        Saves 'self.list_of_data' to a json.

        Args:
            directory:str - Path of file to save within.
        """
        with open(directory, 'w') as file:
            json.dump(self.list_of_data, file, indent=2)
    

