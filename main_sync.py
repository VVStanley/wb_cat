import time

import requests

from schemas import Category, FiltersModel, RootModel

SEARCH_TERM = "catalog"


def fetch_catalog():
    r = requests.get(f"https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v3.json")
    return [Category(**category) for category in r.json() if
            category.get("url") and SEARCH_TERM in category.get("url")]


def fetch_products(cat):
    r = requests.get(
        f"https://catalog.wb.ru/catalog/{cat.shard}/v2/catalog?ab_testing=false&appType=1&{cat.query}"
        f"&curr=rub&dest=-5720478"
    )
    return RootModel.parse_raw(r.content)


def fetch_filters(cat):
    r = requests.get(
        f"https://catalog.wb.ru/catalog/{cat.shard}/v6/filters?ab_testing=false&appType=1&{cat.query}"
        "&curr=rub&dest=-5720478&spp=30&uclusters=3"
    )
    return FiltersModel.parse_obj(r.json().get("data"))


def get_products(cats):
    products = []
    for cat in cats:
        print("-------------------------START-------")
        print(cat.name)
        if cat.childs is None and cat.shard:
            products_models = fetch_products(cat)
            filter_ = fetch_filters(cat)
            if filter_.filters and filter_.filters[0].name == "Категория":
                items = filter_.filters[0].items
                print(items)
            print(products_models.data.total)
            products.append(products_models)
            print("-------------------------STOP-------")
        elif cat.childs:
            products.extend(get_products(cat.childs))
            if len(products) >= 500:
                print("!!!!")
                break
    return products


def main():
    start_time = time.time()
    catalog = fetch_catalog()
    products = []
    try:
        products = get_products(catalog)
    except Exception as e:
        print("ОШИБКА -- ", str(e))
    end_time = time.time()
    print(f"Время выполнения: {end_time - start_time:.2f} секунд")
    print("products = ", len(products))


if __name__ == "__main__":
    main()
