import json
import re
import traceback
import uuid
import requests
import pytz
from epicbot_interface.epic_bot.utils import get_date_obj
from .notify_user import notify_all_subs

def find(func, iterator, default=None):
    '''
    return the first match item from iterator or return default
    '''
    items = [item for item in iterator if func(item)]

    return items[0] if len(items) > 0 else default


def fetch_promo_game():
    print('job start')
    previously_seen_game = {}
    has_new_data = False
    with open("epicbot_interface/epic_bot/previously_seen_product.json", "r", encoding="utf-8") as f:
        previously_seen_game = json.load(f)

    data = get_data_from_api()

    if data["extensions"]:
        return

    try:
        elements = data["data"]["Catalog"]["searchStore"]["elements"]
        for ele in elements:
            productSlug = uuid.uuid4().hex

            if ele["productSlug"] == None:
    
                productSlug = find(
                    lambda x:x['pageType'] == 'productHome',
                    ele['catalogNs']['mappings'],
                    default={},
                ).get('pageSlug')

            else:
                productSlug = ele["productSlug"]

            if productSlug == "[]":
                continue

            # we will skip the upcoming promo offers
            if len(ele['promotions']['upcomingPromotionalOffers']) > 0:
                continue

            promotionalOffers = ele["promotions"]["promotionalOffers"][-1]["promotionalOffers"][-1]

            item = previously_seen_game.get(productSlug)

            if item and \
                    get_date_obj(item["promotionalOffers_end_date"]).astimezone(tz=pytz.UTC) > \
                    get_date_obj(promotionalOffers["startDate"]).astimezone(tz=pytz.UTC):
                print(f'{ele["title"]} seen')
                continue
            
            image_url = find(
                lambda x: re.match(r"[A-Za-z]{0,}Wide$", x['type']),
                ele['keyImages'],
                default={}
            ).get('url')

            previously_seen_game[productSlug] = {
                "productSlug": productSlug,
                "title": ele["title"],
                "description": ele["description"],
                "id": ele["id"],
                "namespace": ele["namespace"],
                "promotionalOffers_start_date": promotionalOffers["startDate"],
                "promotionalOffers_end_date": promotionalOffers["endDate"],
                "image_url":image_url,
            }
            has_new_data = True
        
        with open("epicbot_interface/epic_bot/previously_seen_product.json", "w", encoding="utf-8") as f:
            json.dump(previously_seen_game, f)
        if has_new_data:
            notify_all_subs()

    except Exception as _:

        with open("./error_log.txt", "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())



def get_data_from_api():
    req_url = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions"

    headers_list = {}

    payload = ""

    response = requests.request(
        "GET", req_url, data=payload, headers=headers_list, timeout=30
    )

    data = response.json()
    return data
