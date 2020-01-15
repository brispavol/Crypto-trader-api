from unittest import TestCase

from app import crypto_trader_app
from database import SqlLiteDbHelper
from database.CryptoCurrenciesStorage import CryptoCurrenciesStorage
from database.ExchangesStorage import ExchangesStorage
from database.TradesStorage import TradesStorage
from utils import CurrencyExchangeRateDownloader
from utils.Routes import GET_TRADES_ROUTE, CREATE_TRADE_ROUTE, UPDATE_CRYPTO_CURRENCIES_ROUTE, ADD_DEPOSIT_ROUTE, \
    ADD_CRYPTO_EXCHANGE_ROUTE


# Tests testing get trades api call
# noinspection DuplicatedCode
class GetTradesTest(TestCase):

    def setUp(self):
        SqlLiteDbHelper.enable_persist_data_db = False
        TradesStorage.trades_storage = []
        ExchangesStorage.exchanges_storage = {}
        CryptoCurrenciesStorage.crypto_currencies_storage = {}
        CurrencyExchangeRateDownloader.download_exchange_rate_enabled = False
        self.app = crypto_trader_app.test_client()

    def test_get_trades(self):
        exchange_id = self.mock_crypto_exchange()
        self.mock_crypto_currency(exchange_id)
        self.app.post(CREATE_TRADE_ROUTE.format(exchange_id),
                      json={'amount': 100, 'currency_in': 'USD', 'currency_out': 'BTC'})
        response = self.app.get(GET_TRADES_ROUTE)
        json_data = response.json
        self.assertEqual(1, len(json_data))
        self.assertEqual(100, json_data[0].get('amount'))
        self.assertEqual('USD', json_data[0].get('currency_in'))

    def test_get_trades_more_than_limit(self):
        exchange_id = self.mock_crypto_exchange()
        self.mock_crypto_currency(exchange_id)
        self.app.post(CREATE_TRADE_ROUTE.format(exchange_id),
                      json={'amount': 100, 'currency_in': 'USD', 'currency_out': 'BTC'})
        self.app.post(CREATE_TRADE_ROUTE.format(exchange_id),
                      json={'amount': 100, 'currency_in': 'USD', 'currency_out': 'BTC'})
        self.app.post(CREATE_TRADE_ROUTE.format(exchange_id),
                      json={'amount': 100, 'currency_in': 'USD', 'currency_out': 'BTC'})
        self.app.post(CREATE_TRADE_ROUTE.format(exchange_id),
                      json={'amount': 100, 'currency_in': 'USD', 'currency_out': 'BTC'})
        self.app.post(CREATE_TRADE_ROUTE.format(exchange_id),
                      json={'amount': 100, 'currency_in': 'USD', 'currency_out': 'BTC'})
        self.app.post(CREATE_TRADE_ROUTE.format(exchange_id),
                      json={'amount': 100, 'currency_in': 'USD', 'currency_out': 'BTC'})

        response = self.app.get(GET_TRADES_ROUTE)
        json_data = response.json
        self.assertEqual(6, len(json_data))
        self.assertEqual(100, json_data[0].get('amount'))
        self.assertEqual('USD', json_data[0].get('currency_in'))

    def test_get_trades_extra_filters(self):
        exchange_id = self.mock_crypto_exchange()
        self.mock_crypto_currency(exchange_id)
        self.app.post(CREATE_TRADE_ROUTE.format(exchange_id),
                      json={'amount': 100, 'currency_in': 'USD', 'currency_out': 'BTC'})
        self.app.post(CREATE_TRADE_ROUTE.format(exchange_id),
                      json={'amount': 100, 'currency_in': 'USD', 'currency_out': 'BTC'})
        self.app.post(CREATE_TRADE_ROUTE.format(exchange_id),
                      json={'amount': 100, 'currency_in': 'USD', 'currency_out': 'BTC'})
        self.app.post(CREATE_TRADE_ROUTE.format(exchange_id),
                      json={'amount': 100, 'currency_in': 'USD', 'currency_out': 'BAC'})
        self.app.post(CREATE_TRADE_ROUTE.format(exchange_id),
                      json={'amount': 100, 'currency_in': 'USD', 'currency_out': 'BAC'})
        self.app.post(CREATE_TRADE_ROUTE.format(exchange_id),
                      json={'amount': 100, 'currency_in': 'USD', 'currency_out': 'BTC'})
        get_trades_route = GET_TRADES_ROUTE + '?offset=1&limit=3&exchange_id=' + str(
            exchange_id) + '&search=BT&date_from=2020-01-01T12:12:12Z&date_to=2020-02-01T12:12:12Z'
        response = self.app.get(get_trades_route)
        json_data = response.json
        self.assertEqual(2, len(json_data))
        self.assertEqual(100, json_data[0].get('amount'))
        self.assertEqual('USD', json_data[0].get('currency_in'))

    def post_add_crypto_currency(self):
        return self.app.post(ADD_CRYPTO_EXCHANGE_ROUTE, json={'name': 'exchange_name', 'currency': 'USD'})

    def mock_crypto_exchange(self):
        response = self.post_add_crypto_currency()
        json_data = response.json
        exchange_id = json_data.get("exchange_id")
        return exchange_id

    def mock_crypto_currency(self, exchange_id):
        self.app.post(ADD_DEPOSIT_ROUTE + str(exchange_id), json={'amount': 1000, 'currency': 'USD'})
        self.app.put(UPDATE_CRYPTO_CURRENCIES_ROUTE.format(exchange_id),
                     json={'action': 'ADD', 'name': 'Bitcoin', 'shortcut': 'BTC', 'amount': 10})
