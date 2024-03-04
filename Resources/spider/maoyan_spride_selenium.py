"""
    使用selenium+Chrome抓取猫眼电影top100数据
1.打开浏览器
2.输入URL地址
3.table_list:匹配所有图书信息的table节点对象
4.for循环依次遍历,提取每个电影的信息
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

#设置浏览器无界面模式
options = webdriver.ChromeOptions()
options.add_argument('--headless')

# 1.打开浏览器
driver = webdriver.Chrome(options=options)

# 2.输入URL地址
driver.get('https://book.douban.com/top250?icn=index-book250-all')

def get_one_page():
    # 3.table_list:匹配所有图书信息的table节点对象
    table_list = driver.find_elements(By.XPATH,'//*[@id="content"]/div/div[1]/div/table')
    for table in table_list:
        # print(table.text)
        # print('*'*50)
        item = {}
        info_list = table.text.split('\n')
        if len(info_list) == 5:
            item['name'] = info_list[0].strip()
            item['book_info'] = info_list[2].strip()
            item['score'] = info_list[3].split('(')[0].strip()
            # item['commit'] = info_list[3].split('(')[1][1:-1].strip()
            item['comment'] = info_list[4].strip()
        elif len(info_list) == 4:
            item['name'] = info_list[0].strip()
            item['book_info'] = info_list[1].strip()
            item['score'] = info_list[2].split('(')[0].strip()
            # item['commit'] = info_list[2].split('(')[0][0:-1].strip()
            item['comment'] = info_list[3].strip()
        print(item)

while True:
    get_one_page()
    # 判断是否为最后一页,查找节点时,如果找不到会抛出异常
    try :
        driver.find_element(By.LINK_TEXT,'后页>').click()
        # 点击之后需要给页面元素加载预留时间
        time.sleep(1)
    except:
        driver.quit()
        break








