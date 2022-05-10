import logging
import requests
import re
from src.main.fma.controllers import yad_2_db
import random

URL = "http://gw.yad2.co.il/feed-search-legacy/realestate/forsale?"
URL_PAGE = "https://gw.yad2.co.il/feed-search-legacy/realestate/forsale?page="
CITIES_ID = ["topArea=25&area=96&city=2800", "area=93&city=9200"]


class yad2_searcher_api:
    def __init__(self):
        self.apartments = []
        self.num_of_pages = 0
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            'referer': 'https://www.google.com/'
        }
        logging.basicConfig(filename="../logs/yad2_log.md", filemode='w',
                            format='%(asctime)s, %(msecs)d, %(name)s, %(levelname)s, %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)
        logging.info('###############################')
        logging.info('Initial yad2 api done')
        logging.info('###############################')

    def find_num_of_pages(self, city_id):
        r = requests.get(URL + city_id, headers=self.header).json()
        self.num_of_pages = int(r.get('data').get('pagination').get('last_page'))

    def search_apartments(self):
        for city in CITIES_ID:
            self.find_num_of_pages(city)
            for i in range(self.num_of_pages):
                logging.info('###############################')
                logging.info("scanning page #" + str(i + 1))
                self.search_apartment_in_page(i + 1, city)
            self.num_of_pages = 0

    def search_apartment_in_page(self, i, city_id):
        global r
        if i == 1:
            url = URL + city_id
        else:
            url = URL_PAGE + str(i)
        try:
            r = requests.get(url, headers=self.header).json()
        except requests.exceptions.RequestException as e:
            print(e)
        apartments_json = r.get('data').get('feed').get('feed_items')
        for apartment in apartments_json:
            if apartment.get('city') == 'קרית שמונה' or apartment.get('city') == 'בית שאן':
                tmp_apartment = {
                    'description': apartment.get('search_text'),
                    'price': self.find_price(apartment.get('price')),  # 1,400,000 ₪, #None, #לא צוין מחיר
                    'num_of_rooms': int(round(float(apartment.get('Rooms_text')))) if self.has_number(
                        apartment.get('Rooms_text')) else 0,
                    'floor': apartment.get('line_2'),
                    'street': apartment.get('street'),
                    'neighbor': apartment.get('neighborhood'),
                    'city': apartment.get('city'),
                    'square_meter': int(round(float(apartment.get('square_meters')))) if self.has_number(
                        apartment.get('square_meters')) else 0,
                    'date_of_uploaded': apartment.get('date_added'),
                    'pictures': apartment.get('images_urls'),
                    'contract_name': apartment.get('contact_name'),
                    'contract_phone':
                        self.find_phone_number(apartment.get('id'))
                }
                self.apartments.append(tmp_apartment)

    def data_manager(self):
        for apartment in self.apartments:
            yad_2_db.insert_one(apartment)

    def has_number(self, string):
        return bool(re.search(r'\d', str(string)))

    def find_price(self, price):
        if self.has_number(price):
            return int(price.replace('₪', '').replace(',', '').strip())
        return 0

    def find_phone_number(self, id):
        return '05' + str(random.randint(2, 4)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(
            random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(
            random.randint(0, 9)) + str(random.randint(0, 9))