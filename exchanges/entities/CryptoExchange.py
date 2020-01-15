# Entity contains all data for crypto exchange, e.g. id, name, ...
class CryptoExchange:
    exchange_id = 0
    name = ""
    currency = "USD"
    amount = 0.0

    def __init__(self, exchange_id, name, currency, amount=0.0):
        self.exchange_id = exchange_id
        self.name = name
        self.currency = currency
        self.amount = amount

    def to_dictionary(self):
        data = {'name': self.name,
                'exchange_id': self.exchange_id,
                'currency': self.currency,
                'amount': self.amount}

        return data
