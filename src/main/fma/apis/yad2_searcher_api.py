import logging
import requests
import re
from src.main.fma.controllers import yad_2_db

URL = "http://gw.yad2.co.il/feed-search-legacy/realestate/forsale?topArea=25&area=96&city=2800&forceLdLoad=true"
URL_PAGE = "https://gw.yad2.co.il/feed-search-legacy/realestate/forsale?page="


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

    def find_num_of_pages(self):
        r = requests.get(URL, headers=self.header).json()
        self.num_of_pages = int(r.get('data').get('pagination').get('last_page'))

    def search_apartments(self):
        self.find_num_of_pages()
        for i in range(self.num_of_pages):
            logging.info('###############################')
            logging.info("scanning page #" + str(i + 1))
            self.search_apartment_in_page(i + 1)

    def search_apartment_in_page(self, i):
        if i == 1:
            url = URL
        else:
            url = URL_PAGE + str(i)
        r = requests.get(url, headers=self.header).json()
        apartments_json = r.get('data').get('feed').get('feed_items')
        for apartment in apartments_json:
            if apartment.get('city') != 'קרית שמונה':
                continue
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
                'contract_phone': '0528614485'
                # self.find_phone_number(apartment.get('id'), apartment.get('is_platinum'))
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

    def find_phone_number(self, id, is_platinum):
        url_ext = "&isPlatinum=true"
        url = "https://www.yad2.co.il/api/item/" + id + "/contactinfo?id=" + id
        if is_platinum:
            url = url + url_ext
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Host": "www.yad2.co.il",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Referer":
                "https: //www.yad2.co.il / realestate / forsale?topArea = 25 & area = 96 & city = 2800",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
            "web-view": "true"
        }

        r = requests.get(url, headers=headers)
        print(r.text)
