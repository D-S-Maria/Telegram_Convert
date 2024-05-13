import json

import requests

from config import keys, API_KEY


class APIException(Exception):
    pass


class Convertion:
    @staticmethod
    def get_price(base, quote, amount):
        v1, v2 = None, None
        for k, v in keys.items():
            if base in v:
                v1 = k
            if quote in v:
                v2 = k
        if v1 == v2 and v1:
            raise APIException('Это одна и та же валюта')

        if not v1:
            raise APIException(f'Нет данной валюты в списке - "{base}"')
        if not v2:
            raise APIException(f'Нет данной валюты в списке - "{quote}"')
        try:
            n = float(amount)
        except ValueError:
            raise APIException(f'Введите корректное количество - {amount}')
        r = requests.get(
            f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{v1}/{v2}').content
        return json.loads(r)['conversion_rate'] * n, v1, v2
