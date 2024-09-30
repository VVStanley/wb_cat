from concurrent.futures import ProcessPoolExecutor, as_completed

import requests

from schemas import Category, RootModel

SEARCH_TERM = "catalog"


def fetch_catalog():
    r = requests.get("https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v3.json")
    return [Category(**category) for category in r.json() if
            category.get("url") and SEARCH_TERM in category.get("url")]


def fetch_products(cat):
    products_in_cat = requests.get(
        f"https://catalog.wb.ru/catalog/{cat.shard}/v2/catalog?ab_testing=false&appType=1&{cat.query}&curr=rub&dest=-5720478"
    )
    return RootModel.parse_raw(products_in_cat.content)


def get_products(cats):
    products = []
    with ProcessPoolExecutor() as executor:
        futures = {}
        for cat in cats:
            if cat.childs is None and cat.shard:
                futures[executor.submit(fetch_products, cat)] = cat
            elif cat.childs:
                products.extend(get_products(cat.childs))

        for future in as_completed(futures):
            products_models = future.result()
            print(products_models.version)
            print(products_models.data.total)
            print(len(products_models.data.products))
            products.append(products_models)

    return products


if __name__ == "__main__":
    catalog = fetch_catalog()
    get_products(catalog)
