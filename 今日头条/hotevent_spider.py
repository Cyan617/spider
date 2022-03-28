from spider import Spider

class HotEventSpider(Spider):

    def __init__(self):
        self.url = 'https://www.toutiao.com/hot-event/hot-board/'
        self.params = {
            'origin': 'toutiao_pc'
        }

if __name__ == '__main__':
    spider = HotEventSpider()
    spider.main()
