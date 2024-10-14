from map_scraper import MapsScraper

if __name__ == "__main__":
    print("Starting Google Maps Scraper.")

    input("Press Enter to continue.")

    search_query = str(input('Please type the search query you wish to enter into google maps e.g. Barbers Soho.'))

    destination_file = search_query + '.json'

    limit = int(input("Please enter a maximum limit to the number of merchants scraped (Around 300 is a sensible limit)."))

    print(f'The search query you entered is "{search_query}" and the results will be saved in the file "{destination_file}", and the scraper will automatically terminate after it has scraped {limit} merchants.')

    input("Press Enter to continue.")

    scraper = MapsScraper()

    scraper.scrape_search_results(search_query, limit)
    scraper.crawl_all_links(limit)
    scraper.save_data_to_json(directory=destination_file)

    print("The scrape has been completed, you can now close the browser window.")