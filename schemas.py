from typing import List, Optional, Union

from pydantic import BaseModel


class Category(BaseModel):
    id: int
    name: str
    url: str
    parent: Optional[int] = None
    seo: Optional[str] = None
    shard: Optional[str] = None
    query: Optional[str] = None
    childs: Optional[List[Union["Category"]]] = None
    is_deny_link: Optional[bool] = None


Category.update_forward_refs()


class Color(BaseModel):
    name: str
    id: int


class Price(BaseModel):
    basic: int
    product: int
    total: int
    logistics: int
    return_: Optional[int] = 0


class Size(BaseModel):
    name: str
    origName: str
    rank: int
    optionId: int
    wh: int
    dtype: int
    price: Price
    saleConditions: int
    payload: str


class Product(BaseModel):
    __sort: int
    ksort: int
    time1: int
    time2: int
    wh: int
    dtype: int
    dist: int
    id: int
    root: int
    kindId: int
    brand: str
    brandId: int
    siteBrandId: int
    colors: list[Color] = []
    subjectId: int
    subjectParentId: int
    name: str
    entity: str
    supplier: str
    supplierId: int
    supplierRating: float
    supplierFlags: int
    pics: int
    rating: int
    reviewRating: float
    feedbacks: int
    panelPromoId: Optional[int] = 0
    promoTextCard: Optional[str] = ""
    promoTextCat: Optional[str] = ""
    volume: int
    viewFlags: int
    isNew: Optional[bool] = False
    sizes: list[Size] = []
    totalQuantity: int
    meta: dict


class Data(BaseModel):
    products: list[Product]
    total: int


class RootModel(BaseModel):
    state: int
    version: int
    payloadVersion: int
    data: Data


class Item(BaseModel):
    id: int
    name: str
    count: Optional[int] = None


class Filter(BaseModel):
    name: str
    key: str
    maxselect: Optional[int] = None
    minTime: Optional[int] = None
    maxTime: Optional[int] = None
    fullKey: Optional[str] = None
    isTop: Optional[bool] = None
    type: Optional[str] = None
    minPriceU: Optional[int] = None
    maxPriceU: Optional[int] = None
    multiselect: Optional[int] = None
    items: Optional[List[Item]] = None


class FiltersModel(BaseModel):
    filters: List[Filter]
