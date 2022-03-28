import requests

import execjs

import json

'''
base64解密
'''
# https://www.qimingpian.cn/finosda/project/pinvestment
url = 'https://vipapi.qimingpian.cn/DataList/productListVip'

def get_url():
    headers = {
        'Accept': 'Application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '69',
        'Content-Type': 'Application/x-www-form-urlencoded',
        'Host': 'vipapi.qimingpian.cn',
        'Origin': 'https://www.qimingpian.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }

    data = {
        'time_interval': '',
        'tag': '',
        'tag_type': '',
        'province': '',
        'lunci': '',
        'page': '1',
        'num': '20',
        'unionid': ''
    }

    response = requests.post(url=url, headers=headers, data=data).json()
    # print(response)
    encrypt_data = response['encrypt_data']
    base64(encrypt_data)

def base64(encrypt_data):

    with open('test.js', encoding='utf-8') as f:
        s = f.read()

    result = execjs.compile(s).call('o', encrypt_data)
    js_data = json.loads(result)
    print(js_data)

if __name__ == '__main__':
    get_url()
