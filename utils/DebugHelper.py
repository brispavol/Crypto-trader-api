from flask import jsonify

from utils import Logger

crypto_exchanges_storage = None


# print debug messages for crypto exchanges
class DebugHelper:

    @staticmethod
    def print_debug_crypto_exchanges(exchanges):
        exchanges_list = []
        for exchange in exchanges:
            exchanges_list.append(exchange.to_dictionary())
        return jsonify(exchanges_list)

    @staticmethod
    def print_debug_crypto_exchange(exchange):
        return jsonify(exchange.to_dictionary())

    @staticmethod
    def print_debug_crypto_currencies(crypto_currencies):
        crypto_currencies_list = []
        for crypto_currency in crypto_currencies:
            crypto_currencies_list.append(crypto_currency.to_dictionary())
        return jsonify(crypto_currencies_list)

    @staticmethod
    def print_debug_trades(trades):
        trades_list = []
        for trade in trades:
            trades_list.append(trade.to_dictionary())

        return jsonify(trades_list)

    @staticmethod
    def print_all(exchanges, crypto_currencies, trades):
        results_list = []
        for exchange in exchanges:
            exchange_items = [exchange.to_dictionary()]

            for crypto_currency in crypto_currencies:
                if crypto_currency.exchange_id == exchange.exchange_id:
                    exchange_items.append(crypto_currency.to_dictionary())

            for trade in trades:
                if trade.exchange_id == exchange.exchange_id:
                    exchange_items.append(trade.to_dictionary())
            results_list.append(exchange_items)

        try:

            for error in Logger.errors:
                results_list.append({'error': ''.join(error.args)})

            # reset exceptions cache
            Logger.errors = []
        except TypeError:
            pass

        return jsonify(results_list)
