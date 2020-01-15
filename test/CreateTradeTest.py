from unittest import TestCase

from app import crypto_trader_app
from database import SqlLiteDbHelper
from database.CryptoCurrenciesStorage import CryptoCurrenciesStorage
from database.ExchangesStorage import ExchangesStorage
from database.TradesStorage import TradesStorage
from exchanges.CryptoExchangeAPI import CryptoExchangeAPI
from exchanges.entities.CryptoExchange import CryptoExchange
from trade.TradesAPI import TradesAPI
from utils import CurrencyExchangeRateDownloader
from utils.Responses import INVALID_DATA_ERROR_JSON_RESPONSE, INCORRECT_EXCHANGE_ID_JSON_RESPONSE, \
    ANY_CRYPTO_CURRENCIES_JSON_RESPONSE
from utils.Routes import CREATE_TRADE_ROUTE, UPDATE_CRYPTO_CURRENCIES_ROUTE, ADD_DEPOSIT_ROUTE, \
    ADD_CRYPTO_EXCHANGE_ROUTE


# Tests testing creates trades api call
class CreateTradeTest(TestCase):
    crypto_exchanges_api = CryptoExchangeAPI()
    trades_api = TradesAPI()

    def setUp(self):
        SqlLiteDbHelper.enable_persist_data_db = False
        TradesStorage.trades_storage = []
        ExchangesStorage.exchanges_storage = {}
        CryptoCurrenciesStorage.crypto_currencies_storage = {}
        CurrencyExchangeRateDownloader.download_exchange_rate_enabled = False
        self.app = crypto_trader_app.test_client()

    def test_add_trade_to_crypto_currency(self):
        crypto_exchange = self.mock_crypto_exchange()
        crypto_currency = self.mock_crypto_currency(crypto_exchange.exchange_id)
        exchange_id = crypto_exchange.exchange_id
        crypto_exchange_amount = 1000
        crypto_currency_amount = crypto_currency.get('amount')

        response = self.app.post(CREATE_TRADE_ROUTE.format(exchange_id),
                                 json={'amount': 100, 'currency_in': 'USD', 'currency_out': 'BTC'})
        json_data = response.json
        self.assertEqual(True, json_data.get("crypto_currency_amount") > crypto_currency_amount)
        self.assertEqual(True, json_data.get("exchange_amount") < crypto_exchange_amount)

    def test_add_trade_to_crypto_currency_different_currency(self):
        crypto_exchange = self.mock_crypto_exchange()
        crypto_currency = self.mock_crypto_currency(crypto_exchange.exchange_id)
        exchange_id = crypto_exchange.exchange_id
        crypto_exchange_amount = 1000
        crypto_currency_amount = crypto_currency.get('amount')

        response = self.app.post(CREATE_TRADE_ROUTE.format(exchange_id),
                                 json={'amount': 100, 'currency_in': 'CZK', 'currency_out': 'BTC'})
        json_data = response.json
        self.assertEqual(True, json_data.get("crypto_currency_amount") > crypto_currency_amount)
        self.assertEqual(True, json_data.get("exchange_amount") < crypto_exchange_amount)

    def test_add_trade_from_crypto_currency(self):
        crypto_exchange = self.mock_crypto_exchange()
        crypto_currency = self.mock_crypto_currency(crypto_exchange.exchange_id)
        exchange_id = crypto_exchange.exchange_id
        crypto_exchange_amount = 1000
        crypto_currency_amount = crypto_currency.get('amount')
        response = self.app.post(CREATE_TRADE_ROUTE.format(exchange_id),
                                 json={'amount': 10, 'currency_in': 'BTC', 'currency_out': 'USD'})
        json_data = response.json
        self.assertEqual(True, json_data.get("crypto_currency_amount") < crypto_currency_amount)
        self.assertEqual(True, json_data.get("exchange_amount") > crypto_exchange_amount)

    def test_add_trade_from_crypto_currency_different_currency(self):
        crypto_exchange = self.mock_crypto_exchange()
        crypto_currency = self.mock_crypto_currency(crypto_exchange.exchange_id)
        exchange_id = crypto_exchange.exchange_id
        crypto_exchange_amount = 1000
        crypto_currency_amount = crypto_currency.get('amount')
        response = self.app.post(CREATE_TRADE_ROUTE.format(exchange_id),
                                 json={'amount': 10, 'currency_in': 'BTC', 'currency_out': 'CZK'})
        json_data = response.json
        self.assertEqual(True, json_data.get("crypto_currency_amount") < crypto_currency_amount)
        self.assertEqual(True, json_data.get("exchange_amount") > crypto_exchange_amount)

    def test_add_trade_invalid_exchange_id(self):
        response = self.app.post(CREATE_TRADE_ROUTE.format(0),
                                 json={'amount': 10, 'currency_in': 'BTC', 'currency_out': 'CZK'})
        json_data = response.json
        self.assertEqual(INCORRECT_EXCHANGE_ID_JSON_RESPONSE, json_data)

    def test_add_trade_string_exchange_id(self):
        response = self.app.post(CREATE_TRADE_ROUTE.format("STRING_ID"),
                                 json={'amount': 10, 'currency_in': 'BTC', 'currency_out': 'CZK'})
        json_data = response.json
        self.assertEqual(INCORRECT_EXCHANGE_ID_JSON_RESPONSE, json_data)

    def test_add_trade_invalid_currency(self):
        crypto_exchange = self.mock_crypto_exchange()
        self.mock_crypto_currency(crypto_exchange.exchange_id)
        exchange_id = crypto_exchange.exchange_id
        response = self.app.post(CREATE_TRADE_ROUTE.format(exchange_id),
                                 json={'amount': 10, 'currency_in': 'BTCg', 'currency_out': 'CZK'})
        json_data = response.json
        self.assertEqual(INVALID_DATA_ERROR_JSON_RESPONSE, json_data)

    def test_add_trade_invalid_amount(self):
        crypto_exchange = self.mock_crypto_exchange()
        self.mock_crypto_currency(crypto_exchange.exchange_id)
        exchange_id = crypto_exchange.exchange_id
        response = self.app.post(CREATE_TRADE_ROUTE.format(exchange_id),
                                 json={'amount': "A", 'currency_in': 'BTC', 'currency_out': 'CZK'})
        json_data = response.json
        self.assertEqual(INVALID_DATA_ERROR_JSON_RESPONSE, json_data)

    def test_add_trade_unknown_currency(self):
        crypto_exchange = self.mock_crypto_exchange()
        self.mock_crypto_currency(crypto_exchange.exchange_id)
        exchange_id = crypto_exchange.exchange_id
        response = self.app.post(CREATE_TRADE_ROUTE.format(exchange_id),
                                 json={'amount': 10, 'currency_in': 'BTd', 'currency_out': 'CZK'})
        json_data = response.json
        self.assertEqual(ANY_CRYPTO_CURRENCIES_JSON_RESPONSE, json_data)

    def post_add_crypto_currency(self):
        return self.app.post(ADD_CRYPTO_EXCHANGE_ROUTE, json={'name': 'exchange_name', 'currency': 'USD'})

    def mock_crypto_exchange(self):
        response = self.post_add_crypto_currency()
        json_data = response.json
        return CryptoExchange(json_data.get("exchange_id"),
                              json_data.get("name"),
                              json_data.get("currency"),
                              json_data.get("amount"))

    def mock_crypto_currency(self, exchange_id):
        self.app.post(ADD_DEPOSIT_ROUTE + str(exchange_id), json={'amount': 1000, 'currency': 'USD'})
        response = self.app.put(UPDATE_CRYPTO_CURRENCIES_ROUTE.format(exchange_id),
                                json={'action': 'ADD', 'name': 'Bitcoin', 'shortcut': 'BTC', 'amount': 10})
        json_data = response.json[0]
        return json_data
