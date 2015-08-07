
import json
from collections import defaultdict

class CountryDataCodes(object):
    def __init__(self, input_file_path):
        self._countries_data = []
        with open(input_file_path, "rb") as input_file:
            self._countries_data = json.load(input_file)
        self._set_countries_data()

    def _set_countries_data(self):
        self._countries_data = {country_data["country_name"].lower(): country_data for country_data in self._countries_data}
        self._alpha_two_to_country_name = {}
        self._alpha_three_to_country_name = {}
        for country_name, country_data in self._countries_data.items():
            alpha_two = country_data['ISO 3166-1 alpha-2']
            alpha_three = country_data['ISO 3166-1 alpha-3']
            self._alpha_two_to_country_name[alpha_two.lower()] = country_name
            self._alpha_three_to_country_name[alpha_three.lower()] = country_name

    def get_country_details(self, value):
        value = value.lower().strip()
        if len(value) == 2:
            country_name = self._alpha_two_to_country_name.get(value, None)
        elif len(value) == 3:
            country_name = self._alpha_three_to_country_name.get(value, None)
        else:
            country_name = value
        country_data = self._countries_data.get(country_name)
        return country_data

    def get_country_name(self, value):
        country_data = self.get_country_details(value)
        return country_data["country_name"]

