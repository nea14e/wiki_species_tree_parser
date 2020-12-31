from multiprocessing.queues import Queue


class Logger:
    log_query: Queue = None

    @staticmethod
    def print(*args):
        if Logger.log_query is not None:
            Logger.log_query.put("".join(args))
        else:
            print(*args)