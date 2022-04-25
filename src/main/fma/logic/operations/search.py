from src.main.fma.logic.item_service import item_service
from src.main.fma.controllers import yad_2_db, nadlan_gov_db


class search:
    def __init__(self):
        self.item_service = item_service()

    def search_previous_apartment_data(self, item_id):
        print("In Search Data")
        item = self.item_service.get_specific_item(item_id)
        search_details = item["item_attributes"]
        price = int(search_details['price'])
        num_of_rooms = int(search_details['num_of_rooms'])
        location = search_details['location']
        city = location['city']
        if city == 'קרית שמונה':
            city = 'קריית שמונה'
        street = location['street']
        square_meter = search_details['square_meter']
        query = [
            {'price_sold_asset': {
                '$lt': price
            }},
            {'asset_room_numbers': {
                '$lt': num_of_rooms
            }},
            {'city': {
                '$regex': city
            }},
            {'asset_size_in_meters': {
                '$lt': square_meter
            }}
        ]
        if street != '':
            query.append(
                {'street_and_number': {
                    '$regex': street
                }}
            )
        apartment_data = list(nadlan_gov_db.find({
            '$and': query}
        ).sort("price_sold_asset", 1))
        apartment_data = apartment_data[0:3]
        if apartment_data:
            return apartment_data
        return {}

    def search_apartment(self, item_id):
        print("In Search")
        item = self.item_service.get_specific_item(item_id)
        search_details = item["item_attributes"]
        price = int(search_details['price'])
        num_of_rooms = int(search_details['num_of_rooms'])
        location = search_details['location']
        street = location['street']
        city = location['city']
        square_meter = search_details['square_meter']
        query = [
            {'price': {
                '$lt': price
            }},
            {'num_of_rooms': {
                '$lt': num_of_rooms
            }},
            {'city': city},
            {'square_meter': {
                '$lt': square_meter
            }}]
        if street != '':
            query.append({
                'street': {'$regex': street}
            })
        ls = list(yad_2_db.find({
            '$and': query}).sort("price", 1))
        return ls
