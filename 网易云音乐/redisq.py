import datetime
import json

import loguru
import redis

class RdsQueue:
    def __init__(self, name='redis_log'):
        REDIS_CONFIG = {
            'host': 'localhost',
            'port': '6379',
            'db': '1',
            'decode_responses': True,
        }
        redis_pool = redis.ConnectionPool(**REDIS_CONFIG)
        self.rds = redis.Redis(connection_pool=redis_pool)
        self.logger = loguru.logger

        self.TASK_NAME = name
        day = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        self.logger.add(
            sink=f'./logs/{self.TASK_NAME}/{day}.log',
            level='INFO',
            retention='7 days',
            enqueue=True,
            encoding='utf-8'
        )
    def connect(self):
        pass

    def close(self):
        pass

    def pop(self):
        task = self.rds.rpop(self.TASK_NAME)
        return task

    def add(self, data):
        """
        :param config:  type is dict
        :return:
        """

        self.rds.lpush(self.TASK_NAME, data)
        self.logger.info(f'{data} add to {self.TASK_NAME}')
        return

    def queueLen(self):
        queue_len = self.rds.llen(self.TASK_NAME)
        if queue_len:
            return queue_len
        return 0
