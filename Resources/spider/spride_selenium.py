"""
        使用selenium+浏览器组合,爬取百度热搜新闻第一页,并使用Series存储到Excel中
            https://top.baidu.com/board?tab=realtime&sa=fyb_realtime_31065
"""

# 1.导入浏览器驱动工具
from pandas import Series
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

# 2.使用驱动打开浏览器
with Chrome() as driver:
    # 3.访问web页面
    driver.get("https://top.baidu.com/board?tab=realtime&sa=fyb_realtime_31065")

    # '//div[@class="c-single-text-ellipsis"]','//标签名[@属性名="内容"]'
    # Alt+回车 导入包 , Ctrl+鼠标左键打开文档
    # By返回一个webElement列表 ,包含XPATH表示的所有内容
    # 4.获取html标签
    list_result = []
    for item in driver.find_elements(By.XPATH,'//div[@class="c-single-text-ellipsis"]'):
        # 5.获取标签内的数据
        list_result.append(item.text)
        # print(item.text)

    # 6.保存数据
    series_title = Series(list_result,name='新闻标题')
    series_title.to_excel("D:/Users/Desktop/test/code/test_code/save_test/百度新闻热搜.xlsx",index=False)



    input()  # 使浏览器保持开启状态



