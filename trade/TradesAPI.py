from database.TradesStorage import TradesStorage
from trade.Trade import Trade

from utils.CurrencyExchangeRateDownloader import download_exchange_rate_for_crypto_currency, \
    download_exchange_rate_for_currency


# Base api for making trades in the crypto exchange
class TradesAPI:
    trades_storage = TradesStorage()

    # Create trade from/to crypto currency
    # Exchange amount to valid currency if is needed
    # trade if everything is ok or None
    @staticmethod
    def create_trade(exchange_currency, convert_to_crypto, exchange_id, amount, currency_in,
                     currency_out):
        converted_amount = 0.0
        if convert_to_crypto:
            if exchange_currency == currency_in:
                exchange_rate = download_exchange_rate_for_crypto_currency(currency_in, currency_out)
                amount_out = amount / exchange_rate
            else:
                exchange_rate = download_exchange_rate_for_currency(currency_in, exchange_currency)
                converted_amount = exchange_rate * amount
                exchange_rate = download_exchange_rate_for_crypto_currency(exchange_currency, currency_out)
                amount_out = amount / exchange_rate
        else:
            if exchange_currency == currency_out:
                exchange_rate = download_exchange_rate_for_crypto_currency(currency_out, currency_in)
                amount_out = amount * exchange_rate
            else:
                exchange_rate = download_exchange_rate_for_crypto_currency(exchange_currency, currency_in)
                amount_out = amount * exchange_rate

        # amount has invalid value
        if amount_out <= 0.0:
            return None

        trade = Trade(amount, amount_out, currency_in, currency_out, exchange_id)
        if converted_amount > 0:
            trade.amount = converted_amount
        # everything ok return trade
        return trade

    # trade was validated, will be persisted to storage
    def save_trade(self, trade):
        self.trades_storage.save(trade)

    # return list of trades depend on filter conditions
    def get_trades(self, exchange_id=0, offset=0, limit=-1, search='', date_from=None, date_to=None):
        return self.trades_storage.get_trades(exchange_id, offset, limit, search, date_from, date_to)
