from multiprocessing.queues import Queue

from config import Config


class Logger:
    log_query: Queue = None

    @staticmethod
    def print(*args):
        if Logger.log_query is not None:
            if Config.IS_DEBUG:
                print(*args)
            Logger.log_query.put("".join(args))
        else:
            print(*args)