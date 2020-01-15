import sqlite3

from exchanges.entities.CryptoCurrency import CryptoCurrency
from exchanges.entities.CryptoExchange import CryptoExchange
from trade.Trade import Trade
from utils.Logger import log_error

# if false persist data to db will be disabled, disabled for tests
enable_persist_data_db = True


# load all crypto exchanges from db
# return dictionary(exchange_id = exchange) or None if something failed
def load_crypto_exchanges_from_db():
    if not enable_persist_data_db:
        return {}

    db = __create_connection()
    if db is None:
        return None

    try:
        cursor = db.cursor()
        __try_create_exchange_table(cursor)

        cursor.execute("SELECT * FROM exchanges")

        crypto_exchanges = {}
        records = cursor.fetchall()
        for row in records:
            crypto_exchange = CryptoExchange(row[0], row[1], row[2], row[3])
            crypto_exchanges[row[0]] = crypto_exchange

        return crypto_exchanges

    except sqlite3.Error as e:
        log_error(e)
    finally:
        db.close()

    return None


# save crypto exchange to db
# return true if saving was success otherwise false
def save_crypto_exchange_to_db(exchange):
    if not enable_persist_data_db:
        return True

    db = __create_connection()
    if db is None:
        return False
    try:

        cursor = db.cursor()
        __try_create_exchange_table(cursor)

        query = "INSERT OR REPLACE INTO exchanges(id,name,currency,amount) VALUES(?, ?, ?, ?)"
        values = (exchange.exchange_id, exchange.name, exchange.currency, exchange.amount)

        cursor.execute(query, values)
        db.commit()

        return True
    except sqlite3.Error as e:
        log_error(e)
    finally:
        db.close()

    return False


# load crypto currencies from db
# return dictionary(name+exchange_id = currency) or None if something failed
def load_crypto_currencies(exchange_id):
    if not enable_persist_data_db:
        return {}

    db = __create_connection()
    if db is None:
        return None

    try:
        cursor = db.cursor()
        __try_create_crypto_exchanges_table(cursor)

        if exchange_id is None:
            cursor.execute("SELECT * FROM crypto_currencies")
        else:
            cursor.execute("SELECT * FROM crypto_currencies WHERE exchange_id=" + str(exchange_id))

        records = cursor.fetchall()
        crypto_exchanges = {}
        for row in records:
            crypto_exchanges[row[0]] = CryptoCurrency(row[3], row[1], row[2], row[4], row[0])
        return crypto_exchanges

    except sqlite3.Error as e:
        log_error(e)
    finally:
        db.close()

    return None


# insert or update crypto currency to db
# return true if saving was success otherwise false
def save_crypto_currency_to_db(crypto_currency):
    if not enable_persist_data_db:
        return True

    db = __create_connection()
    if db is None:
        return False

    try:
        cursor = db.cursor()
        __try_create_crypto_exchanges_table(cursor)

        cursor = db.cursor()
        query = "INSERT OR REPLACE INTO crypto_currencies " \
                "(id, name, shortcut, exchange_id, amount) VALUES(?, ?, ?, ?, ?)"
        values = (
            crypto_currency.currency_id, crypto_currency.name, crypto_currency.shortcut, crypto_currency.exchange_id,
            crypto_currency.amount)

        cursor.execute(query, values)
        db.commit()

        return True

    except sqlite3.Error as e:
        log_error(e)
    finally:
        db.close()

    return False


# remove crypto currency from db
# return true if saving was success otherwise false
def remove_crypto_currency_to_db(currency_id):
    if not enable_persist_data_db:
        return True

    db = __create_connection()
    if db is None:
        return False

    try:
        cursor = db.cursor()
        query = "DELETE FROM crypto_currencies WHERE id = ?"
        values = (currency_id,)

        cursor.execute(query, values)
        db.commit()
        return True

    except sqlite3.Error as e:
        log_error(e)
    finally:
        db.close()

    return False


# save trade to db
# return true if saving was success otherwise false
def save_trade_to_db(trade):
    if not enable_persist_data_db:
        return True

    db = __create_connection()
    if db is None:
        return False

    try:
        cursor = db.cursor()

        __try_create_trades_table(cursor)

        query = "INSERT INTO trades (amount, amount_out, currency_in, currency_out, exchange_id, timestamp) " \
                "VALUES (?, ?, ?, ?, ? ,?)"
        values = (
            trade.amount, trade.amount_out, trade.currency_in, trade.currency_out, trade.exchange_id, trade.timestamp)

        cursor.execute(query, values)
        db.commit()

        return True

    except sqlite3.Error as e:
        log_error(e)
    finally:
        db.close()

    return False


# load trades from db
# return dictionary(id = trade) or None if something failed
def load_trades_from_db():
    if not enable_persist_data_db:
        return {}

    db = __create_connection()
    if db is None:
        return None

    try:
        cursor = db.cursor()

        __try_create_trades_table(cursor)

        cursor.execute("SELECT * FROM trades")
        records = cursor.fetchall()
        trades = []
        for row in records:
            trades.append(Trade(row[1], row[2], row[3], row[4], row[5], row[6]))

        return trades
    except sqlite3.Error as e:
        log_error(e)
    finally:
        db.close()

    return None


def __create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect("crypto_exchanges_db.db")
        conn.commit()

    except sqlite3.Error as e:
        log_error(e)

    return conn


def __try_create_exchange_table(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS exchanges (id int PRIMARY KEY, name VARCHAR(255),"
                   "currency VARCHAR(3), amount FLOAT(20, 10))")


def __try_create_crypto_exchanges_table(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS crypto_currencies (id INTEGER PRIMARY KEY, name VARCHAR(255),"
                   "shortcut VARCHAR(5), exchange_id int, amount FLOAT(20, 10))")


def __try_create_trades_table(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS trades "
                   "(id INTEGER PRIMARY KEY, amount FLOAT(10, 4), amount_out FLOAT(20, 10), "
                   "currency_in VARCHAR(3), currency_out VARCHAR(3), exchange_id int, timestamp float)")


# only for testing
def remove_all_data():
    db = __create_connection()
    if db is None:
        return None

    try:
        cursor = db.cursor()

        cursor.execute("DROP TABLE exchanges;")
        cursor.execute("DROP TABLE crypto_currencies;")
        cursor.execute("DROP TABLE trades;")

    except sqlite3.Error as e:
        log_error(e)
    finally:
        db.close()

    return None
