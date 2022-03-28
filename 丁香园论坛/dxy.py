import random

r = random.sample([str(i) for i in range(0, 10)], 8)
r = "".join(r)
# print(r)

# -*- coding: utf-8 -*-

import requests
import time
import random
from hashlib import sha1

class Crawls:
    def __init__(self):
        self.url = 'https://www.dxy.cn/bbs/newweb/homepage/recommend'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
            'referer': 'https://www.dxy.cn/bbs/newweb/pc/home',
        }
        self.noncestr = ''.join(random.sample([str(i) for i in range(0, 10)], 8))
        self.timestamp = int(time.time() * 1000)
        # print(self.timestamp)
        self.json_data = {
            'pageSize': '20',
            'refresh': 'true',
            'serverTimestamp': self.timestamp - random.randint(10, 1000),
            'timestamp': self.timestamp,
            'noncestr': self.noncestr
        }
        self.get_sign()

    def get_sign(self):
        sign_s = f"appSignKey=4bTogwpz7RzNO2VTFtW7zcfRkAE97ox6ZSgcQi7FgYdqrHqKB7aGqEZ4o7yssa2aEXoV3bQwh12FFgVNlpyYk2Yjm9d2EZGeGu3&noncestr={self.json_data['noncestr']}&pageSize={self.json_data['pageSize']}&refresh={self.json_data['refresh']}&serverTimestamp={self.json_data['serverTimestamp']}&timestamp={self.json_data['timestamp']}"
        s1 = sha1()
        s1.update(sign_s.encode("utf-8"))
        sing_s = s1.hexdigest()
        # print(sing_s)
        self.json_data['sign'] = sing_s
        # print(self.json_data)

    def crawl(self):
        resp = requests.get(self.url, headers=self.headers, params=self.json_data)
        # reps.content.decode("utf-8")
        # print(resp)
        if resp.content:
            print(resp.json()['data']['result'])
            resp_json = resp.json()['data']['result']
            for i in resp_json:
                print(i['title'], i['entityId'])
        else:
            print(resp.text)

crawls = Crawls()
crawls.crawl()
