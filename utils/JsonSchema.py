from schema import Schema, And, Or, Optional

# Json validation schema for adding new crypto exchange
CRYPTO_EXCHANGE_SCHEMA = Schema({'name': And(str, lambda s: 0 < len(s) <= 50),
                                 'currency': And(str, lambda s: len(s) == 3)})

# Json validation schema for adding deposit to existing crypto exchange
ADD_DEPOSIT_SCHEMA = Schema({'amount': And(Or(float, int), lambda s: s < 1000000),
                             'currency': And(str, lambda s: len(s) == 3)})

# Json validation schema for adding/updating or remove crypto currency
CRYPTO_CURRENCY_SCHEMA = Schema({
    'action': Or('ADD', 'UPDATE', 'REMOVE'),
    'name': And(str, lambda s: 0 < len(s) <= 250),
    'shortcut': And(str, lambda s: len(s) == 3),
    Optional('amount'): And(Or(float, int), lambda s: s < 1000000),
    Optional('currency_id'): int
})

# Json validation schema for new trade
TRADE_SCHEMA = Schema({
    'amount': And(Or(float, int), lambda s: s < 1000000),
    'currency_in': And(str, len, lambda s: len(s) == 3),
    'currency_out': And(str, lambda s: len(s) == 3),
})
