from unittest import TestCase

from app import crypto_trader_app
from database import SqlLiteDbHelper
from database.ExchangesStorage import ExchangesStorage
from utils import CurrencyExchangeRateDownloader
from utils.Responses import INVALID_DATA_ERROR_JSON_RESPONSE
from utils.Routes import ADD_CRYPTO_EXCHANGE_ROUTE


# Tests testing app exchange api call
class AddCryptoExchangeTest(TestCase):

    def setUp(self):
        SqlLiteDbHelper.enable_persist_data_db = False
        CurrencyExchangeRateDownloader.download_exchange_rate_enabled = False
        ExchangesStorage.exchanges_storage = {}
        self.app = crypto_trader_app.test_client()

    def test_add_crypto_exchange(self):
        response = self.post_add_crypto_currency()
        json_data = response.json
        self.assertEqual(json_data.get("name"), 'exchange_name')
        self.assertEqual(json_data.get("currency"), 'USD')
        self.assertNotEqual(json_data.get("exchange_id"), None)

    def test_add_multiple_crypto_exchanges(self):
        response = self.post_add_crypto_currency()
        json_data = response.json
        self.assertEqual(json_data.get("name"), 'exchange_name')
        self.assertEqual(json_data.get("currency"), 'USD')
        exchange_id = json_data.get("exchange_id")
        self.assertNotEqual(exchange_id, None)

        response = self.app.post(ADD_CRYPTO_EXCHANGE_ROUTE, json={'name': 'exchange_name_2', 'currency': 'EUR'})
        json_data = response.json
        self.assertEqual(json_data.get("name"), 'exchange_name_2')
        self.assertEqual(json_data.get("currency"), 'EUR')
        self.assertNotEqual(json_data.get("exchange_id"), None)

        self.assertNotEqual(json_data.get("exchange_id"), exchange_id)

    def test_add_multiple_crypto_exchanges_same_values(self):
        response = self.post_add_crypto_currency()
        json_data = response.json
        self.assertEqual(json_data.get("name"), 'exchange_name')
        self.assertEqual(json_data.get("currency"), 'USD')
        exchange_id = json_data.get("exchange_id")
        self.assertNotEqual(exchange_id, None)

        response = self.post_add_crypto_currency()
        json_data = response.json
        self.assertEqual(json_data.get("name"), 'exchange_name')
        self.assertEqual(json_data.get("currency"), 'USD')
        self.assertNotEqual(json_data.get("exchange_id"), None)

        self.assertNotEqual(json_data.get("exchange_id"), exchange_id)

    def test_add_crypto_exchange_missing_name(self):
        response = self.app.post(ADD_CRYPTO_EXCHANGE_ROUTE, json={'currency': 'USD'})
        self.assertEqual(response.json, INVALID_DATA_ERROR_JSON_RESPONSE)

    def test_add_crypto_exchange_name_as_int(self):
        response = self.app.post(ADD_CRYPTO_EXCHANGE_ROUTE, json={'name': 123, 'currency': 'USD'})
        self.assertEqual(response.json, INVALID_DATA_ERROR_JSON_RESPONSE)

    def test_add_crypto_exchange_missing_currency(self):
        response = self.app.post(ADD_CRYPTO_EXCHANGE_ROUTE, json={'name': 'exchange_name'})
        self.assertEqual(response.json, INVALID_DATA_ERROR_JSON_RESPONSE)

    def test_add_crypto_exchange_currency_as_int(self):
        response = self.app.post(ADD_CRYPTO_EXCHANGE_ROUTE, json={'name': "name", 'currency': 123})
        self.assertEqual(response.json, INVALID_DATA_ERROR_JSON_RESPONSE)

    def test_add_crypto_exchange_currency_too_long(self):
        response = self.app.post(ADD_CRYPTO_EXCHANGE_ROUTE,
                                 json={'name': "name", 'currency': "asasfadfsdfsdfsdfsfsdfs"})
        self.assertEqual(response.json, INVALID_DATA_ERROR_JSON_RESPONSE)

    def test_add_crypto_exchange_extra_data(self):
        response = self.app.post(ADD_CRYPTO_EXCHANGE_ROUTE,
                                 json={'name': 'exchange_name', 'extra': 'A', 'currency': 'USD'})
        self.assertEqual(response.json, INVALID_DATA_ERROR_JSON_RESPONSE)

    def test_add_crypto_exchange_empty_data(self):
        response = self.app.post(ADD_CRYPTO_EXCHANGE_ROUTE)
        self.assertEqual(response.json, INVALID_DATA_ERROR_JSON_RESPONSE)

    def post_add_crypto_currency(self):
        return self.app.post(ADD_CRYPTO_EXCHANGE_ROUTE, json={'name': 'exchange_name', 'currency': 'USD'})
