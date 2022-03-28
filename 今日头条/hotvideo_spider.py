from spider import Spider

class HotVideoSpider(Spider):

    def __init__(self):
        self.url = 'https://www.toutiao.com/api/pc/list/feed'
        self.params = {
            "offset": "0",
            "channel_id": "94349549395",
            "max_behot_time": "0",
            "category": "pc_profile_channel",
            "disable_raw_data": "true",
            "aid": "24",
            "app_name": "toutiao_web"
        }

if __name__ == '__main__':
    spider = HotVideoSpider()
    spider.main()
