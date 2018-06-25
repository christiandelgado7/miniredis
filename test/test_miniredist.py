import logging
import unittest
from time import sleep

from miniredis.miniredis import MiniRedis
from miniredis.structures import *

log_format = "%(asctime)s %(funcName)20s %(levelname)-8s %(message)s"
logging.basicConfig(level=logging.DEBUG, format=log_format)
log = logging.getLogger(__name__)


def multithread_worker(miniredis, key, th):
    log.debug('thread {})  {}'.format(th, miniredis.incr(key)))
    return


class TestMiniRedis(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.miniredis = MiniRedis()

    def test_get_empty(self):
        key = 'empty'
        resp = self.miniredis.get(key)
        self.assertEquals(resp, EMPTY_VALUE)

    def test_set(self):
        key = 'key'
        value = 10
        resp = self.miniredis.set(key, value)
        self.assertEquals(resp, OK_VALUE)
        resp = self.miniredis.get(key)
        self.assertEquals(resp, value)

    def test_set_seconds(self):
        key = 'key_sec'
        value = 5
        resp = self.miniredis.set(key, value, 3)
        self.assertEquals(resp, OK_VALUE)
        resp = self.miniredis.get(key)
        self.assertEquals(resp, value)
        sleep(4)
        resp = self.miniredis.get(key)
        self.assertEquals(resp, EMPTY_VALUE)

    def test_incr_multithreading(self):
        key = 'threads'
        threads = []
        for i in range(10):
            t = threading.Thread(name='thread_' + str(i + 1), target=multithread_worker,
                                 args=(self.miniredis, key, i + 1))
            threads.append(t)
        for i in range(10):
            threads[i].start()
            if (i % 3) == 0:
                log.debug('main thread) i:{}  {}'.format(i, self.miniredis.incr(key)))
        for i in range(10):
            threads[i].join()
        log.debug('main thread) final  {}'.format(self.miniredis.incr(key)))
        self.assertEquals(int(self.miniredis.get(key)), 15)

    def test_del(self):
        key = 'del'
        value = 5
        resp = self.miniredis.set(key, value)
        self.assertEquals(resp, OK_VALUE)
        resp = self.miniredis.get(key)
        self.assertEquals(resp, value)
        resp = self.miniredis.delete(key)
        self.assertEquals(resp, 1)
        resp = self.miniredis.get(key)
        self.assertEquals(resp, EMPTY_VALUE)

    def test_z_functions(self):
        key = 'zkey'
        resp = self.miniredis.zadd(key, '10', 'a')
        self.assertEquals(resp, 1)
        resp = self.miniredis.zadd(key, '30', 'c')
        self.assertEquals(resp, 1)
        resp = self.miniredis.zadd(key, '20', 'b')
        self.assertEquals(resp, 1)
        resp = self.miniredis.zcard(key)
        self.assertEquals(resp, 3)
        resp = self.miniredis.zrange(key, 0, -1)
        self.assertEquals(resp, ['a', 'b', 'c'])
        resp = self.miniredis.zrank(key, 'a')
        self.assertEquals(resp, 0)
        resp = self.miniredis.zadd(key, '50', 'a')
        self.assertEquals(resp, 0)
        resp = self.miniredis.zrank(key, 'a')
        self.assertEquals(resp, 2)
        resp = self.miniredis.zrange(key, 0, -1)
        self.assertEquals(resp, ['b', 'c', 'a'])
        resp = self.miniredis.zrank(key, 'x')
        self.assertEquals(resp, EMPTY_VALUE)
        resp = self.miniredis.zrange('x', 0, -1)
        self.assertEquals(resp, EMPTY_LIST)

    def test_handle_errors(self):
        key = 'err'
        resp = self.miniredis.get(None)
        self.assertEquals(resp, ERROR_ARGUMENT)
        resp = self.miniredis.set(key, 1, 3.3)
        self.assertEquals(resp, ERROR_INTEGER)
        resp = self.miniredis.set(key, 1, 0)
        self.assertEquals(resp, ERROR_EXPIRE)
        resp = self.miniredis.set(key, 1)
        self.assertEquals(resp, OK_VALUE)
        resp = self.miniredis.zadd(key, '10', 'a')
        self.assertEquals(resp, ERROR_WRONG_TYPE)
        resp = self.miniredis.delete(key)
        self.assertEquals(resp, 1)
        resp = self.miniredis.zadd(key, 'x', 'a')
        self.assertEquals(resp, ERROR_FLOAT)


if __name__ == "__main__":
    unittest.main()
