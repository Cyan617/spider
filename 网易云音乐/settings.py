import datetime
import loguru

from DBUtils.PooledDB import PooledDB
import pymysql

logger = loguru.logger
PROJECT_NAME = 'spider'
day = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
logger.add(
    sink=f'./logs/{PROJECT_NAME}/{day}.log',
    level='INFO',
    retention='7 days',
    enqueue=True,
    encoding='utf-8'
)

mysql_pool = PooledDB(
            creator=pymysql,
            maxconnections=50,
            mincached=0,
            maxcached=20,
            maxshared=0,
            blocking=True,
            setsession=[],
            ping=0,
            host='127.0.0.1',
            port=3306,
            user='root',
            password='123456',
            database='music163',
            charset='utf8mb4')
conn = mysql_pool.connection()
