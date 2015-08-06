
import re
import bs4
import json
import requests
import argparse

BASE_URL = "https://countrycode.org/"

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output_file", dest = 'output_file', required = True)

    args = parser.parse_args()

    # Get page soup
    response = requests.get(BASE_URL)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # Find country code table
    country_code_tables = soup.findAll('table', {"class" : "table table-hover table-striped main-table"})
    if not country_code_tables:
        print "Failed to find country codes table"
        return 

    # Use the first country code table that was found 
    # (there supposed to be 2 tables in the HTML - one for browser and one for mobile)
    country_code_table = country_code_tables[0]

    # Get column names
    column_names = [th.text.replace("\n", "").strip() for th in country_code_table.find_all("th")]

    # Get the body of the table
    tbody = country_code_table.find("tbody")

    all_countries_data = []
    for tr in tbody.find_all("tr"):
        country_values = [td.text.replace("\n", "").strip() for td in tr.find_all("td")]
        country_data = dict(zip(column_names, country_values))
        all_countries_data.append(country_data)

    with open(args.output_file, "wb") as output_file:
        json.dump(all_countries_data, output_file)

if __name__ == '__main__':
    main()