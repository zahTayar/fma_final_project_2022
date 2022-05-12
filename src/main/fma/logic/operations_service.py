from src.main.fma.controllers import operations_db
from src.main.fma.boundaries.operation_boundary import operation_boundary
from src.main.fma.helpers.checker_authorization import checker_authorization
from src.main.fma.logic.operations.search import search
from src.main.fma.logic.operations.calculate_increase_in_value import calculate_incrase_in_value
from src.main.fma.data.operation_entity import operation_entity
from src.main.fma.logic.operations.get_streets_by_city import get_streets_by_city
import pymongo.errors as mongodb_errors
from datetime import datetime
import uuid


# object  invokeOperation (operationBoundary)
# operationBoundary  invokeAsyncOperation (operationBoundary)
# List <operationBoundary> getAllOperations (adminEmail)
# void deleteAllOperations (adminEmail)

class operations_service:
    def __init__(self):
        self.search = search()
        self.calculate_increase_in_value = calculate_incrase_in_value()
        self.checker_authorization = checker_authorization()
        self.get_streets_by_city = get_streets_by_city()

    def invoke_operation(self, boundary):
        entity = self.convert_boundary_to_entity(boundary)
        entity.set_operation_id(str(uuid.uuid4()))
        operations_db.insert(entity.__dict__)

        if boundary.get_type() == 'search':
            lst = self.search.search_apartment(boundary.get_operation_attributes()["item_id"])
            result = {}
            if not lst:
                return {}
            for apa in lst:
                js = self.convert_apartment(apa)
                result[str(lst.index(apa))] = js
            print(result)
            return result

        if boundary.get_type() == 'streets_by_city_apartments':
            lst = self.get_streets_by_city.get_streets_by_city_of_apartments(boundary.get_operation_attributes()["city"])
            if not lst:
                return {}
            return {'0': lst}

        if boundary.get_type() == 'search_apartments_data':
            lst = self.search.search_previous_apartment_data(boundary.get_operation_attributes()["item_id"])
            if not lst:
                return {}
            result = {}
            for apa in lst:
                js = self.convert_data_apartment(apa)
                result[str(lst.index(apa))] = js
            print(result)
            return result

        if boundary.get_type() == 'calculate_increase_in_value':
            return self.calculate_increase_in_value.calculate_increase_in_value(
                boundary.get_operation_attributes()["asset_room_numebers"],
                boundary.get_operation_attributes()["asset_size_in_meters"],
                boundary.get_operation_attributes()["location"])

    def convert_apartment(self, apartment):
        rv = {'description': apartment['description'], 'price': apartment['price'],
              'num_of_rooms': apartment['num_of_rooms'], 'floor': apartment['floor'],
              'street': apartment['street'],
              'neighbor': apartment['neighbor'], 'city': apartment['city'],
              'square_meter': apartment['square_meter'],
              'date_of_uploaded': apartment['date_of_uploaded'], 'pictures': apartment['pictures'],
              'contract_name': apartment['contract_name'], 'contract_phone': apartment['contract_phone']}
        return rv

    def convert_data_apartment(self, apartment):
        rv = {'full_address': apartment['full_address'], 'street_and_number': apartment['street_and_number'],
              'deal_description': apartment['deal_description'], 'asset_room_numbers': apartment['asset_room_numbers'],
              'asset_size_in_meters': apartment['asset_size_in_meters'],
              'price_sold_asset': apartment['price_sold_asset'], 'date_deal': apartment['date_deal'],
              'year_building_build': apartment['year_building_build']}
        return rv

    def invoke_async_operation(self, boundary):
        return None

    def convert_boundary_to_entity(self, boundary):
        entity = operation_entity()
        entity.set_type(boundary.get_type())
        entity.set_operation_attributes(boundary.get_operation_attributes())
        entity.set_invoked_by(boundary.get_invoked_by())
        entity.set_created_timestamp(datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
        return entity

    def convert_entity_to_boundary(self, entity):
        boundary = operation_boundary()
        boundary.set_operation_id(entity.get_operation_id())
        boundary.set_type(entity.get_type())
        boundary.set_operation_attributes(entity.get_operation_attributes())
        boundary.set_invoked_by(entity.get_invoked_by())
        boundary.set_created_timestamp(entity.get_created_timestamp())
        return boundary

    def get_all_operations(self, admin_email):
        # check auth of admin_email
        if not self.checker_authorization.check_admin_user(admin_email):
            raise RuntimeError("not authorized to act this operation")
        operations = []
        entities = []
        try:
            entities = operations_db.find()
        except mongodb_errors:
            print(str(mongodb_errors))
        for rv in entities:
            operations.append(
                operation_boundary(rv['operation_id'], rv['type'], rv['invoked_by'], rv['created_timestamp'],
                                   rv['operation_attributes']))
        my_dict = dict()
        for index, value in enumerate(operations):
            my_dict[index] = value.__dict__
        return my_dict

    def delete_all_operation(self, admin_email):
        # check auth of admin_email
        if not self.checker_authorization.check_admin_user(admin_email):
            raise RuntimeError("not authorized to act this operation")
        x = []
        try:
            x = operations_db.delete_many({})
        except mongodb_errors:
            print(str(mongodb_errors))
        print(x.deleted_count, " documents deleted.")
