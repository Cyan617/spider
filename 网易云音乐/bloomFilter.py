# coding:utf-8
from hashlib import md5
import redis

class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


class BloomFilter(object):
    def __init__(self, PROJECT_NAME):
        """
        :param blockNum: one blockNum for about 90,000,000; if you have more strings for filtering, increase it.
        """
        REDIS_CONFIG = {
            'host': '127.0.0.1',
            'port': '6379',
            'db': '1',
            'decode_responses': True,
            'password': '123456'
        }
        redis_pool = redis.ConnectionPool(
            host=REDIS_CONFIG['host'],
            port=int(REDIS_CONFIG['port']), db=int(REDIS_CONFIG['db']))
        self.server = redis.Redis(connection_pool=redis_pool)
        self.bit_size = 1 << 32  # Redis的String类型最大容量为512M，现使用256M
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.key = f'{PROJECT_NAME}_bloomfilter'
        self.blockNum = 1
        self.hashfunc = []
        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))

    def isContains(self, str_input):
        """
        :param str_input: url判断采集的url是否存在
        :return: true or false
        """
        if not str_input:
            return False
        str_input = str_input.encode('utf-8')
        m5 = md5()
        m5.update(str_input)
        str_input = m5.hexdigest()
        ret = True
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            ret = ret & self.server.getbit(name, loc)
        return ret

    def insert(self, str_input):
        """
        对于未采集的url采集成功后插入到布隆过滤器里面
        :param str_input:
        :return:
        """
        str_input = str_input.encode('utf-8')
        m5 = md5()
        m5.update(str_input)
        str_input = m5.hexdigest()
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            self.server.setbit(name, loc, 1)
