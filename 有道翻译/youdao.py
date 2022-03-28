import time
from hashlib import md5
import requests

"""
i: dog
from: AUTO
to: AUTO
smartresult: dict
client: fanyideskweb
salt: 16414618296845
sign: 0e1ba04d8adb727938e40784647f0282
lts: 1641461829684
bv: e70edeacd2efbca394a58b9e43a6ed2a
doctype: json
version: 2.1
keyfrom: fanyi.web
action: FY_BY_REALTlME
"""
headers={
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,de;q=0.8',
    'Connection': 'keep-alive',
    'Content-Length': '240',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'OUTFOX_SEARCH_USER_ID=834912817@10.169.0.83; OUTFOX_SEARCH_USER_ID_NCOO=1727090705.8985744; UM_distinctid=17e03d97c4f42b-06f7ee7b1fe264-978153c-1fa400-17e03d97c50d40; _ntes_nnid=dc00bf3def0b8a9b072fcbee1f5c93a7,1640742139559; JSESSIONID=aaaJjcJ-4TL8qdbnzTU4x; ___rl__test__cookies=1641461829683',
    'Host': 'fanyi.youdao.com',
    'Origin': 'https://fanyi.youdao.com',
    'Referer': 'https://fanyi.youdao.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

md = md5()

word = input("翻译单词: ")
lts = str(int(time.time()*1000))
salt = lts+"1"

sign = f"fanyideskweb{word}{salt}Y2FYu%TNSbMCxc3t2u^XT"
bv = "e70edeacd2efbca394a58b9e43a6ed2a"

md.update(sign.encode())
sign = md.hexdigest()

data={
    'i': word,
    'from': 'AUTO',
    'to': 'AUTO',
    'smartresult': 'dict',
    'client': 'fanyideskweb',
    'salt': salt,
    'sign': sign,
    'lts': lts,
    'bv': 'e70edeacd2efbca394a58b9e43a6ed2a',
    'doctype': 'json',
    'version': '2.1',
    'keyfrom': 'fanyi.web',
    'action': 'FY_BY_REALTlME',
}

res = requests.post(url="https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule", headers=headers, data=data)
print(res.json()['translateResult'][0][0]['tgt'])
