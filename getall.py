from Config import Config
from utils.Cybersafeapi import Cybersafeapi
import json


def app(name,id,msg,exp,price,new_price):
    userJSON = json.load(open('./database/allapp.json', 'r', encoding='utf-8'))
    userJSON[id] = ({
                        'id': id,
                        'name': name,
                        'msg': msg,
                        "exp": exp,
                        "price": price,
                        "new_price": new_price
                    })
    json.dump(userJSON, open('./database/allapp.json', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)


def calculate_new_price(price, percentage):
    new_price = float(price) + (float(price) * float(percentage) / 100)
    return new_price

price_percentage = Config().Get()["configweb"]["price_percentage"]
dd = Cybersafeapi()
aa = dd.Dtstoresocial().json()["result"]
for i in aa:
    print(i["name"],i["price"],calculate_new_price(i["price"],(price_percentage)))
    app(name=i["name"],id=i["id"],msg=i["msg"],exp=i["exp"],price=i["price"],new_price=calculate_new_price(i["price"],(price_percentage)))

