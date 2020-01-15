from database.SqlLiteDbHelper import save_crypto_exchange_to_db, load_crypto_exchanges_from_db


# Storage persists list of crypto exchanges
class ExchangesStorage:
    exchanges_storage = {}

    def __init__(self):
        self.exchanges_storage = load_crypto_exchanges_from_db()

    # return exchange or None
    def get_exchange(self, exchange_id):
        return self.exchanges_storage.get(exchange_id)

    # return list of all exchanges
    def get_exchanges(self):
        return self.exchanges_storage.values()

    # add new crypto exchange
    def add_exchange(self, exchange):
        save_crypto_exchange_to_db(exchange)

        self.exchanges_storage[exchange.exchange_id] = exchange
