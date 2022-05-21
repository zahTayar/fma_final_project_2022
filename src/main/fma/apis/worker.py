from src.main.fma.apis.yad2_searcher_api import yad2_searcher_api
from src.main.fma.apis.nadlangov import nadlangov
from src.main.fma.controllers import db
from src.main.fma.apis.send_alert import send_alert

cities = ['בית שאן', 'קרית שמונה']


class worker:
    def __init__(self):
        self.yad2_searcher_api = yad2_searcher_api()
        self.searcher_nadlan = nadlangov()
        self.s = send_alert()

    def update_db(self):
        # search for new data
        self.yad2_searcher_api.search_apartments()
        # # remove
        db.apartments_data.remove({})
        for city in cities:
            apartments_data = self.searcher_nadlan.search_all_town(city)
            # # import new data
            self.searcher_nadlan.data_manager(apartments_data)
        # # remove
        db.apartments.remove({})
        # # import new data
        self.yad2_searcher_api.data_manager()
        # send alerts to users
        self.s.send_email_with_update()
