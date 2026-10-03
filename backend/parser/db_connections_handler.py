import psycopg2

from config import Config


class DbConnectionsHandler:
    connections_pool = {}

    @classmethod
    def get_connection(cls, tag: str = "default_conn"):
        """
                Выдаёт соединение, соответствующее тегу.
                Запоминает его для переиспользования - для одного и того же тега всегда выдаётся одно и то же соединение.
                При необходимости создаёт новый элемент (для нового тега).
                :param tag: str: некий тег для различения соединений
                :return: соединение, соответствующее тегу.
                """
        if tag in cls.connections_pool.keys():
            return cls.connections_pool[tag]
        else:
            db_name = Config.TEST_DB_NAME if Config.BACKEND_IS_USE_TEST_DB else Config.PROD_DB_NAME
            new_conn = psycopg2.connect(
                "host='" + Config.DB_HOST +
                "' port=" + Config.DB_PORT +
                " dbname='" + db_name +
                "' user='" + Config.DB_USER +
                "' password='" + Config.DB_PASSWORD + "'"
            )
            cls.connections_pool[tag] = new_conn
            return new_conn