from multiprocessing.queues import Queue

from config import Config


class Logger:
    log_queue: Queue = None

    @staticmethod
    def print(*args):
        if Logger.log_queue is not None:
            if Config.IS_DEBUG:
                print(*args)
            Logger.log_queue.put(" ".join(args))
        else:
            print(*args)