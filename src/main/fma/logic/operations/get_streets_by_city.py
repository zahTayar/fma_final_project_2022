from src.main.fma.controllers import yad_2_db, nadlan_gov_db
import re


class get_streets_by_city:

    def get_streets_by_city_of_apartments(self, city):
        query = [
            {'city': city}
        ]
        ls = list(yad_2_db.find({'$and': query}))
        rv = map(self.map_func_street, ls)
        return list(rv)

    def get_streets_by_city_of_apartments_data(self, city):
        if city == 'קרית שמונה':
            city = 'קריית שמונה'
        query = [
            {'city': {
                '$regex': city
            }}
        ]
        ls = list(nadlan_gov_db.find({'$and': query}))
        rv = map(self.map_func_street_data, ls)
        return list(rv)

    def map_func_street(self, item):
        return item["street"]

    def map_func_street_data(self, item):
        return item["street_and_number"]
