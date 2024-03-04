"""               百度贴吧数据抓取实战
需求 : 输入贴吧名称 :
      输入起始页 :
      输入终止页 :
      保存到本地文件 : 赵丽颖吧_第1页.html
                    赵丽颖吧_第二页.html
静态网页抓取思路步骤 :
1. 查看网页源代码,确认所抓取数据在响应内容中是否存在
2. 存在即查找并分析 URL 地址规律
     第 1 页 : http://tieba.baidu.com/f?kw= ???&pn=0
     第 2 页 : http://tieba.baidu.com/f?kw= ???&pn=50
     第 n 页 : pn = (n-1)*50
3. 拼接URL地址 ,发送请求获取响应内容
4. 数据解析处理 ,保存到本地文件
"""

import requests
from urllib import parse
import time
import random

class BaiduSpider :
    def __init__(self):
        """ 定义常用变量 """
        self.url = 'http://tieba.baidu.com/f?kw={}&pn={}'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}


    def get_html(self ,url):
        """ 请求的功能函数 , 获取响应内容html"""
        html = requests.get(url=url , headers=self.headers).content.decode('utf_8')

        return html


    def parse_html(self):
        """ 解析的功能函数 , 解析提取数据 """
        pass

    def save_html(self , filename , html):
        """ 数据处理的功能函数 , 把数据存入数据库 , 本地文件...等 """
        with open(filename ,'w' ,encoding='utf_8') as f :
            f.write(html)

    def run(self):
        """ 程序入口函数 """
        name = input('请输入贴吧名:')
        start = int(input('请输入起始页:'))
        end = int(input('请输入终止页:'))
        # 编码
        params = parse.quote(name)
        for page in range(start , end+1 ):
            pn = (page - 1) * 50
            page_url = self.url.format(params , pn)
            # 调用请求功能函数
            html = self.get_html(url=page_url)
            # 调用保存功能函数
            filename = '{}_第{}页.html'.format(name , page)
            self.save_html(filename, html)
            # 终端提示
            print('第%d页抓取完成'% page)
            # 控制数据抓取频率,每抓取一个页面随机休眠一段时间
            time.sleep(random.randint(1,2))

if __name__ == '__main__' :
    spider = BaiduSpider()
    spider.run()

print('程序结束')

