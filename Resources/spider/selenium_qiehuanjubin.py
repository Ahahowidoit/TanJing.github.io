"""
切换句柄 : 爬取民政部 2022 年行政区划代码
"""
import time

from selenium import webdriver
from selenium.webdriver.common.by import By


class MzbSpider:
    def __init__(self):
        self.url = 'https://www.mca.gov.cn/n156/n2679/index.html'
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(url=self.url)


    def get_html(self):
        self.driver.find_element(By.XPATH,'//*[@id="comp_6934"]/table/tbody/tr[7]/td[2]/a').click()
        time.sleep(1)
        # 获取并切换句柄
        all_handles = self.driver.window_handles
        self.driver.switch_to.window(all_handles[1])
        # 解析提取数据
        self.parse_html()

    def parse_html(self):
        """解析提取数据"""
        tr_list = self.driver.find_elements(By.XPATH,'//tr[@height="19"]')
        i = 0
        for tr in tr_list:
            i = i+1
            # print(len(tr.text))
            item = {}
            if len(tr.text) >= 11 :
                info_list = tr.text.split()
                item['name'] = info_list[1].strip()
                item['code'] = info_list[0].strip()
                print(item)
            else:
                continue
                # break
        print(i)



    def run(self):
        self.get_html()

if __name__ == '__main__':
    spider = MzbSpider()
    spider.run()

