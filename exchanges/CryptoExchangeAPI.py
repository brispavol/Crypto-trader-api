import random

from utils.CurrencyExchangeRateDownloader import download_exchange_rate_for_currency
from database.CryptoCurrenciesStorage import CryptoCurrenciesStorage
from database.ExchangesStorage import ExchangesStorage
from exchanges.common.CryptoCurrencyOperations import CryptoCurrenciesOperations
from exchanges.entities.CryptoCurrency import CryptoCurrency
from exchanges.entities.CryptoExchange import CryptoExchange


# Base api for adding new crypto exchange adding deposit to crypto exchange adding crypto currency to exchange
class CryptoExchangeAPI:
    exchanges_storage = None
    crypto_currencies_storage = None

    def __init__(self):
        self.exchanges_storage = ExchangesStorage()
        self.crypto_currencies_storage = CryptoCurrenciesStorage()

    # Create and add new crypto exchange to list of exchanges
    # return new exchange entity
    def add_crypto_exchange(self, name, currency):
        # exchange id is automatically generated
        exchange = CryptoExchange(random.getrandbits(31), name, currency)
        # save to storage
        self.exchanges_storage.add_exchange(exchange)

        return exchange

    # Update existing exchange, e.g. after new trade
    # no return
    def update_crypto_exchange(self, exchange):
        self.exchanges_storage.add_exchange(exchange)

    # Add deposit to exchange(amount=float, currency=ISO code)
    # return true if success
    def add_deposit(self, crypto_exchange, amount, currency):
        # invalid amount value
        if amount <= 0:
            return False

        # deposit currency is not equal exchange currency. Download exchange rate
        if crypto_exchange.currency != currency:
            exchange_rate = download_exchange_rate_for_currency(currency, crypto_exchange.currency)
            float_amount = exchange_rate * amount
            if float_amount == 0:
                return False

            crypto_exchange.amount += float_amount
        else:
            crypto_exchange.amount += amount

        self.exchanges_storage.add_exchange(crypto_exchange)

        return True

    # Handle user action for crypto currency change(ADD, UPDATE, REMOVE)
    # return true if success
    def handle_crypto_currency_change(self, exchange_id, action, name, shortcut, amount, currency_id=0):

        crypto_currency = CryptoCurrency(exchange_id, name, shortcut, amount, currency_id)
        if action == CryptoCurrenciesOperations.ADD.name or \
                action == CryptoCurrenciesOperations.UPDATE.name:
            if currency_id is None:
                crypto_currency.currency_id = random.getrandbits(31)
            self.crypto_currencies_storage.add_crypto_currency(crypto_currency)
            return True

        elif action == CryptoCurrenciesOperations.REMOVE.name:
            self.crypto_currencies_storage.remove_crypto_currency(currency_id)
            return True

        return False

    # update existing crypto currency
    # no return
    def update_crypto_currency(self, crypto_currency):
        self.crypto_currencies_storage.add_crypto_currency(crypto_currency)

    # return exchange depend on exchange id or none
    def get_exchange(self, exchange_id):
        return self.exchanges_storage.get_exchange(exchange_id)

    # return list of exchange depend on exchange id or none
    def get_exchanges(self):
        return self.exchanges_storage.get_exchanges()

    # return list of crypto currencies for given exchange id
    def get_crypto_currencies(self, exchange_id=0):
        return self.crypto_currencies_storage.get_crypto_currencies(exchange_id)

    # return crypto exchange or none
    def get_crypto_currency(self, exchange_id, shortcut):
        return self.crypto_currencies_storage.get_crypto_currency(exchange_id, shortcut)
