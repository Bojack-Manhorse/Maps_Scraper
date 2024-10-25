from map_scraper import MapsScraper

if __name__ == "__main__":
    print("Starting Google Maps Scraper.")

    input("Press Enter to continue.")

    search_query = str(input('Please type the search query you wish to enter into google maps e.g. Barbers Soho.'))

    destination_file = search_query + '.json'

    limit = int(input("Please enter a maximum limit to the number of merchants scraped (Around 300 is a sensible limit)."))

    filter_string = str(input("Please enter a postcode you would like to filter for e.g. 'BA1' or 'BA'. Leave blank for no filter."))

    print(f'The search query you entered is "{search_query}"\n' +
            f'The results will be saved in the file "{destination_file}"\n' +
            f'The scraper will filter for results containing {filter_string} in the postcode \n' * (not filter_string == '') + 
            f'The the scraper will automatically terminate after it has scraped {limit} merchants.')

    input("Press Enter to continue.")

    scraper = MapsScraper()

    scraper.scrape_search_results(search_query, limit)
    scraper.crawl_all_links(limit)
    scraper.filter_postcode(filter_string)
    scraper.save_data_to_json(directory=destination_file)

    print("The scrape has been completed, you can now close the browser window.")