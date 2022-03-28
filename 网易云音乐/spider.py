import json
import math
import random
from threading import Lock, Thread

import requests
from Crypto.Cipher import AES
import codecs
import base64


from bloomFilter import BloomFilter
from main.redisq import RdsQueue
from settings import conn, logger

class SpiderMan:

    insert_sql = "insert into artist(artistId, artistName) values(%s,%s)"

    def __init__(self, redisName, filterName):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
        }
        self.start_queue = RdsQueue(redisName)
        self.filter = BloomFilter(filterName)
        self.lock_commit = Lock()
        self.logger = logger
        self.conn = conn
        self.cursor = self.conn.cursor()

    # 发送请求
    def detailRequest(self, url, data, encode="utf-8"):
        """
        :param url:
        :param data:
        :param encode:
        :return: Request
        """
        try:
            resp = requests.post(url, data=data)
            resp.encoding = encode
            if resp.status_code == 200:
                return resp
        except Exception as e:
            print(f"爬取失败!{e}")

    # 生成16个随机字符
    def generate_random_strs(self, length):
        string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        # 控制次数参数i
        i = 0
        # 初始化随机字符串
        random_strs = ""
        while i < length:
            e = random.random() * len(string)
            # 向下取整
            e = math.floor(e)
            random_strs = random_strs + list(string)[e]
            i = i + 1
        return bytes(random_strs, encoding="utf8")

    # AES加密
    def AESencrypt(self, msg, key):
        # 如果不是16的倍数则进行填充(paddiing)
        padding = 16 - len(msg) % 16
        # 这里使用padding对应的单字符进行填充
        msg = msg + padding * chr(padding)
        # 用来加密或者解密的初始向量(必须是16位)
        iv = '0102030405060708'
        aes = AES.new(key.encode("utf-8"), IV=iv.encode("utf-8"), mode=AES.MODE_CBC)
        # 加密后得到的是bytes类型的数据
        encryptedbytes = aes.encrypt(msg.encode("utf-8"))
        # 使用Base64进行编码,返回byte字符串
        encodestrs = base64.b64encode(encryptedbytes)
        # 对byte字符串按utf-8进行解码
        enctext = encodestrs.decode('utf-8')
        return enctext

    # RSA加密
    def RSAencrypt(self, randomstrs, key, f):
        # 随机字符串逆序排列
        string = randomstrs[::-1]
        # 将随机字符串转换成byte类型数据
        # text = bytes(string, encoding='utf8')
        seckey = int(codecs.encode(string, encoding='hex'), 16) ** int(key, 16) % int(f, 16)
        return format(seckey, 'x').zfill(256)

    # 定义Post参数
    def postParam(self, detailId):
        """

        :param detailId:
        :return: dict(param)
        """
        return dict

    # 获取加密参数
    def get_params(self, detailId):
        d = self.postParam(detailId)
        # 固定值
        g = '0CoJUm6Qyw8W8jud'
        f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        e = '010001'

        # 随机生成长度为16的随机字符串,可固定
        # i = self.generate_random_strs(16)
        i = 'kEhRsbVFNaFQEOaG'
        # 随机值通过RSA加密之后得到encSecKey的值,可固定
        # encSecKey = RSAencrypt(i, e, f)
        encSecKey = 'a200e63459c28899f38dd1866058664c3fc10567b9d72ef91378dedf3971075e45732976768705520ee58a55d0e2a3b72ff8fe351e16651af42d001e77cf1c823006a8974cb88c986d1525cfe71935db2ec7a1b3677dfc670dbcdc4e58820fc31ade511a79a8e910a28d542fd44b7f67958468bd41d73d2ade5268565ac9f5de'

        # 两次AES加密之后得到params的值
        enctext = self.AESencrypt(d, g)
        encText = self.AESencrypt(enctext, i)
        return encText, encSecKey

    #数据插入
    def insert_data(self, sql, detailList):
        try:
            #数据库操作锁
            self.lock_commit.acquire()
            self.cursor.executemany(sql, detailList)
            self.conn.commit()
            self.lock_commit.release()
            self.logger.info(f'insert {detailList[-1]} success')
        except Exception as e:
            self.logger.debug(e)

    # 页面解析
    def parse_detail(self, detailId):
        """
        :param detailId:
        :return: list
        """
        return

    #通用采集流程
    def getdetailInfo(self):
        p = 0
        detailList = []
        while True:
            if self.start_queue.queueLen():
                detailId = self.start_queue.pop()
                if self.filter.isContains(detailId):
                    self.logger.debug(f"{detailId} has been crawled")
                    continue
                self.filter.insert(detailId)
                try:
                    detailList.append(self.parse_detail(detailId))
                    p += 1
                    if p == 10 or self.start_queue.queueLen() == 0:
                        if detailList != []:
                            self.insert_data(self.insert_sql, detailList)
                            detailList = []
                        else:
                            self.logger.debug('no data to sql')
                        p = 0
                except Exception as e:
                    self.logger.debug(f"{detailId} {e}")
            elif detailList != []:
                self.insert_data(self.insert_sql, detailList)
                detailList = []
                break

    # 采集流程1
    def getdetailsInfo(self):
        p = 0
        detailList = []
        while True:
            try:
                if self.start_queue.queueLen():
                    detailId = self.start_queue.pop()
                    if self.filter.isContains(detailId):
                        self.logger.debug(f"{detailId} has been crawled")
                        continue
                    self.filter.insert(detailId)

                    detailList = self.parse_detail(detailId)
                    p += 1
                    if p == 10 or self.start_queue.queueLen() == 0:
                        if detailList != []:
                            self.insert_data(self.insert_sql, detailList)
                            detailList = []
                        else:
                            self.logger.debug('no data to sql')
                        p = 0

                elif detailList != []:
                    self.insert_data(self.insert_sql, detailList)
                    detailList = []
                    break
            except Exception as e:
                self.logger.debug(e)

    #多线程
    def multi_task(self, function, num):
        tasks = []
        for _ in range(num):
            thread = Thread(target=function)
            thread.start()
            tasks.append(thread)
        for th in tasks:
            th.join()

    def main(self, num):
        self.multi_task(self.getdetailInfo, num)
