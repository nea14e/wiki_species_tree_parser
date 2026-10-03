import os
import traceback

from config import Config
from parser.db_connections_handler import DbConnectionsHandler
from parser.logger import Logger


class DbExecuteNonQuery:
    @staticmethod
    def execute(connection_tag, query):
        conn1 = DbConnectionsHandler.get_connection(connection_tag)
        cur1 = conn1.cursor()
        try:
            cur1.execute(query)
            conn1.commit()
        except BaseException:
            error_message = traceback.format_exc()
            for line in error_message.split("\n"):
                Logger.print(Config.LOGS_ERROR_PREFIX + line)
            conn1.rollback()

    @staticmethod
    def execute_file(connection_tag, path):
        Logger.print("execute_file(): ", path)
        # path is relative to this script file's directory, not to the root script
        this_script_file = os.path.realpath(__file__)
        this_script_dir = os.path.dirname(this_script_file)
        path = os.path.join(this_script_dir, path)
        with open(path, "r", encoding="utf-8") as f:
            query = f.read()
        DbExecuteNonQuery.execute(connection_tag, query)