# Invalid format input json data
INVALID_DATA_ERROR_JSON_RESPONSE = {"code": 400, "name": "Bad request",
                                    "description": "Invalid format input json data. Read documentation."}
# Invalid exchange_id identifier. e.g empty data, invalid int number, not existing exchange with this id
INCORRECT_EXCHANGE_ID_JSON_RESPONSE = {"code": 400, "name": "Bad request",
                                       "description": "Invalid exchange_id identifier. e.g empty data, invalid int "
                                                      "number, not existing exchange with this id. Read documentation."}
# Negative or invalid amount, unsupported currency(Currency ISO code)
INVALID_AMOUNT_OR_UNKNOWN_CURRENCY_RESPONSE = {"code": 400, "name": "Bad request",
                                               "description": "Negative or invalid amount, unsupported currency("
                                                              "Currency ISO code). Read documentation."}
ANY_CRYPTO_CURRENCIES_JSON_RESPONSE = {"code": 400, "name": "Bad request",
                                       "description": "Missing crypto currencies. Read documentation."}
CREATE_TRADE_FAILED_JSON_RESPONSE = {"code": 400, "name": "Bad request",
                                     "description": "Missing crypto currencies. See documentation or visit root page"}
CREATE_TRADE_FAILED_AMOUNT_HAS_INVALID_VALUE_JSON_RESPONSE = {"code": 400, "name": "Bad request",
                                                              "description": "Missing crypto currencies. Read "
                                                                             "documentation."}
# Valid response when add deposit to exchange finish successfully
ADD_DEPOSIT_RESPONSE_OK = {'success': True, 'code': 200, 'ContentType': 'application/json'}
