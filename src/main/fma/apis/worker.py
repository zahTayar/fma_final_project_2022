from src.main.fma.apis.yad2_api import yad2_searcher


class worker():
    def __init__(self):
        self.searcher_yad_2 = yad2_searcher()
        self.sercher_nadlan =0

    def update_db(self):
        self.searcher_yad_2.search_in_yad2()
        # self.searcher.