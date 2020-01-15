import json

import requests

from utils.ExternalServers import EXCHANGE_RATE_FOR_CRYPTO_CURRENCY_SERVER, EXCHANGE_RATE_FOR_CURRENCY_SERVER
from utils.Logger import log_error

# download_exchange_rate_enabled - if true for adding deposit can be download exchange rate if user insert another
# currency, disabled for tests
download_exchange_rate_enabled = True


# download exchange rate in currency for given crypto currency
# return conversion rate or 1 - default value
def download_exchange_rate_for_crypto_currency(currency, crypto_currency):

    if not download_exchange_rate_enabled:
        return 1

    url = EXCHANGE_RATE_FOR_CRYPTO_CURRENCY_SERVER.format(crypto_currency, currency)
    # key for getting exchange rates
    headers = {'X-CoinAPI-Key': '5DB08D8A-C2DD-4592-AD7E-B7C7F4F875E2'}
    try:
        res = requests.get(url, headers=headers)
        data = json.loads(res.content)["rate"]
        print("Price: " + str(data))
        return data

    except Exception as e:
        log_error(e)

    return 1  # default value


# download exchange rate between in and out currency
# return conversion rate or 1 - default value
def download_exchange_rate_for_currency(currency_in, currency_out):
    if not download_exchange_rate_enabled:
        return 1

    try:
        currencies = currency_in + "_" + currency_out
        url = EXCHANGE_RATE_FOR_CURRENCY_SERVER.format(currencies)
        res = requests.get(url)
        exchange_rate = json.loads(res.content)[currencies]["val"]
        return exchange_rate
    except Exception as e:
        log_error(e)

        return 1  # return default value
