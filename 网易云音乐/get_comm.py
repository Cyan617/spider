# coding='utf-8'

import json
import time
from threading import Thread, Lock

import pymysql
import requests
from main.spider import SpiderMan

class commSpider(SpiderMan):

    insert_sql = "insert into songcomment(songId, commentId, content, likedCount, userId, userName, commentTime) values(%s,%s,%s,%s,%s,%s,%s)"  # 要插入的数据

    def __init__(self):
        super(commSpider, self).__init__(redisName="music_seed", filterName="music")
        self.lock = Lock()
        self.cursor_select = self.conn.cursor(cursor=pymysql.cursors.SSDictCursor)

    # 获取请求数据
    def get_comments_json(self, url, data):
        try:
            r = requests.post(url, data=data)
            r.encoding = "utf-8"
            if r.status_code == 200:
                # 返回json格式的数据
                return r.json()
        except Exception as e:
            print(f"爬取失败!{e}")

    def postParam(self, detailId):
        d = {
            "csrf_token": "",
            "cursor": "-1",
            "offset": 0,
            "orderType": "1",
            "pageNo": "1",
            "pageSize": "20",
            "rid": f"R_SO_4_{detailId}",
            "threadId": f"R_SO_4_{detailId}"
        }
        d = json.dumps(d)
        return d

    def parse_detail(self, detailId):
        params, encSecKey = self.get_params(detailId)
        url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
        data = {'params': params, 'encSecKey': encSecKey}
        # 获取第一页评论
        json_data = self.detailRequest(url, data)
        # 热评总数
        hotcmts = json_data["data"]["hotComments"]
        detailList = []
        if hotcmts:
            print(detailId)
            time.sleep(0.1)
            for item in range(len(hotcmts)):
                content = hotcmts[item]["content"]
                commentId = hotcmts[item]["commentId"]
                t = hotcmts[item]["time"]
                timeStr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t / 1000))
                likedCount = hotcmts[item]["likedCount"]
                userId = hotcmts[item]["user"]["userId"]
                userName = hotcmts[item]["user"]["nickname"]
                res = (detailId, commentId, content, likedCount, userId, userName, timeStr)
                detailList.append(res)
        return detailList

if __name__ == "__main__":
    spider = commSpider()
    spider.main(4)


