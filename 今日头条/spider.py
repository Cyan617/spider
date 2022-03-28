from urllib.parse import urlencode

import requests

class Spider:
    sign_url = 'http://localhost:9999/get_signs'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    }
    def __init__(self):
        """
        url: 需要爬取的数据接口url
        params: 除去_signature的接口参数
        """
        self.url = 'https://www.toutiao.com/api/pc/list/feed' # 首页推荐页
        self.params = {
            'channel_id': '0',
            'max_behot_time': '1648458994',
            'category': 'pc_profile_recommend',
            'aid': '24',
            'app_name': 'toutiao_web',
        }

    def get_sign(self, url):
        url += '?{}'
        sign_resp = requests.post(self.sign_url, {'urls': url.format(urlencode(self.params))})
        sign = sign_resp.text
        self.params['_signature'] = sign

    def get_data(self):
        self.get_sign(self.url)
        resp = requests.get(self.url, params=self.params, headers=self.headers)
        return resp.json()

    def main(self):
        data = self.get_data()
        print(data)

if __name__ == '__main__':
    spider = Spider()
    spider.main()
