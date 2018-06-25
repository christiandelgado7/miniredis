import logging

from structures import *

log = logging.getLogger(__name__)


def redis_set_to_list(dic):
    return [str(x) for _, x in sorted(zip(dic.values(), dic.keys()))]


class MiniRedis(object):

    def __init__(self):
        self.db = ThreadSafeDict()
        self.tasks = ThreadSafeDict()

    def delete_timer(self, key):
        print("deleting key {}".format(key))
        self.delete(key)

    def set(self, key, value, seconds=None):
        if key is None or value is None:
            return ERROR_ARGUMENT
        if seconds is not None:
            try:
                seconds = int(str(seconds))
            except (KeyError, TypeError, ValueError):
                return ERROR_INTEGER
            if seconds < 1:
                return ERROR_EXPIRE
        with self.db as db:
            with self.tasks as tasks:
                if key in tasks:
                    tasks[key].cancel()
                    del tasks[key]
                db[key] = value
                if seconds is not None:
                    new_task = threading.Timer(seconds, self.delete, args=[key])
                    new_task.start()
                    tasks[key] = new_task
        return OK_VALUE

    def get(self, key):
        if key is None:
            return ERROR_ARGUMENT
        with self.db as db:
            value = db.get(key)
            if isinstance(value, dict):
                return ERROR_WRONG_TYPE
            if value is not None:
                return value
            else:
                return EMPTY_VALUE

    def delete(self, key):
        if key is None:
            return ERROR_ARGUMENT
        with self.db as db:
            if key not in db:
                return 0
            with self.tasks as task:
                if key in task:
                    task[key].cancel()
                    del task[key]
                del db[key]
        return 1

    def db_size(self):
        with self.db as db:
            return len(db)

    def incr(self, key):
        if key is None:
            return ERROR_ARGUMENT
        with self.db as db:
            val = db.get(key)
            if val is None:
                val = 0
            try:
                val = int(str(val)) + 1
                db[key] = str(val)
                return val
            except (KeyError, TypeError, ValueError):
                return ERROR_INTEGER

    def zadd(self, key, score, member):
        try:
            score = float(str(score))
        except (KeyError, TypeError, ValueError):
            return ERROR_FLOAT
        if key is None or score is None or member is None:
            return ERROR_ARGUMENT
        with self.db as db:
            z = db.get(key)
            if z is None:
                z = {}
            elif not isinstance(z, dict):
                return ERROR_WRONG_TYPE
            if member in z:
                val = 0
            else:
                val = 1
            z[member] = score
            db[key] = z
            return val

    def zcard(self, key):
        if key is None:
            return ERROR_ARGUMENT
        with self.db as db:
            z = db.get(key)
            if z is None:
                return 0
            elif not isinstance(z, dict):
                return ERROR_WRONG_TYPE
            return len(z)

    def zrank(self, key, member):
        if key is None or member is None:
            return ERROR_ARGUMENT
        with self.db as db:
            z = db.get(key)
            if z is None:
                return EMPTY_VALUE
            elif not isinstance(z, dict):
                return ERROR_WRONG_TYPE
            if member in z:
                return redis_set_to_list(z).index(member)
            else:
                return EMPTY_VALUE

    def zrange(self, key, start, stop):
        try:
            start = int(str(start))
            stop = int(str(stop))
        except (KeyError, TypeError, ValueError):
            return ERROR_INTEGER
        if key is None:
            return ERROR_ARGUMENT
        with self.db as db:
            z = db.get(key)
            if z is None:
                return EMPTY_LIST
            elif not isinstance(z, dict):
                return ERROR_WRONG_TYPE
            zlist = redis_set_to_list(z)
            size = len(zlist)
            if start < 0:
                start = size + start
            if stop < 0:
                stop = size + stop
            result = zlist[start:stop + 1]
            if not result:
                return EMPTY_LIST
            else:
                return result
