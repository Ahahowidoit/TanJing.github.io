"""
            代理参数 proxies
 获取代理IP的网站: 西刺代理 /快代理 / 全网代理 / 代理精灵
 参数类型 :
    字典 : proxies = { '协议' : '协议://IP:端口号' }
示例 :
    proxies = {
        'http' : 'http://192.168.1.11:8888',
        'https' : 'https://192.168.1.11:9999' ,
        }
"""


"""
        免费代理IP的使用 

import requests

url = 'http://httpbin.org/get'
headers = { 'User-Agent':'Mozilla/5.0'}
proxies = {
    'http' : 'http://60.188.241.255:3000' ,
    'http' : 'http://60.188.241.255:3000' ,
}
# 测试
html = requests.get(url=url , proxies=proxies ,headers=headers).text
print(html)
# html = requests.get(url=url , headers=headers).text
# print(html)

"""



""" 
                构建代理IP池
抓取西刺免费高匿代理,并测试是否可用,建立免费代理IP池
!!! 西刺代理网址已失效
URL地址:
        https://www.xicidaili.com/nn/1 (西刺代理,已失效)
        https://www.kuaidaili.com/free/inha/{n}/ (快代理网址 , 目前可用)
将可用代理IP保存到本地文件中
测试: 可使用代理IP向测试网站请求,根据HTTP响应码来判定是否可用
"""
import requests
from lxml import etree
import time
import random
from fake_useragent import UserAgent

class Proxypool:
    def __init__(self):
        self.url = 'https://www.xicidaili.com/nn/{}'
        self.test_url = 'http://httpbin.org/get'

    # 获取代理IP
    def get_proxy(self , url):
        headers = {'User-Agent':UserAgent().random}
        # html = requests.get(url=url,headers=headers).text
        html = requests.get(url=url, headers=headers, verify=False).text
        # 解析提取代理IP
        p = etree.HTML(html)
        tr_list = p.xpath('//tr')
        for tr in tr_list[1:] :
            ip_list = tr.xpath('./td[2]/text()')
            ip = ip_list[0].strip() if ip_list else None
            port_list = tr.xpath('./td[3]/text()')
            port = port_list[0].strip() if port_list else None
            # 测试此ip和port是否可用
            self.test_proxy(ip , port)


    def test_proxy(self ,ip ,port):
        # 测试一个代理IP是否可用
        proxies = {
            'http' : 'http://{}:{}'.format(ip , port),
            'https' : 'https://{}:{}'.format(ip , port),
        }
        try:
            resp = requests.get(url=self.test_url,proxies=proxies,timeout=3)
            if resp.status_code == 200 :
                print(ip , port , '可用IP')
            else :
                print(ip , port , '不可用IP')
        except:
            print(ip , port ,'不可用IP')


    def run(self):
        for pg in range(1,1001):
            page_url = self.url.format(pg)
            self.get_proxy(url=page_url)
            # 控制数据抓取的频率
            time.sleep(random.randint(2,4))

if __name__ == '__main__':
    spider = Proxypool()
    spider.run()




















