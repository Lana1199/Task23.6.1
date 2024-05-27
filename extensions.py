import requests
import json
from config import keys


class APIExcetion(Exception):
    pass


class CriptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIExcetion(f'Невозможно перевести одинаковые валюты{base}.')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIExcetion(f'Не удалось обработать валюту {quote}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIExcetion(f'Не удалось обработать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise APIExcetion(f'Не удалось обработать количество валюты {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
       
        return total_base * amount
