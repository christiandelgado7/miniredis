import threading


class ThreadSafeDict(dict):
    def __init__(self):
        super(ThreadSafeDict, self).__init__()
        self._lock = threading.Lock()

    def __enter__(self):
        self._lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._lock.release()

    def __del__(self):
        self._lock.release()


class RedisError(object):
    def __init__(self, message, e_type=None):
        self.message = message
        if e_type is not None:
            self.type = e_type
        else:
            self.type = "ERR"

    def __str__(self):
        msg = '(error) '
        if self.type is not None:
            msg = msg + self.type + ' '
        if self.message is not None:
            msg = msg + self.message
        return msg

    def __repr__(self):
        return '<RedisError {}>'.format(str(self))


class RedisMessage(object):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return '<RedisMessage {}>'.format(str(self))


ERROR_WRONG_TYPE = RedisError("Operation against a key holding the wrong kind of value", "WRONGTYPE")
ERROR_ARGUMENT = RedisError("Invalid arguments")
ERROR_INTEGER = RedisError("value is not an integer or out of range")
ERROR_EXPIRE = RedisError("invalid expire time in set")
ERROR_FLOAT = RedisError("value is not a valid float")

OK_VALUE = RedisMessage("OK")
EMPTY_VALUE = RedisMessage("(nil)")
EMPTY_LIST = RedisMessage("(empty list or set)")
