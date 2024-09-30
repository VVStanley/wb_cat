import asyncio

import httpx

from schemas import Category, FiltersModel, RootModel

SEARCH_TERM = "catalog"


async def fetch_catalog():
    async with httpx.AsyncClient() as client:
        r = await client.get("https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v3.json")
        return [Category(**category) for category in r.json() if
                category.get("url") and SEARCH_TERM in category.get("url")]


async def fetch_products(cat):
    async with httpx.AsyncClient() as client:
        products_in_cat = await client.get(
            f"https://catalog.wb.ru/catalog/{cat.shard}/v2/catalog?ab_testing=false&appType=1&{cat.query}"
            f"&curr=rub&dest=-5720478"
        )
        return RootModel.parse_raw(products_in_cat.content)


async def fetch_filters(cat):
    async with httpx.AsyncClient() as client:
        filter_ = await client.get(
            f"https://catalog.wb.ru/catalog/{cat.shard}/v6/filters?ab_testing=false&appType=1&{cat.query}"
            "&curr=rub&dest=-5720478&spp=30&uclusters=3"
        )
        return FiltersModel.parse_obj(filter_.json().get("data"))


async def get_products(cats):
    products = []
    for cat in cats:
        if cat.childs is None and cat.shard:
            products_models = await fetch_products(cat)
            filter_ = await fetch_filters(cat)
            print("-------------------------START-------")
            print(cat.name)
            if filter_.filters and filter_.filters[0].name == "Категория":
                print(filter_.filters[0].items)
            print(products_models.data.total)
            print("-------------------------STOP-------")
            products.append(products_models)
        elif cat.childs:
            products.extend(await get_products(cat.childs))
    return products


async def main():
    catalog = await fetch_catalog()
    await get_products(catalog)


if __name__ == "__main__":
    asyncio.run(main())
