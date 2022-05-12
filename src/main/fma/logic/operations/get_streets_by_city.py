from src.main.fma.controllers import yad_2_db, nadlan_gov_db


class get_streets_by_city:

    def get_streets_by_city_of_apartments(self, city):
        query = [
            {'city': city}
        ]
        ls = list(yad_2_db.find({'$and': query}))
        rv = map(self.map_func_street, ls)
        return list(rv)


    def get_streets_by_city_of_apartments_data(self, city):
        pass

    def map_func_street(self, item):
        return item["street"]
