# r_list = re.findall('AB','ABCABCABCDEFG') # 将符合'AB'的值提出作为列表的元素
# print(f'r_list为列表',r_list)


"""             猫眼电影数据抓取 
需求分析 : 抓取猫眼电影 TOP100 榜单中的电影名称/主演/上映时间
https://www.maoyan.com/board/4?&offset=0
第 n 页 : offset = (n-1)*10
"""

""" 
网页源码 : 
<div class="movie-item-info">
        <p class="name"><a href="/films/1200486" title="我不是药神" data-act="boarditem-click" data-val="{movieId:1200486}">我不是药神</a></p>
        <p class="star">
                主演：徐峥,周一围,王传君
        </p>
<p class="releasetime">上映时间：2018-07-05</p>    </div>
"""

""" 
正则表达式 : 
<div class="movie-item-info">.*?title="(.*?)".*?<p class="star">(.*?)</p>.*?<p class="releasetime">(.*?)</p>
"""


import re
import requests
import time
import  random

class MaoyanSpider :
    def __init__(self):
        self.url = 'https://www.maoyan.com/board/4?offset={}'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.37'}

    def get_html(self , url):
        """ 获取响应内容 """
        html = requests.get(url=url , headers=self.headers).content.decode('utf_8')
        # 直接调用解析函数
        self.parse_html(html)

    def parse_html(self,html):
        """ 解析提取数据函数 """
        regex = '<div class="movie-item-info">.*?title="(.*?)".*?<p class="star">(.*?)</p>.*?<p class="releasetime">(.*?)</p>'
        pattern = re.compile(regex , re.S)
        r_list = pattern.findall(html)

        # 直接调用数据处理函数
        self.save_html(r_list)

    def save_html(self ,r_list):
        """ 具体数据处理的函数 """
        item = { }
        for r in r_list :
            item['name'] = r[0].strip()
            item['actor'] = r[1].strip()
            item['time'] = r[2].strip()
            print(item)

    def run(self):
        """ 程序入口函数 """
        for offset in range(0,91,10) :
            page_url = self.url.format(offset)
            self.get_html(url=page_url)
            # 控制数据抓取频率 uniform 生成指定范围内的浮点数
            time.sleep(random.uniform(1,3))

if __name__ == '__main__' :
    spider = MaoyanSpider()
    spider.run()

