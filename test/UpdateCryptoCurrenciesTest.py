from unittest import TestCase

from app import crypto_trader_app
from database import SqlLiteDbHelper
from database.CryptoCurrenciesStorage import CryptoCurrenciesStorage
from database.ExchangesStorage import ExchangesStorage
from utils import CurrencyExchangeRateDownloader
from utils.Routes import UPDATE_CRYPTO_CURRENCIES_ROUTE, ADD_CRYPTO_EXCHANGE_ROUTE
from utils.Responses import INVALID_DATA_ERROR_JSON_RESPONSE, INCORRECT_EXCHANGE_ID_JSON_RESPONSE


# Tests testing add update crypto currencies api call
# noinspection DuplicatedCode
class CryptoCurrenciesTest(TestCase):

    def setUp(self):
        SqlLiteDbHelper.enable_persist_data_db = False
        ExchangesStorage.exchanges_storage = {}
        CryptoCurrenciesStorage.crypto_currencies_storage = {}
        CurrencyExchangeRateDownloader.download_exchange_rate_enabled = False
        self.app = crypto_trader_app.test_client()

    def test_add_crypto_currency(self):
        exchange_id = self.mock_crypto_exchange()
        response = self.app.put(UPDATE_CRYPTO_CURRENCIES_ROUTE.format(exchange_id),
                                json={'action': 'ADD', 'name': 'Bitcoin', 'shortcut': 'BTC'})
        json_data = response.json[0]
        self.assertEqual('Bitcoin', json_data.get("name"))
        self.assertEqual('BTC', json_data.get("shortcut"))
        self.assertEqual(exchange_id, json_data.get("exchange_id"))

    def test_multiple_add_crypto_currencies(self):
        exchange_id = self.mock_crypto_exchange()
        self.app.put(UPDATE_CRYPTO_CURRENCIES_ROUTE.format(exchange_id),
                     json={'action': 'ADD', 'name': 'Ethereum', 'shortcut': 'ETH'})
        response = self.app.put(UPDATE_CRYPTO_CURRENCIES_ROUTE.format(exchange_id),
                                json={'action': 'ADD', 'name': 'Bitcoin', 'shortcut': 'BTC'})
        json_data = response.json[1]
        self.assertEqual('Bitcoin', json_data.get("name"))
        self.assertEqual('BTC', json_data.get("shortcut"))
        self.assertEqual(exchange_id, json_data.get("exchange_id"))
        json_data = response.json[0]
        self.assertEqual('Ethereum', json_data.get("name"))
        self.assertEqual('ETH', json_data.get("shortcut"))
        self.assertEqual(exchange_id, json_data.get("exchange_id"))

    def test_add_crypto_currencies_invalid_exchange_id(self):
        response = self.app.put(UPDATE_CRYPTO_CURRENCIES_ROUTE.format(0),
                                json={'action': 'ADD', 'name': 'Ethereum', 'shortcut': 'ETH'})
        json_data = response.json
        self.assertEqual(INCORRECT_EXCHANGE_ID_JSON_RESPONSE, json_data)

    def test_add_crypto_currencies_string_exchange_id(self):
        response = self.app.put(UPDATE_CRYPTO_CURRENCIES_ROUTE.format("text"),
                                json={'action': 'ADD', 'name': 'Ethereum', 'shortcut': 'ETH'})
        json_data = response.json
        self.assertEqual(INCORRECT_EXCHANGE_ID_JSON_RESPONSE, json_data)

    def test_add_crypto_currencies_long_shortcut(self):
        exchange_id = self.mock_crypto_exchange()
        response = self.app.put(UPDATE_CRYPTO_CURRENCIES_ROUTE.format(exchange_id),
                                json={'action': 'ADD', 'name': 'Ethereum', 'shortcut': 'ETHETH'})
        json_data = response.json
        self.assertEqual(INVALID_DATA_ERROR_JSON_RESPONSE, json_data)

    def test_add_crypto_currencies_empty_name(self):
        exchange_id = self.mock_crypto_exchange()
        response = self.app.put(UPDATE_CRYPTO_CURRENCIES_ROUTE.format(exchange_id),
                                json={'action': 'ADD', 'name': '', 'shortcut': 'ETH'})
        json_data = response.json
        self.assertEqual(INVALID_DATA_ERROR_JSON_RESPONSE, json_data)

    def test_update_crypto_currencies_duplicity(self):
        exchange_id = self.mock_crypto_exchange()
        response = self.app.put(UPDATE_CRYPTO_CURRENCIES_ROUTE.format(exchange_id),
                                json={'action': 'ADD', 'name': 'BITCOIN', 'shortcut': 'BTC'})
        json_data = response.json[0]
        currency_id = json_data.get("currency_id")
        self.app.put(UPDATE_CRYPTO_CURRENCIES_ROUTE.format(exchange_id),
                     json={'action': 'ADD', 'name': 'Bitcoin', 'shortcut': 'BTC',
                           'currency_id': currency_id})
        response = self.app.put(UPDATE_CRYPTO_CURRENCIES_ROUTE.format(exchange_id),
                                json={'action': 'UPDATE', 'name': 'Bitcoin', 'shortcut': 'BTC',
                                      'currency_id': currency_id})
        json_data = response.json[0]
        self.assertEqual('Bitcoin', json_data.get("name"))
        self.assertEqual('BTC', json_data.get("shortcut"))
        self.assertEqual(exchange_id, json_data.get("exchange_id"))
        self.assertEqual(len(response.json), 1)

    def test_remove_crypto_currency(self):
        exchange_id = self.mock_crypto_exchange()
        response = self.app.put(UPDATE_CRYPTO_CURRENCIES_ROUTE.format(exchange_id),
                                json={'action': 'ADD', 'name': 'Bitcoin', 'shortcut': 'BTC'})
        json_data = response.json[0]
        self.assertEqual('Bitcoin', json_data.get("name"))
        self.assertEqual('BTC', json_data.get("shortcut"))
        self.assertEqual(exchange_id, json_data.get("exchange_id"))
        self.assertEqual(len(response.json), 1)
        json_data = response.json[0]
        currency_id = json_data.get("currency_id")
        response = self.app.put(UPDATE_CRYPTO_CURRENCIES_ROUTE.format(exchange_id),
                                json={'action': 'REMOVE', 'name': 'Bitcoin', 'shortcut': 'BTC',
                                      'currency_id': currency_id})
        self.assertEqual(0, len(response.json))

    def test_invalid_action_crypto_currency(self):
        exchange_id = self.mock_crypto_exchange()
        response = self.app.put(UPDATE_CRYPTO_CURRENCIES_ROUTE.format(exchange_id),
                                json={'action': 'invalid', 'name': 'Bitcoin', 'shortcut': 'BTC'})
        self.assertEqual(INVALID_DATA_ERROR_JSON_RESPONSE, response.json)

    def post_add_crypto_currency(self):
        return self.app.post(ADD_CRYPTO_EXCHANGE_ROUTE, json={'name': 'exchange_name', 'currency': 'USD'})

    def mock_crypto_exchange(self):
        response = self.post_add_crypto_currency()
        json_data = response.json
        exchange_id = json_data.get("exchange_id")
        return exchange_id
