"""
        使用selenium+浏览器组合,爬取百度热搜小说第一页,并使用Series存储到Excel中
            https://top.baidu.com/board?tab=novel&sa=fyb_novel_31065
"""

from pandas import Series
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

with Chrome() as driver:
    driver.get("https://top.baidu.com/board?tab=novel&sa=fyb_novel_31065")
    #//div[@class="c-single-text-ellipsis"]
    # list_result = []
    # for item in driver.find_elements(By.XPATH,'//div[@class="c-single-text-ellipsis"]'):
    #     list_result.append(item.text)

    #函数式编程写法
    list_result=list(map(lambda item:item.text,driver.find_elements(By.XPATH,'//div[@class="c-single-text-ellipsis"]')))

    series_novel = Series(list_result,name="小说名称")
    series_novel.to_excel("D:/Users/Desktop/test/code/test_code/save_test/百度热搜小说标题.xlsx",index=False)
print("程序已结束")

