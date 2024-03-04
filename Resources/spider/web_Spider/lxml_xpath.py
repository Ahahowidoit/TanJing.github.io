"""
    使用流程:
        导入模块: from lxml import etree
        创建解析对象: parse_html = etree.HTML(html)
            html: 向网站发请求拿到的响应内容(resq.text)
        开始提取数据: r_list = parse_html.xpath('xpath表达式')
            调用 xpath ,结果一定是个列表
"""

"""
    抓取豆瓣图书TOP250榜单数据抓取(一级页面)
    https://book.douban.com/top250?start=0
"""
import requests
from lxml import etree
import time
import random
from fake_useragent import UserAgent

class DoubanBookspider :
    def __init__(self):
        self.url = 'https://book.douban.com/top250?start={}'

    def get_html(self ,url):
        """ 请求函数 - 获取 html """
        headers = { 'User-Agent' : UserAgent().random }
        html = requests.get(url=url , headers=headers).content.decode('utf-8' , 'ignore')
        # decode:网页编码方式,可通过网页源码中搜索 charset 查询 , ignore :防止网站解析后嵌入无法识别的字符
        #  直接调用解析函数
        self.parse_html(html)

    def parse_html(self , html):
        """ 解析函数 - 解析提取数据 """
        parse = etree.HTML(html)
        table_list = parse.xpath('//table')
        for table in table_list :
            item = {}
            ## 书的名称,判断
            name_list = table.xpath('.//div[@class="pl2"]/a/text()')
            item['name'] = name_list[0].strip() if name_list else None
            # 书的信息
            comment_list = table.xpath('.//p[@class="pl"]/text()')
            item['comment'] = comment_list[0].strip() if comment_list else None
            ## 书的评分
            score_list = table.xpath('.//span[@class="rating_nums"]/text()')
            item['score'] = score_list[0].strip() if score_list else None
            ## 书的评价人数
            number_list = table.xpath('.//span[@class="pl"]/text()')
            item['number'] = number_list[0][1:-1].strip() if number_list else None
            ## 书的说明
            instructions_list = table.xpath('.//span[@class="inq"]/text()')
            item['instructions'] = instructions_list[0].strip() if instructions_list else None
            print(item)


    def run(self):
        for page in range(1 ,11):
            start = (page - 1) * 25
            page_url = self.url.format(start)
            self.get_html(url = page_url)
            # 控制数据抓取频率
            time.sleep(random.uniform(0,2))


if __name__ == '__main__' :
    spider = DoubanBookspider()
    spider.run()

print('数据抓取完成')