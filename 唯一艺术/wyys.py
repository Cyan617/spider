import re
from urllib import parse

import requests

session = requests.Session()

json_param = {
    "pageCount": "1",
    "pageSize": "20",
    "sort": None,
}

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'referer': 'https://theone.art/',
    'origin': 'https://theone.art',
    "Accept": "application/json, text/plain, */*"
}

def get_datakey():
    url = 'https://api.theone.art/market/api/key/get'
    resp = session.get(url, headers=headers)
    # print(resp.json())
    # exit()
    data = resp.json()['data']
    # print(data)
    return data

def post_datakey():
    url = 'http://localhost:9999/decrypt'
    data = {
        'data': get_datakey()
    }
    resp = requests.post(url, data)
    dataresult = resp.text
    dataResultFun = dataresult.split(",")[0][4:]
    dataResultId = dataresult.split(",")[1].split("=")[1]
    p1 = re.compile(r"x\*a (.*?) y\*b", re.S)
    p2 = re.compile(r".*?=(\d+)", re.S)
    num = p2.findall(dataResultFun)
    mark = p1.findall(dataResultFun)[0]
    res = eval(f'int(num[0]) * int(num[2]) {mark} int(num[1]) * int(num[3])')
    # print(num, mark, res)
    return {
        'id': dataResultId,
        'num': res
    }


def post_data():
    url = 'http://localhost:9999/encrypt'
    data = post_datakey()
    resp = requests.post(url, data)
    return resp.text

def main():
    url = 'https://api.theone.art/market/api/saleRecord/list'
    sig = post_data()
    print(sig)
    json_param['sig'] = sig
    headers['sig'] = parse.quote(sig)
    headers['accept'] = 'application/json, text/plain, */*'
    resp = session.post(url=url, headers=headers, json=json_param)
    # print(resp)
    print(resp.json())

if __name__ == '__main__':
    main()
