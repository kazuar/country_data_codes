
import bs4
import json
import requests
import argparse

BASE_URL = "https://en.wikipedia.org"
COUNTRY_CODES_URL = BASE_URL + "/wiki/Country_code"

def scrape_countries_details(url):
    # Get remote page
    response = requests.get(url)

    # Create soup object from page content
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    countries_data = []

    # Fetch all elements that holds country name
    country_names_elems = soup.findAll('span', 'mw-headline')

    # For each country element retrieve all the relevant data
    for country_name_elem in country_names_elems:
        # Find the next table element after country name while holds
        # the country's data
        country_table = country_name_elem.parent.findNext("table")
        if not country_table:
            continue

        # Fetch all the cells in the table
        tds = country_table.findAll("td")

        # Each cell holds the column name and the value 
        # so we can create a dict by reading each cell
        # with the column name as the key and the cell data as the value
        country_data = {td.find("a").text: td.find("span").text for td in tds}

        # Add the country name and wikipedia page url for the country
        country_a_elem = country_name_elem.find('a')
        country_data["country_name"] = country_a_elem.text.replace("\n", "").strip()
        country_data["country_url"] = BASE_URL + country_a_elem['href']
        countries_data.append(country_data)
    return countries_data

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output_file", dest = 'output_file', required = True)

    args = parser.parse_args()

    # Get page soup
    response = requests.get(COUNTRY_CODES_URL)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # Find countries urls
    all_countries_details = []
    countries_urls = [a_elem['href'] for a_elem in soup.findAll('a') if a_elem.attrs.get('href', '').startswith('/wiki/Country_codes')]
    for countries_url in countries_urls:
        countries_data = scrape_countries_details(BASE_URL + countries_url)
        all_countries_details.extend(countries_data)

    with open(args.output_file, "wb") as output_file:
        json.dump(all_countries_details, output_file)

if __name__ == '__main__':
    main()
