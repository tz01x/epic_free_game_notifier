import json
import re
import traceback
import uuid
import requests
import pytz
from epicbot_interface.epic_bot.utils import get_date_obj
from .notify_user import notify_all_subs
from epicbot_interface.models import PromoData


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
    obj = PromoData.objects.all().first()
    previously_seen_game =  json.loads(obj.data or "{}") if obj else {}

    data = get_data_from_api()

    if data["extensions"]:
        return

    try:
        elements = data["data"]["Catalog"]["searchStore"]["elements"]
        for ele in elements:
            productSlug = uuid.uuid4().hex

            if not ele.get("productSlug"):
    
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
    
            if not ele.get('promotions') or \
                ele.get('promotions').get('upcomingPromotionalOffers'):
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
        
        if obj is not None:
            PromoData.objects.filter(id=obj.id).update(data=json.dumps(previously_seen_game))
        else:
            PromoData.objects.create(data=json.dumps(previously_seen_game))
        if has_new_data:
            notify_all_subs()

    except Exception as e:
        raise e



def get_data_from_api():
    req_url = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions"

    headers_list = {}

    payload = ""

    response = requests.request(
        "GET", req_url, data=payload, headers=headers_list, timeout=30
    )
    print('reading data')
    data = response.json()
    return data
