import traceback

from config import Config
from parser.db_connections_handler import DbConnectionsHandler
from parser.logger import Logger


class DbListItemsIterator:
    def __init__(self, connection_tag, query):
        self.conn1 = DbConnectionsHandler.get_connection(connection_tag)
        self.cur1 = self.conn1.cursor()
        try:
            self.cur1.execute(query)
            self.conn1.commit()
        except BaseException:
            error_message = traceback.format_exc()
            for line in error_message.split("\n"):
                Logger.print(Config.LOGS_ERROR_PREFIX + line)
            self.conn1.rollback()

    def rowcount(self):
        return self.cur1.rowcount

    def fetchone(self):
        return self.cur1.fetchone()

    def commit(self):
        self.conn1.commit()