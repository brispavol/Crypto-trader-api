from unittest import TestCase

from app import crypto_trader_app
from database import SqlLiteDbHelper
from database.ExchangesStorage import ExchangesStorage
from utils import CurrencyExchangeRateDownloader
from utils.Responses import INVALID_DATA_ERROR_JSON_RESPONSE, INCORRECT_EXCHANGE_ID_JSON_RESPONSE, \
    INVALID_AMOUNT_OR_UNKNOWN_CURRENCY_RESPONSE
from utils.Routes import ADD_DEPOSIT_ROUTE, ADD_CRYPTO_EXCHANGE_ROUTE


# Tests testing add deposit to exchange
class AddDepositTest(TestCase):

    def setUp(self):
        SqlLiteDbHelper.enable_persist_data_db = False
        CurrencyExchangeRateDownloader.download_exchange_rate_enabled = False
        ExchangesStorage.exchanges_storage = {}
        self.app = crypto_trader_app.test_client()

    def test_add_deposit(self):
        exchange_id = self.mock_crypto_exchange()
        response = self.app.post(ADD_DEPOSIT_ROUTE + str(exchange_id), json={'amount': 1000, 'currency': 'USD'})
        json_data = response.json
        self.assertEqual(200, json_data.get("code"))
        response = self.app.get(ADD_DEPOSIT_ROUTE + str(exchange_id))
        self.assertEqual(1000.0, response.get_json().get('amount'))

    def test_multiple_add_deposit(self):
        exchange_id = self.mock_crypto_exchange()
        self.app.post(ADD_DEPOSIT_ROUTE + str(exchange_id), json={'amount': 1000, 'currency': 'USD'})
        self.app.post(ADD_DEPOSIT_ROUTE + str(exchange_id), json={'amount': 1000, 'currency': 'USD'})
        response = self.app.get(ADD_DEPOSIT_ROUTE + str(exchange_id))
        self.assertEqual(2000.0, response.get_json().get('amount'))

    def test_add_deposit_invalid_exchange_id(self):
        response = self.app.post(ADD_DEPOSIT_ROUTE + str(0), json={'amount': 1000, 'currency': 'USD'})
        json_data = response.json
        self.assertEqual(INCORRECT_EXCHANGE_ID_JSON_RESPONSE, json_data)

    def test_add_deposit_string_exchange_id(self):
        response = self.app.post(ADD_DEPOSIT_ROUTE + "STRING_ID", json={'amount': 1000, 'currency': 'USD'})
        json_data = response.json
        self.assertEqual(INCORRECT_EXCHANGE_ID_JSON_RESPONSE, json_data)

    def test_add_deposit_invalid_currency(self):
        exchange_id = self.mock_crypto_exchange()
        response = self.app.post(ADD_DEPOSIT_ROUTE + str(exchange_id), json={'amount': 1000, 'currendcy': 'USD'})
        json_data = response.json
        self.assertEqual(INVALID_DATA_ERROR_JSON_RESPONSE, json_data)

    def test_add_deposit_invalid_amount(self):
        exchange_id = self.mock_crypto_exchange()
        response = self.app.post(ADD_DEPOSIT_ROUTE + str(exchange_id), json={'amount': "aa", 'currency': 'USD'})
        json_data = response.json
        self.assertEqual(INVALID_DATA_ERROR_JSON_RESPONSE, json_data)

    def test_add_deposit_negative_amount(self):
        exchange_id = self.mock_crypto_exchange()
        response = self.app.post(ADD_DEPOSIT_ROUTE + str(exchange_id), json={'amount': -1000, 'currency': 'USD'})
        json_data = response.json
        self.assertEqual(INVALID_AMOUNT_OR_UNKNOWN_CURRENCY_RESPONSE, json_data)

    def test_add_deposit_another_currency(self):
        exchange_id = self.mock_crypto_exchange()
        self.app.post(ADD_DEPOSIT_ROUTE + str(exchange_id), json={'amount': 1000, 'currency': 'CZK'})
        response = self.app.get(ADD_DEPOSIT_ROUTE + str(exchange_id))
        self.assertEqual(True, response.get_json().get('amount') > 0)

    def post_add_crypto_currency(self):
        return self.app.post(ADD_CRYPTO_EXCHANGE_ROUTE, json={'name': 'exchange_name', 'currency': 'USD'})

    def mock_crypto_exchange(self):
        response = self.post_add_crypto_currency()
        json_data = response.json
        exchange_id = json_data.get("exchange_id")
        return exchange_id
