import logging
import requests
import re
from src.main.fma.controllers import yad_2_db
from selenium import webdriver

URL = "http://gw.yad2.co.il/feed-search-legacy/realestate/forsale?topArea=25&area=96&city=2800&forceLdLoad=true"
URL_PAGE = "https://gw.yad2.co.il/feed-search-legacy/realestate/forsale?page="


class yad2_searcher_api:
    def __init__(self):
        self.apartments = []
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--disable-extensions')
        # chrome_options.add_argument('--profile-directory=Default')
        # chrome_options.add_argument("--disable-plugins-discovery")
        # chrome_options.add_argument("--start-maximized")
        # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # chrome_options.add_experimental_option('useAutomationExtension', False)
        # self.driver = webdriver.Chrome('C:\\Users\\User\\Desktop\\chromedriver.exe', options=chrome_options)
        # self.driver.delete_all_cookies()
        # self.driver.set_window_size(800, 800)
        # self.driver.set_window_position(0, 0)
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
        global r
        if i == 1:
            url = URL
        else:
            url = URL_PAGE + str(i)
        try:
            r = requests.get(url, headers=self.header).json()
        except requests.exceptions.RequestException as e:
            print(e)
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
        url = "https://www.yad2.co.il/api/item/" + id + "/contactinfo?id=" + id
        # headers = {
        #     "Host": "www.yad2.co.il",
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        #     "Accept-Encoding": "gzip, deflate, br",
        #     "Accept-Language": "en-US,en;q=0.5",
        #     "Connection": "keep-alive",
        #     "Cookie": "__uzma=820c8a13-7e81-4b1b-bf45-0a7a8fae74d5; __uzmb=1636235304; __uzmc=2942235842622; __uzmd=1647959998; __uzme=3495; rdw_storereferer=; __ssds=3; __ssuzjsr3=a9be0cd8e; _ga=GA1.3.1133966222.1636235311; y2018-2-cohort=57; leadSaleRentFree=14; _ga_GQ385NHRG1=GS1.1.1647959656.10.1.1647959837.0; _hjid=946beedd-e73e-4565-a702-3bd5d2d6eefc; __gads=ID=4a1d47e507223768:T=1636235310:S=ALNI_MbvZJ9bvU6ywrDT1jvf3zknZat6vw; bc.visitor_token=6862868333773389824; __uzmf=7f600081020e40-4c24-416b-8aa7-7ea86e56c6561647333975311626022953-d49475ae84c685f4199; abTestKey=25; use_elastic_search=1; recommendations-searched-2=1; recommendations-home-category={""categoryId"":2,""subCategoryId"":1}; _pxvid=627601f9-a43c-11ec-8b67-6e7366477365; __uzmaj3=7f9b2b41-c29c-4d21-8b02-4c275c2fb76b; __uzmbj3=1647333980; __uzmcj3=622094692811; __uzmdj3=1647959794; _fbp=fb.2.1647333980771.1906411023; _gaexp=GAX1.3.H-vNp9sRSxqdT2QjHXBEHw.19150.0; _px3=4a7d5a80261b5d3a119a6521802f7dbe7f18e0be7e887f7d386f455daf075988:TPbTPjHwepnSrS0K+/3y3nnAlcORPUBa9ZOzz0gSJqYm2h1YVRuTQpV6jEqqdYu/XMw9cBGQwMEHZLI7gt0tnQ==:1000:5iBXDFL9/H0kF25haQut5828qrKWtQ3hmcclf+z+KstdNVxBnjG8lAtQxv2Z3FhxM3QVLA8IRPXcbliAix4nU0PAgFXRTm7DLbQMstzEn/IEsoLOEMbpNTYtFgsqsBUSUvGAuOgdFTd11imPlw931vUUEp7XRMKHSNiTt70Qylxfowkv9un+IWbqL6z7rwp1R77mrttm1n2TqqCuUsPxig==; _hjSessionUser_266550=eyJpZCI6IjhlNjUyYjIwLTg1OTQtNTM1Ny1iZTM5LTVmNjAxNmJiMTk3ZSIsImNyZWF0ZWQiOjE2NDczMzM5ODA4NzUsImV4aXN0aW5nIjp0cnVlfQ==; _gcl_au=1.1.28460038.1647342993; canary=never; __uzmhj=54881313370e6e80e8d9a386cf99ce9de08b458b8f85cc0f64689069d75ffac7; server_env=production; y2_cohort_2020=50; _gid=GA1.3.1016132156.1647959658; _hjIncludedInSessionSample=0; _hjSession_266550=eyJpZCI6ImFlYzZkMDlhLTU5MGEtNGY2MC1iMDMxLThkZGMxODJjMjA1ZSIsImNyZWF0ZWQiOjE2NDc5NTk2NTgwMjksImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _gac_UA-708051-1=1.1647959805.EAIaIQobChMIqKqSz_jZ9gIVhYxoCR2BxA_rEAAYASAAEgKwWPD_BwE; favorites_userid=ddg717198517",
        #     "Upgrade-Insecure-Requests": "1",
        #     "Sec-Fetch-Dest": "document",
        #     "Sec-Fetch-Mode": "navigate",
        #     "Sec-Fetch-Site": "none",
        #     "Sec-Fetch-User": "?1"
        # }
        # rv = requests.get('https://mhaifafc.com/')
        # r = requests.get(url, headers=headers, cookies=rv.cookies)
        # self.driver.get(url)
        return '054-3246673'



# yad2_searcher_api = yad2_searcher_api()
# yad2_searcher_api.search_apartments()
#https://www.yad2.co.il/api/item/c48e2fb4/contactinfo?id=c48e2fb4