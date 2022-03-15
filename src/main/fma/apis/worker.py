from src.main.fma.apis.yad2_searcher_api import yad2_searcher_api
from src.main.fma.apis.nadlangov import nadlangov
from src.main.fma.controllers import db


class worker:
    def __init__(self):
        self.yad2_searcher_api = yad2_searcher_api()
        self.searcher_nadlan = nadlangov()

    def update_db(self):
        # search for new data
        self.yad2_searcher_api.search_apartments()
        apartments_data = self.searcher_nadlan.search_all_town()
        # remove
        db.apartments.remove({})
        db.apartments_data.remove({})
        # import new data
        self.searcher_nadlan.data_manager(apartments_data)
        self.yad2_searcher_api.data_manager()
