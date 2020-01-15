from database import SqlLiteDbHelper
from database.SqlLiteDbHelper import save_crypto_currency_to_db, remove_crypto_currency_to_db, \
    load_crypto_currencies


# Storage persists list of crypto currencies
class CryptoCurrenciesStorage:
    crypto_currencies_storage = {}
    __data_loaded_from_db = False

    # add new crypto currency to existing currencies
    def add_crypto_currency(self, crypto_currency):

        save_crypto_currency_to_db(crypto_currency)

        self.crypto_currencies_storage[crypto_currency.currency_id] = crypto_currency

    # remove existing crypto currency
    def remove_crypto_currency(self, currency_id):
        remove_crypto_currency_to_db(id)

        self.crypto_currencies_storage.pop(currency_id, 'No Key found')

    # return list of crypto currencies depend on exchange_id
    def get_crypto_currencies(self, exchange_id):
        # if data is not loaded from db, will be loaded
        if SqlLiteDbHelper.enable_persist_data_db and not self.__data_loaded_from_db:
            self.crypto_currencies_storage = load_crypto_currencies(None)
            self.__data_loaded_from_db = True

        result = []
        for crypto_currency in self.crypto_currencies_storage.values():
            if exchange_id is None or crypto_currency.exchange_id == exchange_id:
                result.append(crypto_currency)

        return result

    # return crypto currency or None if not exist
    def get_crypto_currency(self, exchange_id, shortcut):

        # if data is not loaded from db, will be loaded
        if SqlLiteDbHelper.enable_persist_data_db and not self.__data_loaded_from_db:
            self.crypto_currencies_storage = load_crypto_currencies(None)
            self.__data_loaded_from_db = True

        for crypto_currency in self.crypto_currencies_storage.values():
            if crypto_currency.exchange_id == exchange_id and crypto_currency.shortcut == shortcut:
                return crypto_currency

        return None
