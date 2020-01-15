# Crypto Trader API in Python

# Overview

Crypto Trader API is an example project which demonstrates my knowledge from python.  
Project has been written in Python using Flask.  
Project uses SQLite database for persisting data.  
Project has more than 24 python files and more than 40 unit tests methods.

# Requirements

• Python 3.8  
• Works on Mac OSX, Linux, Windows.  

# Development environment

• Pycharm Professional  
• Postman 2  

# APIs and Documentation

## ADD crypto exchange

**POST /api/v1/crypto/exchanges**  
Example:  
{"name": "exchange_name", "currency": "USD"}  

Request is validated by:  
CRYPTO_EXCHANGE_SCHEMA = Schema({"name": And(str, lambda s: 0 < len(s) <= 250), "currency": And(str, lambda s: len(s) == 3)})  

if validation is OK, will be generated exchange id and saved to db.  
Response: {"amount": 0.0, "currency": "USD", "exchange_id": 436583595, "name": "exchange_name"}  

For this API has been written 10 unit tests.  

**FOR TESTING PURPOSES**  
**GET /api/v1/crypto/exchanges** – return json representation all exchanges  

## Deposit exchange

**POST /api/v1/crypto/exchanges/{exchange_id}**  
Example:  
{"amount": 1000, "currency": "USD"}  

**Preconditions:**  
Valid exchange_id – has to be number  
Request is validated by: ADD_DEPOSIT_SCHEMA = Schema({"amount": Or(float, int, lambda s: s < 1000000), "currency": And(str, lambda s: len(s) == 3)})  

If amount is another currency will be recalculated to exchange currency by thirty web service. if validation is OK, will be updated exchange and saved to db.  
Response:  
{"success": True, "code": 200, "ContentType": "application/json"}  

For this API has been written 10 unit tests.  
**FOR TESTING PURPOSES**  
**GET /api/v1/crypto/exchanges/{exchange_id}** – return json representation exchange with given exchange id  

## Update crypto currencies within exchange

**PUT /api/v1/crypto/exchanges/{exchange_id}/currencies**  
Example:  
{"action": "ADD", "name": "Bitcoin", "shortcut": "BTC", "amount": 5}  
{"action": "UPDATE", "name": "Bitcoin", "shortcut": "BTC", "amount": 5, "currency_id": 123}  
{"action": "REMOVE", "name": "Bitcoin", "shortcut": "BTC", "currency_id": 123}  

**Preconditions:**  
Valid exchange_id – has to be number  
Request is validated by:  
CRYPTO_CURRENCY_SCHEMA = Schema({ "action": Or("ADD", "UPDATE", "REMOVE"), "name": And(str, lambda s: 0 < len(s) <= 250), "shortcut": And(str, lambda s: len(s) == 3), Optional("amount"): And(Or(float, int), lambda s: s < 1000000), Optional("currency_id"): int })  

if validation is OK, will be created crypto exchange and saved to db.  
Response:  
[{"amount": 0.0, "currency_id": 1733229929, "exchange_id": 2015236545, "name": "Bitcoin", "shortcut": "BTC"}]  

For this API has been written 9 unit tests.  
**FOR TESTING PURPOSES**  
**GET /api/v1/crypto/exchanges/{exchange_id}/currencies** – return json representation crypto currencies with given exchange id  

## Create trade

**POST /api/v1/crypto/exchanges/{exchange_id}/trades**  
Example:  
{"amount": 10, "currency_in": "BTC", "currency_out": "USD"} {"amount": 10, "currency_in": "BTC", "currency_out": "USD"}  

**Preconditions:**  
Valid exchange_id – has to be number  
Request is validated by: TRADE_SCHEMA = Schema({ "amount": And(Or(float, int), lambda s: s < 1000000), "currency_in": And(str, len, lambda s: len(s) == 3), "currency_out": And(str, lambda s: len(s) == 3), })  

if trade is to crypto currency than trade.amount <= exchange.amount  
if trade is from crypto currency than trade.amount <= crypto currency.amount  
if validation is OK, will be updated exchange, crypto currency and trade and all will be saved to db.  
Response:  
{"crypto_currency_amount": 110.0, "exchange_amount": 900.0, "previous_crypto_currency_amount": 10, "previous_exchange_amount": 1000.0}  

For this API has been written 9 unit tests.  
**FOR TESTING PURPOSES**  
**GET /api/v1/crypto/exchanges/{exchange_id}/trades** – return json representation trades with given exchange id  

## History of trades

**GET /api/v1/crypto/history?offset={offset}&limit={limit}&exchange_id={exchange_id} &search={search}&date_from={date_from}&date_to={date_to}**  

date_from: (String) - “2019-10-23T12:12:12Z”  
date_to: (String) - “2019-10-23T12:12:12Z”  
exchange_id: (Integer)  
search: (String)  
offset: (Integer)  
limit: (Integer)  

Response:  
[{"amount": 100, "amount_out": 100.0, "created": "2020-01-14T22:05:47Z", "currency_in": "USD", "currency_out": "BTC", "exchange_id": 338851043}]  

For this API has been written 3 unit tests.  

**FOR TESTING PURPOSES**  

## Mock test data

**POST /api/v1/crypto/exchanges/test**  
Add 2 exchanges, for every exchange add deposit and crypto currencies and make trade  

**FOR TESTING PURPOSES**  
**GET /api/v1/crypto/exchanges/test** – return json representation all persisted data, and exceptions log  

## Remove db data

**GET /api/v1/crypto/exchanges/test_remove_data** - Remove all tables from db:  

## Documentation

**GET /** - This documentation  

**GET /api/v1/crypto/exchanges/** - This documentation  

# Some important files:

**app.py** - main flask application  

**CryptoExchangeAPI** - base logic for exchanges and crypto currencies  
**TradesAPI** - base logic for trades  
**SqlLiteDbHelper - crypto exchanges db(exchanges, crypto currencies, trades tables)**  
**CurrencyExchangeRateDownloader** - convert currencies via thirty-party apis  
**DebugHelper** - prints data to json format - for debugging  
**ExternalServers** - list of external api services  
**JsonSchema** - list of validation json schema for input data  
**Logger** - log exceptions  
**Responses** - list of error responses for api calls  
**Routes** - list of supported routes  
**AddCryptoExchangeTest** - test api call for adding exchanges  
**AddDepositTest** - test api call for adding deposit  
**UpdateCryptoCurrenciesTest** - test api call for modifying crypto currencies  
**CreateTradeTest** - test api call for creates trades  
**GetTradesTest** - test api call for getting list of trades