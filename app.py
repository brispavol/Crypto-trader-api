import requests
from flask import Flask, request, jsonify, render_template

from database.CryptoCurrenciesStorage import CryptoCurrenciesStorage
from database.ExchangesStorage import ExchangesStorage
from database.SqlLiteDbHelper import remove_all_data
from database.TradesStorage import TradesStorage
from exchanges.CryptoExchangeAPI import CryptoExchangeAPI
from trade.TradesAPI import TradesAPI
from utils.DebugHelper import DebugHelper
from utils.JsonSchema import CRYPTO_EXCHANGE_SCHEMA, ADD_DEPOSIT_SCHEMA, TRADE_SCHEMA, CRYPTO_CURRENCY_SCHEMA
from utils.Responses import INVALID_DATA_ERROR_JSON_RESPONSE, INCORRECT_EXCHANGE_ID_JSON_RESPONSE, \
    INVALID_AMOUNT_OR_UNKNOWN_CURRENCY_RESPONSE, ANY_CRYPTO_CURRENCIES_JSON_RESPONSE, \
    CREATE_TRADE_FAILED_JSON_RESPONSE, \
    CREATE_TRADE_FAILED_AMOUNT_HAS_INVALID_VALUE_JSON_RESPONSE, ADD_DEPOSIT_RESPONSE_OK
from utils.Routes import GET_TRADES_ROUTE, CREATE_TRADE_ROUTE, EXCHANGE_ID, UPDATE_CRYPTO_CURRENCIES_ROUTE, \
    ADD_DEPOSIT_ROUTE, ADD_CRYPTO_EXCHANGE_ROUTE, ROOT_ROUTE, MAIN_ROUTE

crypto_trader_app = Flask(__name__)
exchange_api = CryptoExchangeAPI()
trades_api = TradesAPI()


@crypto_trader_app.route(MAIN_ROUTE)
@crypto_trader_app.route(ROOT_ROUTE)
def root():
    return render_template("home.html")


# API try create new crypto exchange
# POST request - valid json data - CRYPTO_EXCHANGE_SCHEMA
# return list of errors see Responses if something failed
# return json representation new created crypto exchange
@crypto_trader_app.route(ADD_CRYPTO_EXCHANGE_ROUTE, methods=['GET', 'POST'])
def add_crypto_exchange():
    if request.method == 'POST':
        json_data = request.get_json()
        if json_data is None or not CRYPTO_EXCHANGE_SCHEMA.is_valid(json_data):
            return INVALID_DATA_ERROR_JSON_RESPONSE

        # try add crypto exchange
        crypto_exchange = __get_exchanges_api().add_crypto_exchange(json_data.get('name'), json_data.get('currency'))
        # everything OK return valid response
        return crypto_exchange.to_dictionary()

    # print debug json representation all crypto exchanges
    return DebugHelper.print_debug_crypto_exchanges(__get_exchanges_api().get_exchanges())


# API try add deposit to existing crypto exchange
# Required valid exchange_id
# POST request - valid json data - ADD_DEPOSIT_SCHEMA
# if currency != exchange currency will be converted
# return list of errors see Responses if something failed
# return ADD_DEPOSIT_RESPONSE_OK if deposit was added to exchange
@crypto_trader_app.route(ADD_DEPOSIT_ROUTE + EXCHANGE_ID, methods=['GET', 'POST'])
def add_deposit(exchange_id):
    # validate exchange id
    crypto_exchange = __get_crypto_exchange(exchange_id)
    if crypto_exchange is None:
        return INCORRECT_EXCHANGE_ID_JSON_RESPONSE

    if request.method == 'POST':
        json_data = request.get_json()
        if not ADD_DEPOSIT_SCHEMA.is_valid(json_data):
            return INVALID_DATA_ERROR_JSON_RESPONSE

        # amount has to be number
        amount = json_data.get('amount')
        # try add deposit if everything ok return success
        if __get_exchanges_api().add_deposit(crypto_exchange, amount, json_data.get('currency')):
            return ADD_DEPOSIT_RESPONSE_OK
        else:
            # something failed, return error
            return INVALID_AMOUNT_OR_UNKNOWN_CURRENCY_RESPONSE

    # print debug json representation crypto exchange
    return DebugHelper.print_debug_crypto_exchange(crypto_exchange)


# API try add/update/remove crypto currency list of existing crypto currencies in crypto exchange
# Required valid exchange_id
# PUT request - valid json data - CRYPTO_CURRENCY_SCHEMA
# return list of errors see Responses if something failed
# return ADD_DEPOSIT_RESPONSE_OK if deposit was added to exchange
@crypto_trader_app.route(UPDATE_CRYPTO_CURRENCIES_ROUTE.format(EXCHANGE_ID), methods=['GET', 'PUT'])
def update_crypto_currencies(exchange_id):
    # validate exchange id
    crypto_exchange = __get_crypto_exchange(exchange_id)
    if crypto_exchange is None:
        return INCORRECT_EXCHANGE_ID_JSON_RESPONSE

    exchange_id = int(exchange_id)
    if request.method == 'PUT':
        json_data = request.get_json()
        # validate json data
        if not CRYPTO_CURRENCY_SCHEMA.is_valid(json_data):
            return INVALID_DATA_ERROR_JSON_RESPONSE

        # try add/update or remove crypto currency
        if __get_exchanges_api().handle_crypto_currency_change(exchange_id,
                                                               json_data.get('action'),
                                                               json_data.get('name'),
                                                               json_data.get('shortcut'),
                                                               json_data.get('amount'),
                                                               json_data.get('currency_id')):
            # everything ok return valid response
            result = []
            for crypto_currency in __get_exchanges_api().get_crypto_currencies(exchange_id):
                result.append(crypto_currency.to_dictionary())

            return jsonify(result)
        # something failed
        else:
            return INVALID_DATA_ERROR_JSON_RESPONSE

    # print debug json representation crypto currencies for exchange
    return DebugHelper.print_debug_crypto_currencies(__get_exchanges_api().get_crypto_currencies(exchange_id))


# API try create trade between exchange amount and crypto currency amount and vice versa
# Required valid exchange_id
# POST request - valid json data - TRADE_SCHEMA
# return list of errors see Responses if something failed
# return json value about trade
@crypto_trader_app.route(CREATE_TRADE_ROUTE.format(EXCHANGE_ID), methods=['GET', 'POST'])
def create_trade(exchange_id):
    # validate exchange id
    crypto_exchange = __get_crypto_exchange(exchange_id)
    if crypto_exchange is None:
        return INCORRECT_EXCHANGE_ID_JSON_RESPONSE

    exchange_id = int(exchange_id)
    if request.method == 'POST':
        json_data = request.get_json()
        # validate schema
        if not TRADE_SCHEMA.is_valid(json_data):
            return INVALID_DATA_ERROR_JSON_RESPONSE

        currency_in = json_data.get('currency_in')
        currency_out = json_data.get('currency_out')
        # is exchange from crypto currency to normal currency
        crypto_currency = __get_exchanges_api().get_crypto_currency(exchange_id, currency_in)
        if crypto_currency is None:
            # is exchange from normal currency to crypto currency
            crypto_currency = __get_exchanges_api().get_crypto_currency(exchange_id, currency_out)
            # missing crypto currency shortcut
            if crypto_currency is None:
                return ANY_CRYPTO_CURRENCIES_JSON_RESPONSE
            convert_to_crypto_currency = True
        else:
            convert_to_crypto_currency = False

        exchange_amount = crypto_exchange.amount
        crypto_currency_amount = crypto_currency.amount

        amount = json_data.get('amount')
        # is valid amount
        if amount <= 0:
            return CREATE_TRADE_FAILED_AMOUNT_HAS_INVALID_VALUE_JSON_RESPONSE

        # try make a trade
        trade = __get_trades_api().create_trade(crypto_exchange.currency, convert_to_crypto_currency,
                                                exchange_id,
                                                amount,
                                                currency_in,
                                                currency_out)
        # making trade failed
        if trade is None:
            return CREATE_TRADE_FAILED_JSON_RESPONSE

        if not __handle_trade_result(convert_to_crypto_currency, crypto_exchange, crypto_currency, trade):
            return CREATE_TRADE_FAILED_AMOUNT_HAS_INVALID_VALUE_JSON_RESPONSE

        return {"previous_exchange_amount": exchange_amount,
                "exchange_amount": crypto_exchange.amount,
                "previous_crypto_currency_amount": crypto_currency_amount,
                "crypto_currency_amount": crypto_currency.amount}

    # print debug json representation trades for exchange
    return DebugHelper.print_debug_trades(__get_trades_api().get_trades(exchange_id))


# API try get list of trades
# GET request - filter arguments are optional
# return list of errors see Responses if something failed
# return json representation of data
@crypto_trader_app.route(GET_TRADES_ROUTE, methods=['GET'])
def get_trades():
    if request.method == 'GET':
        exchange_id = request.args.get("exchange_id")
        if exchange_id is not None and exchange_id.isdigit():
            exchange_id = int(exchange_id)
        else:
            exchange_id = None

        offset = request.args.get("offset")
        if offset is not None and offset.isdigit():
            offset = int(offset)
        else:
            offset = None

        limit = request.args.get("limit")
        if limit is not None and limit.isdigit():
            limit = int(limit)
        else:
            limit = None
        search = request.args.get("search")
        date_from = request.args.get("date_from")
        date_to = request.args.get("date_to")

        # get data from storage
        trades = __get_trades_api().get_trades(exchange_id, offset, limit, search, date_from, date_to)

        trades_list = []
        for trade in trades:
            trades_list.append(trade.to_dictionary())

        # return json representation of data
        return jsonify(trades_list)


# Base api for operations with exchanges
def __get_exchanges_api():
    return exchange_api


# Base api for operations with trades
def __get_trades_api():
    return trades_api


@crypto_trader_app.route('/api/v1/crypto/exchanges/test', methods=['GET', 'POST'])
def test_data():
    res = requests.post('http://127.0.0.1:5000/api/v1/crypto/exchanges',
                        json={'name': 'exchange_name', 'currency': 'USD'})
    json_data = res.json()
    exchange_id_first = json_data.get('exchange_id')
    url = 'http://127.0.0.1:5000/api/v1/crypto/exchanges/{}'.format(exchange_id_first)
    requests.post(url, json={'amount': 1000, 'currency': 'USD'})
    requests.post(url, json={'amount': 1000.0, 'currency': 'CZK'})

    url = 'http://127.0.0.1:5000/api/v1/crypto/exchanges/{}/currencies'.format(exchange_id_first)
    requests.put(url, json={'action': 'ADD', 'name': 'Bitcoin', 'shortcut': 'BTC', 'amount': 10})
    requests.put(url, json={'action': 'ADD', 'name': 'Ripple', 'shortcut': 'XRP'})

    url = 'http://127.0.0.1:5000/api/v1/crypto/exchanges/{}/trades'.format(exchange_id_first)
    requests.post(url, json={'amount': 100, 'currency_in': 'USD', 'currency_out': 'BTC'})
    requests.post(url, json={'amount': 5, 'currency_in': 'BTC', 'currency_out': 'USD'})

    # print debug json representation trades for exchange
    return DebugHelper.print_all(__get_exchanges_api().get_exchanges(),
                                 __get_exchanges_api().get_crypto_currencies(None),
                                 __get_trades_api().get_trades(None))


# only for testing
# will be removed from production code
@crypto_trader_app.route('/api/v1/crypto/exchanges/test_remove_data', methods=['GET'])
def remove_db_data():
    remove_all_data()
    __get_exchanges_api().exchanges_storage.exchanges_storage = {}
    __get_exchanges_api().crypto_currencies_storage.crypto_currencies_storage = {}
    __get_trades_api().trades_storage.trades_storage = []
    return {'success': True, 'code': 200, 'ContentType': 'application/json'}


# validate exchange id
# return crypto exchange for given exchange id or None
def __get_crypto_exchange(exchange_id):
    # exchange_id has to be number
    if not exchange_id.isdigit():
        return None

    exchange_id = int(exchange_id)
    return __get_exchanges_api().get_exchange(exchange_id)


# validate trade trade amount < exchange amount, ..
# if validation was success will be updated amount for exchange and crypto currency
# return true if success otherwise false
def __handle_trade_result(convert_to_crypto_currency, crypto_exchange, crypto_currency, trade):
    # trade was success
    if convert_to_crypto_currency:
        if crypto_exchange.amount < trade.amount:
            return False

        crypto_exchange.amount -= trade.amount
        crypto_currency.amount += trade.amount_out

    else:
        if crypto_currency.amount < trade.amount:
            return False

        crypto_exchange.amount += trade.amount_out
        crypto_currency.amount -= trade.amount

    __get_trades_api().save_trade(trade)

    # update amount in crypto exchange
    __get_exchanges_api().update_crypto_exchange(crypto_exchange)
    # update amount for crypto currency
    __get_exchanges_api().update_crypto_currency(crypto_currency)

    return True


if __name__ == '__main__':
    crypto_trader_app.run('0.0.0.0', 5000)
