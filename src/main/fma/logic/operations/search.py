from src.main.fma.logic.item_service import item_service
from src.main.fma.controllers import yad_2_db


class search:
    def __init__(self):
        self.item_service = item_service()

    def search_apartment(self, item_id):
        item = self.item_service.get_specific_item(item_id)
        search_details = item["item_attributes"]
        price = search_details['price']
        num_of_rooms = search_details['num_of_rooms']
        location = search_details['location']
        street = location['street']
        neighbor = location['neighbor']
        city = location['city']
        square_meter = search_details['square_meter']
        apartments_entities = list(yad_2_db.find({
            '$and': [
                {'price': {
                    '$lt': price
                }},
                {'num_of_room': {
                    '$lt': num_of_rooms
                }},
                {'street': street},
                {'neighbor': neighbor},
                {'city': city},
                {'square_meter': {
                    '$lt': square_meter
                }}]}).sort("price", 1))
        print("In Search")
