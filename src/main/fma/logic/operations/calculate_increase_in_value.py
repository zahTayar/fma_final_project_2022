from src.main.fma.controllers import nadlan_gov_db


class calculate_incrase_in_value:
    def __init__(self):
        pass
    def calculate_increase_in_value(self,asset_room_number,size_in_meters,location):
        all_years = {"2021":[],
                     "2020":[],
                     "2019":[],
                     "2018":[]}
        for key in all_years.keys():
            apartement_data = list(nadlan_gov_db.find({
            '$and': [
                {'street_and_number': {
                    '$regex': location["street"]
                }},
                {'asset_room_numbers':
                     asset_room_number
                 },
                {'year_deal':
                     key
                 },
                {'asset_size_in_meters': {
                    '$lt': (size_in_meters+15)
                }}
            ]}
        ))
            all_years[key]=apartement_data
        return self.calc(all_years)

    def calc(self,all_years):
        results_avarage={}
        for key in all_years.keys():
            list_of_apart = all_years[key]
            results_avarage[key]=0
            if(len(list_of_apart)>0):
                for item in list_of_apart:
                    results_avarage[key] += item["price_sold_asset"]
                results_avarage[key] = results_avarage[key] / len(list_of_apart)
        return results_avarage



