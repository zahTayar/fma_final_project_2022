from requests import post, get, RequestException
import logging
import uuid
import requests
import datetime
import math

from src.main.fma.controllers import nadlan_gov_db

log = logging.getLogger("MAIN LOGGER")
logging.basicConfig(filename="logs/nadlan_log.md", filemode='w',
                    format='%(asctime)s, %(msecs)d, %(name)s, %(levelname)s, %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
class nadlangov():
    def __init__(self):
        pass

    # Get name from user and bring all apartments sold in this town.
    # Can look in log.md to view progress
    def search_all_town(self):

        # first get id town and every data possible
        # word_from_user = input("please enter the name of the tow:\n")
        word_from_user = "קרית שמונה"
        non_stop = True
        while non_stop:
            try:
                answer_from_get = get(
                    "https://www.nadlan.gov.il/Nadlan.REST/Main/GetDataByQuery?query=" + word_from_user)
                log.info("SUCCESS, please verify there is all possible towns in dict")
                non_stop = False
            except requests.exceptions.RequestException as e:
                log.info("FAILED, please verify you done everything right")

        # set post request

        all_town = {}
        is_last_page = False
        counter_for_pages = 1
        dic_to_post = dict(answer_from_get.json())

        while not is_last_page:
            non_stop = True
            while non_stop:
                try:
                    dic_to_post["PageNo"] = counter_for_pages
                    answer_from_post = post("https://www.nadlan.gov.il/Nadlan.REST/Main/GetAssestAndDeals",
                                            json=dic_to_post)
                    all_town[counter_for_pages] = answer_from_post.json()["AllResults"]
                    log.info("first apartment in list is : %s", all_town[counter_for_pages][0])
                    log.info("page number %d done successfully", counter_for_pages)
                    counter_for_pages += 1
                    if list(answer_from_post.json()["AllResults"]).pop(0)["DEALDATE"].split(".")[2] == '2017':
                        is_last_page = True
                    else:
                        is_last_page = answer_from_post.json()["IsLastPage"]
                    non_stop = False
                    # is_last_page = False
                except requests.exceptions.RequestException as e:
                    log.info("FAILED,page number %d didn't load right please verify connection\n", counter_for_pages)
                    log.info("ERROR: %s", e)

        return all_town

    # Generate unique id
    def generate_unique_id(self):
        return uuid.uuid4()

    def initial_data_proccessor(self, tmp_deal):
        json_builder = {
            "new_id": self.generate_unique_id(),
            "did_changed": False,
            "time_creation": str(datetime.datetime.now()),
            "date_deal": "N/A",
            "year_deal": "N/A",  # problem
            "month_deal": "N/A",  # problem
            "full_address": "N/A",  # problem
            "city": "N/A",
            "street_and_number": "N/A",
            "all_gush_str": "N/A",
            "gush": "N/A",
            "property": "N/A",
            "sub_property": "N/A",
            "deal_description": "N/A",
            "asset_room_numbers": "N/A",
            "floor_number": "N/A",
            "asset_size_in_meters": "N/A",
            "price_sold_asset": "N/A",
            "new_project_description": "N/A",
            "project_name": "N/A",
            "year_building_build": "N/A",
            "building_floor": "N/A",
            "key_in_nadlan": "N/A",
            "type": 0,
            "is_negative_trend": False,
            "trend_format": "N/A",
            "sub_property": "N/A",
            "property": "N/A"
        }
        # deal date field
        if tmp_deal["DEALDATE"] is not None and len(tmp_deal["DEALDATE"]) > 0 and tmp_deal["DEALDATE"] != "None":
            json_builder["date_deal"] = tmp_deal["DEALDATE"]
            if len(tmp_deal["DEALDATE"].split(".")) > 1:
                json_builder["month_deal"] = tmp_deal["DEALDATE"].split(".")[1]
                if len(tmp_deal["DEALDATE"].split(".")) > 2:
                    json_builder["year_deal"] = tmp_deal["DEALDATE"].split(".")[2]
        # adrress deal handling
        if tmp_deal["FULLADRESS"] is not None and len(tmp_deal["FULLADRESS"]) > 0 and tmp_deal["FULLADRESS"] != "None":
            json_builder["full_address"] = tmp_deal["FULLADRESS"]
            if len(tmp_deal["FULLADRESS"].split(",")) > 1:
                json_builder["city"] = tmp_deal["FULLADRESS"].split(",")[1]
                json_builder["street_and_number"] = tmp_deal["FULLADRESS"].split(",")[0]
        # divide it for gush property and sub property
        if tmp_deal["GUSH"] is not None and len(tmp_deal["GUSH"]) > 0 and tmp_deal["GUSH"] != "None":
            json_builder["all_gush_str"] = tmp_deal["GUSH"]
            if len(tmp_deal["GUSH"].split("-")) > 1:
                json_builder["gush"] = tmp_deal["GUSH"].split("-")[0]
                json_builder["property"] = tmp_deal["GUSH"].split("-")[1]
                if len(tmp_deal["GUSH"].split("-")) > 2:
                    json_builder["sub_property"] = tmp_deal["GUSH"].split("-")[2]
        # deal description
        if tmp_deal["DEALNATUREDESCRIPTION"] is not None and len(tmp_deal["DEALNATUREDESCRIPTION"]) > 0 and tmp_deal[
            "DEALNATUREDESCRIPTION"] != "None":
            json_builder["deal_description"] = tmp_deal["DEALNATUREDESCRIPTION"]
        # number of rooms in asset
        if tmp_deal["ASSETROOMNUM"] is not None and len(tmp_deal["ASSETROOMNUM"]) > 0 and tmp_deal[
            "ASSETROOMNUM"] != "None":
            json_builder["asset_room_numbers"] = int(math.ceil(float(tmp_deal["ASSETROOMNUM"])))
        # property floor number
        if tmp_deal["FLOORNO"] is not None and len(tmp_deal["FLOORNO"]) > 0 and tmp_deal["FLOORNO"] != "None":
            json_builder["floor_number"] = tmp_deal["FLOORNO"]
        # size in meters of asset
        if tmp_deal["DEALNATURE"] is not None and len(tmp_deal["DEALNATURE"]) > 0 and tmp_deal["DEALNATURE"] != "None":
            json_builder["asset_size_in_meters"] = int(math.ceil(float(tmp_deal["DEALNATURE"])))
        # deal price sold
        if tmp_deal["DEALAMOUNT"] is not None and tmp_deal["DEALAMOUNT"] is not None and len(
                tmp_deal["DEALAMOUNT"]) > 0 and \
                tmp_deal["DEALAMOUNT"] != "None":
            json_builder["price_sold_asset"] = int(tmp_deal["DEALAMOUNT"].replace(",",""))
        # if new project
        if tmp_deal["NEWPROJECTTEXT"] is not None and len(tmp_deal["NEWPROJECTTEXT"]) > 0 and tmp_deal[
            "NEWPROJECTTEXT"] != "None":
            json_builder["new_project_description"] = tmp_deal["NEWPROJECTTEXT"]
        # project name if have one
        if tmp_deal["PROJECTNAME"] is not None and len(tmp_deal["PROJECTNAME"]) > 0 and tmp_deal[
            "PROJECTNAME"] != "None":
            json_builder["project_name"] = tmp_deal["PROJECTNAME"]
        # year building build
        if tmp_deal["BUILDINGYEAR"] is not None and len(tmp_deal["BUILDINGYEAR"]) > 0 and tmp_deal[
            "BUILDINGYEAR"] != "None":
            json_builder["year_building_build"] = tmp_deal["BUILDINGYEAR"]  # deal price sold
        # building floor number
        if tmp_deal["BUILDINGFLOORS"] is not None and len(tmp_deal["BUILDINGFLOORS"]) > 0 and tmp_deal[
            "BUILDINGFLOORS"] != "None":
            json_builder["building_floor"] = tmp_deal["BUILDINGFLOORS"]
        # nadlan key in DB
        if tmp_deal["KEYVALUE"] is not None and len(tmp_deal["KEYVALUE"]) > 0 and tmp_deal["KEYVALUE"] != "None":
            json_builder["key_in_nadlan"] = tmp_deal["KEYVALUE"]
        # type
        if tmp_deal["TYPE"] is not None and tmp_deal["TYPE"] != "None":
            json_builder["type"] = tmp_deal["TYPE"]
        # is trend negative
        if tmp_deal["TREND_IS_NEGATIVE"] is not None and tmp_deal["TREND_IS_NEGATIVE"] != "None":
            json_builder["is_negative_trend"] = tmp_deal["TREND_IS_NEGATIVE"]
        # format for trend in nadlan
        if tmp_deal["TREND_FORMAT"] is not None and len(tmp_deal["TREND_FORMAT"]) > 0 and tmp_deal[
            "TREND_FORMAT"] != "None":
            json_builder["trend_format"] = tmp_deal["TREND_FORMAT"]
        json_builder["did_changed"] = True
        # print(json_builder)
        return json_builder

    # Manage the data
    def data_manager(self, all_pages):
        for i in range(len(all_pages)):
            all_deals_in_page = list(all_pages[i + 1])
            for g in range(len(all_deals_in_page)):
                tmp_deal = all_deals_in_page.pop(g)
                asset_with_my_fields = self.initial_data_proccessor(tmp_deal)
                all_deals_in_page.insert(g, asset_with_my_fields)
                nadlan_gov_db.insert_one(asset_with_my_fields)

        print(all_pages)