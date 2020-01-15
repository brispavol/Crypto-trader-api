

# Entity contains all data for new trade


class Trade:
    amount = 0.0
    amount_out = 0.0
    currency_in = ""
    currency_out = ""
    exchange_id = 0
    timestamp = 0.0

    def __init__(self, amount, amount_out, currency_in, currency_out, exchange_id, timestamp=0.0):
        self.amount = amount
        self.amount_out = amount_out
        self.currency_in = currency_in
        self.currency_out = currency_out
        self.exchange_id = exchange_id
        if timestamp == 0.0:
            from datetime import datetime
            self.timestamp = datetime.timestamp(datetime.now())
        else:
            self.timestamp = timestamp

    def to_dictionary(self):
        import datetime
        converted_datetime = datetime.datetime.fromtimestamp(self.timestamp)
        converted_datetime_string = converted_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')

        data = {'amount': self.amount,
                'amount_out': self.amount_out,
                'currency_in': self.currency_in,
                'currency_out': self.currency_out,
                'exchange_id': self.exchange_id,
                'created': converted_datetime_string}

        return data
