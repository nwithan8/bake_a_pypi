from typing import Union, List
from urllib.parse import urlencode

import requests

from TargetAPI.products import Product, Availability
from TargetAPI.stores import Store

def _make_url(base: str, endpoint: str):
    if base.endswith("/"):
        base = base[:-1]
    if endpoint.startswith("/"):
        endpoint = endpoint[1:]
    return f"{base}/{endpoint}"


class Target:
    def __init__(self, api_key: str):
        self._api_key = api_key
        self.api = TargetAPI(api_key=api_key, target_instance=self)
        self.redsky = RedSky(api_key=api_key, target_instance=self)

    def _store_by_id(self, store_id: str) -> Union[Store, None]:
        for store in self.stores:
            if store.id == store_id:
                return store
        return None

    def find_stores(self, keyword: str) -> List[Store]:
        locations = []
        for store in self.stores:
            if keyword in store.name:
                locations.append(store)
        return locations

    @property
    def stores(self) -> List[Store]:
        return self.api.stores

    def search(self, keyword: str, store_id: str = None, store_search: bool = False, sort_by: str = "relevance") -> List[Product]:
        return self.redsky.search_products(keyword=keyword, store_id=store_id, store_search=store_search, sort_by=sort_by)


class API:
    def __init__(self, api_key: str, target_instance: Target):
        self._key = api_key
        self._target_instance = target_instance
        self._base_url = "https://api.target.com/"

    def _get_json(self, endpoint: str, params: dict = {}) -> dict:
        res = self._get(endpoint=endpoint, params=params)
        if res:
            return res.json()
        return {}

    def _get(self, endpoint: str, params: dict = {}) -> Union[requests.Response, None]:
        params['key'] = self._key
        url = _make_url(base=self._base_url, endpoint=endpoint)
        url += f"?{urlencode(params)}"
        print(url)
        res = requests.get(url=url)
        if res:
            return res
        return None


class RedSky(API):
    def __init__(self, api_key: str, target_instance: Target):
        super().__init__(api_key=api_key, target_instance=target_instance)
        self._base_url = "https://redsky.target.com/"

    def search_products(self, keyword: str, store_id: str = None, store_search: bool = False, sort_by: str = "relevance") -> List[Product]:
        products = []
        params = {
            'searchTerm': keyword,
            'pageNumber': 1,
            'storeSearch': store_search,
            'sortBy': sort_by,
            'pricing_context': 'digital' if not store_id else 'in_store',
            'pricing_store_id': store_id if store_id else '3991'
        }
        endpoint = 'v4/products/list'
        if store_id:
            endpoint += f"/{store_id}"
            params['storeId'] = store_id
        data = self._get_json(endpoint=endpoint, params=params)
        if data:
            if not data.get('products'):
                print("Target is attempting to redirect you to a category page. Please reword your keyword.")
            else:
                for prod in data['products']:
                    products.append(Product(data=prod, target=self._target_instance))
        return products


class TargetAPI(API):
    def __init__(self, api_key: str, target_instance: Target):
        super().__init__(api_key=api_key, target_instance=target_instance)
        self._base_url = "https://api.target.com/"
        self._locations = []

    @property
    def stores(self) -> List[Store]:
        if not self._locations:
            self._locations = []
            data = self._get_json(endpoint='ship_locations/v1')
            if data:
                for loc in data:
                    self._locations.append(Store(data=loc, target=self._target_instance))
        return self._locations

    def product_availability(self, product: Product, nearby_store: str = None, inventory_type: str = 'ALL', multichannel: str = 'ALL') -> Union[Availability, None]:
        params = {
            'inventory_type': inventory_type,
            'multichannel_option': multichannel
        }
        if nearby_store:
            params['nearby_store'] = nearby_store
        data = self._get_json(endpoint=f"available_to_promise/v2/{product.tcin}", params=params)
        if data and data.get('products'):
            return Availability(data=data['products'][0], target=self._target_instance, product=product)
        return None