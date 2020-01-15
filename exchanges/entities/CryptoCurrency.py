# Entity contains all data for crypto currency, e.g name, symbol, amount, ...
class CryptoCurrency:
    currency_id = 0
    name = ""
    shortcut = ""
    exchange_id = 0
    amount = 0.0

    def __init__(self, exchange_id, name, shortcut, amount=0.0, currency_id=0):
        self.name = name
        self.shortcut = shortcut
        self.exchange_id = exchange_id
        if amount is not None:
            self.amount = amount
        self.currency_id = currency_id

    def to_dictionary(self):
        return {'currency_id': self.currency_id,
                'exchange_id': self.exchange_id,
                'name': self.name,
                'shortcut': self.shortcut,
                'amount': self.amount}
