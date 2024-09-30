import requests

from schemas import Category, RootModel

SEARCH_TERM = "catalog"
r = requests.get(f"https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v3.json")

catalog = [Category(**category) for category in r.json() if category.get("url") and SEARCH_TERM in category.get("url")]


def get_products(cats):
    products = []
    for cat in cats:
        if cat.childs is None and cat.shard:
            products_in_cat = requests.get(
                f"https://catalog.wb.ru/catalog/{cat.shard}/v2/catalog?ab_testing=false&appType=1&{cat.query}&curr=rub&dest=-5720478"
            )

            products_models = RootModel.parse_raw(products_in_cat.content)
            print(products_models.version)
            print(products_models.data.total)
            print(len(products_models.data.products))
            products.append(products_models)

        elif cat.childs:
            products.extend(get_products(cat.childs))
    return products


get_products(catalog)
