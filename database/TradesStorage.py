import datetime
import json
import re

from database import SqlLiteDbHelper
from database.SqlLiteDbHelper import save_trade_to_db, load_trades_from_db


# Trades storage persist all trades to storage(db)
# Storage uses own cache
from utils.Logger import log_error


class TradesStorage:
    trades_storage = []
    __data_loaded_from_db = False

    # save trade to storage
    def save(self, trade):

        save_trade_to_db(trade)
        self.trades_storage.append(trade)

    # Get trades depend on conditions
    # return list of trades or empty list
    def get_trades(self, exchange_id=0, offset=0, limit=-1, search='', date_from=None, date_to=None):

        # if data is not loaded from db, will be loaded
        if SqlLiteDbHelper.enable_persist_data_db and not self.__data_loaded_from_db:
            self.trades_storage = load_trades_from_db()
            self.__data_loaded_from_db = True

        trades = []
        try:
            # convert time to timestamp
            date_from_timestamp = self.__convert_date_to_timestamp(date_from)
            date_to_timestamp = self.__convert_date_to_timestamp(date_to)

            for trade in self.trades_storage:
                if self.__validate_trade_depend_on_conditions(trade, exchange_id,
                                                              date_from_timestamp, date_to_timestamp, search):
                    trades.append(trade)

            if isinstance(offset, int) and offset > 0:
                if offset > len(trades):
                    trades = []
                else:
                    trades = trades[offset:len(trades) - 1]

            if isinstance(limit, int) and limit > 0:
                if limit < len(trades):
                    trades = trades[0:limit]

        except Exception as e:
            log_error(e)

        return trades

    @staticmethod
    def __validate_trade_depend_on_conditions(trade, exchange_id, date_from_timestamp, date_to_timestamp, search):
        # validate exchange_id
        if exchange_id is None or trade.exchange_id == exchange_id:
            # validate from date timestamp
            if date_from_timestamp is not None and date_from_timestamp > trade.timestamp:
                return False

            # validate to date timestamp
            if date_to_timestamp is not None and date_to_timestamp < trade.timestamp:
                return False

            # validate search string - using regexp
            if search:
                result = json.dumps(trade.to_dictionary())
                regexp = re.compile(search)
                if regexp.search(result):
                    return True

            else:
                return True

        return False

    @staticmethod
    def __convert_date_to_timestamp(date):
        if date is None:
            return None

        return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ').timestamp()
