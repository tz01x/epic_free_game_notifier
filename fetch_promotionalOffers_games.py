import requests
import json
from utils import get_date_obj

previously_seen_game = {}

available_games = []




with open('previously_seen_product.json', 'r', encoding='utf-8') as f:
    previously_seen_game = json.load(f)


reqUrl = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions"

headersList = {
}

payload = ""

response = requests.request(
    "GET", reqUrl, data=payload,  headers=headersList, timeout=30)

data = response.json()


if not data['extensions']:
    try:
        elements = data['data']['Catalog']['searchStore']['elements']
        for ele in elements:
            if ele['productSlug'] == '[]':
                continue

            promotionalOffers = ele['promotions']['promotionalOffers'][-1]['promotionalOffers'][-1]

            item = previously_seen_game.get(ele['productSlug'])

            if item and get_date_obj(item['promotionalOffers_end_date']) > get_date_obj(promotionalOffers['startDate']):
                print(f'{ele["title"]} seen')
                continue

            previously_seen_game[ele["productSlug"]] = {
                "productSlug": ele["productSlug"],
                "title": ele["title"],
                "description": ele["description"],
                "id": ele["id"],
                "namespace": ele["namespace"],
                "promotionalOffers_start_date": promotionalOffers['startDate'],
                "promotionalOffers_end_date": promotionalOffers['endDate'],
                "status": "active"
            }
    except Exception as e:
        import traceback
        with open('error_log.txt', 'w', encoding='utf-8') as f:
            f.write(traceback.format_exc())

for g in available_games:
    previously_seen_game[g['productSlug']] = {**g}


with open('previously_seen_product.json', 'w') as f:
    json.dump(previously_seen_game, f)
