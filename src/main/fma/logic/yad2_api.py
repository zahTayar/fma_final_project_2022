from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import logging

PATH = "C:\Program Files (x86)\chromedriver.exe"


class yad2_searcher:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("start-maximized")
        self.driver = webdriver.Chrome(PATH, chrome_options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.apartments = []
        logging.basicConfig(level=logging.INFO, filename='yad2.log', filemode="w")
        logging.info('Initial driver done')
        logging.info('################################')

    def search_in_yad2(self):
        driver = self.driver
        driver.get("http://www.google.com")
        driver.get("http://www.yad2.co.il/realestate/forsale?topArea=43&area=22&city=9000")
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "feed_list")))
        pages_amount = int(driver.find_element_by_xpath("(//button[@class = 'page-num'])").text.strip())
        logging.info("There are " + str(pages_amount) + " pages")
        logging.info('################################')
        for i in range(0, pages_amount):
            logging.info("Start scanning page number " + str(i))
            logging.info('################################')
            try:
                WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "feed_list")))
                list_apartments = driver.find_element_by_class_name("feed_list")
                list_items = list_apartments.find_elements_by_xpath("(//*[contains(@class, 'feeditem table')])")
                for item in list_items:
                    logging.info("Scanning apartment " + str(list_items.index(item)) + "/" + str(len(list_items)))
                    logging.info('################################')
                    if self.open_apartment_in_new_tab(item):
                        self.add_apartment_details()
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                logging.info("Scanning page number " + str(i) + " done. " + str(len(list_items)) + "apartments were "
                                                                                                   "added.")
                logging.info('################################')
                self.move_next_page()
            except Exception as e:
                logging.exception("Exception occurred")

    def open_apartment_in_new_tab(self, item):
        driver = self.driver
        try:
            new_tab = item.find_element_by_class_name('new_tab')
        except NoSuchElementException:
            return False
        driver.execute_script("arguments[0].scrollIntoView();", new_tab)
        driver.execute_script("arguments[0].click();", new_tab)
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[1])
        return True

    def move_next_page(self):
        move_next_page_btn = self.driver.find_elements_by_xpath("(//a[contains(@class, 'pagination-nav text')])")
        self.driver.execute_script("arguments[0].scrollIntoView();", move_next_page_btn)
        move_next_page_btn.click()

    def tearDown(self):
        self.driver.close()

    def find_phone_number(self):
        click_ele = self.driver.find_element_by_xpath("(//button[contains(@id, 'contact_seller')])")
        click_ele.click()
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "phone_number")))
        return self.driver.find_element_by_xpath("(//a[@class = 'phone_number'])").text

    def find_pictures(self):
        pictures = []
        click_ele = self.driver.find_element_by_xpath("(//div[@class = 'swiper-slide swiper-slide-active'])")
        click_ele.click()
        time.sleep(3)
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "grid-gallery")))
        pictures_list = self.driver.find_elements_by_xpath("(//li[starts-with(@class, 'grid-gallery-item image')])")
        for picture in pictures_list:
            img = picture.find_element_by_css_selector("img")
            pictures.append(img.get_attribute("src"))
        self.driver.find_element_by_xpath("(//button[@class = 'gallery-popup-nav-button close-popup'])").click()
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "main-menu")))
        return pictures

    def add_apartment_details(self):
        driver = self.driver
        self.apartments.append({
            'description': driver.find_element_by_xpath("(//*[contains(@class, 'show_more content')])").text,
            'price': driver.find_element_by_xpath("(//strong[@class = 'price'])").text,
            'num_of_rooms': driver.find_element_by_xpath("(//dl[@class = 'cell rooms-item'])").text.split('\n')[0],
            'floor': driver.find_element_by_xpath("(//dl[@class = 'cell floor-item'])").text.split('\n')[0],
            'location': {
                'street': driver.find_element_by_xpath("(//h4[@class = 'main_title'])").text,
                'neighbor': driver.find_element_by_xpath("(//span[@class = 'description'])").text.split(',')[0],
                'city': driver.find_element_by_xpath("(//span[@class = 'description'])").text.split(',')[1].strip()
            },
            'square_meter':
                driver.find_element_by_xpath("(//dl[@class = 'cell SquareMeter-item'])").text.split('\n')[0],
            'date_of_uploaded': driver.find_element_by_xpath("(//span[@class = 'left'])").text,
            'pictures': self.find_pictures(),
            'contract_name': driver.find_element_by_xpath("(//span[@class = 'name'])").text,
            'contract_phone': self.find_phone_number()
        })


searcher = yad2_searcher()
searcher.search_in_yad2()
