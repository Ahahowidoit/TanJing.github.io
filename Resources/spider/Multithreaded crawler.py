'''
        多线程抓取豆瓣电影 - 排行榜 - 剧情
1.右键 - 查看网页源代码确认 - 发现为动态
2.F12抓包 , XHR中找到了具体的返回实际数据的JSON地址
3.查看 Query String Parameters 的规律
4.发现只有 start 的值在变 , 0 20 40 60 80 ...
'''

import requests
from threading import Thread,Lock
from queue import Queue
import time
from fake_useragent import UserAgent

class DoubanSpider:
    def __init__(self):
        self.url = 'https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start={}&limit=20'
        # 创建队列
        self.q = Queue()
        # 创建锁
        self.lock = Lock()

    def url_in(self):
        """让URL地址入队列"""
        for start in range(0, 201, 20):
            page_url = self.url.format(start)
            # 把所有的URL地址交给了队列
            self.q.put(page_url)

    def parse_html(self):
        """线程的事件函数 : 请求+解析+数据处理"""
        while True:
            if not self.q.empty():
                url = self.q.get()
                headers = {'User-Agent':UserAgent().random}
                # html:[{},{},{},{},...]
                html = requests.get(url=url,headers=headers).json()
                for one_film_dict in html:
                    item = {}
                    item['name'] = one_film_dict['title']
                    item['rank'] = one_film_dict['rank']
                    item['socre'] = one_film_dict['score']
                    item['time'] = one_film_dict['release_date']
                    print(item)
            else:
                break

    def run(self):
        # URL地址入队列
        self.url_in()
        # 创建多线程
        t_list = []
        for i in range(8):
            t = Thread(target=self.parse_html)
            t_list.append(t)
            t.start()

        for t in t_list:
            t.join()

if __name__ == '__main__':
        start_time = time.time()
        spider = DoubanSpider()
        spider.run()
        end_time = time.time()
        print('执行时间:%.2f' %(end_time - start_time))


