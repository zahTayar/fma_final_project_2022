from src.main.fma.apis.yad2_api import yad2_searcher
from src.main.fma.apis.nadlangov import nadlangov
from src.main.fma.controllers import db


class worker:
    def __init__(self):
        #self.searcher_yad_2 = yad2_searcher()
        self.searcher_nadlan = nadlangov()

    def update_db(self):
        # search for new data
        #self.searcher_yad_2.search_in_yad2()
        apartments_data = self.searcher_nadlan.search_all_town()
        # remove
        db.apartments.remove({})
        db.apartments_data.remove({})
        # import new data
        self.searcher_nadlan.data_manager(apartments_data)
        #self.searcher_yad_2.data_manager()
