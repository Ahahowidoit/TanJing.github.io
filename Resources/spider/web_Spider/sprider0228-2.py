"""
        采集百度电影热搜-结构化采集(无界面浏览器)
            https://top.baidu.com/board?tab=movie
"""

# 1.导入浏览器驱动工具
from pandas import Series, DataFrame
from selenium.webdriver import Chrome , ChromeOptions
from selenium.webdriver.common.by import By

# 2.使用驱动打开浏览器
# with Chrome() as driver:
option = ChromeOptions()
option.add_argument("--haedless")
with Chrome(options=option) as driver:
    # 3.访问web页面
    driver.get("https://top.baidu.com/board?tab=movie")
    # '//div[@class="c-single-text-ellipsis"]','//标签名[@属性名="内容"]'
    # Alt+回车 导入包 , Ctrl+鼠标左键打开文档
    # By返回一个webElement列表 ,包含XPATH表示的所有内容
    # 4.获取html标签
    list_result = []
    # 所有行
    for item in driver.find_elements(By.XPATH,'//div[@class="category-wrap_iQLoo "]'):
        # 改行的列xpath必须使用相对路径.开头
        dict_movie = {
            "电影名称":item.find_element(By.XPATH,'.//div[@class="c-single-text-ellipsis"]').text,
            "电影类型":item.find_element(By.XPATH,'.//div[@class="content_1YWBm"]/div[1]').text,
            "演员":item.find_element(By.XPATH,'.//div[@class="content_1YWBm"]/div[2]').text,
            "剧情描述":item.find_element(By.XPATH,'.//div[@class="content_1YWBm"]/div[3]').text,
            "热搜指数":item.find_element(By.XPATH,'.//div[@class="hot-index_1Bl1a"]').text
        }
        list_result.append(dict_movie)

    save_path ="D:/Users/Desktop/test/code/test_code/save_test/"
    DataFrame(list_result).to_excel(f"{save_path}百度热搜电影结构化爬取.xlsx",index=False)

print(f"程序结束\n请到{save_path}路径下查看\n输出文件名为:百度热搜电影结构化爬取.xlsx")

