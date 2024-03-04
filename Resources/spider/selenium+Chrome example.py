"""示例代码 : 1.打开Chrome浏览器
2.输入百度URL地址 , 打开百度首页
3.找到搜索框节点 , 并发送文本 -
4.找到百度一下按钮 , 并进行模拟点击
"""
# 导入 selenium 的 webdriver 接口
from selenium import webdriver
from selenium.webdriver.common.by import By

# 1.创建浏览器对象 - 此时浏览器打开
browser = webdriver.Chrome() #chrome浏览器
# browser = webdriver.PhantomJS() #无界面浏览器 , selenium4.0版本已禁用

# 2.输入百度地址并确认
browser.get('http://www.baidu.com/')

# 浏览器窗口最大化
browser.maximize_window()

# 3.找到搜索框节点 , 并发送文本
# browser.find_element_by_xpath('//*[@id="kw"]').send_keys('赵丽颖') #在 Selenium 4.0 版本中，用于定位元素的方式有所改变,此写法已废弃
# browser.find_element(By.XPATH,'//*[@id="kw"]').send_keys('赵丽颖') #引入by方法

# 4.找到百度一下按钮 , 并进行模拟点击
# browser.find_element(By.XPATH,'//*[@id="su"]').click

# 获取屏幕快照
browser.save_screenshot('baidu.png')

# find()方法:没有找到,返回-1,经常用于判断是否最后一页
print(browser.page_source.find('aaaa'))

# 5. 关闭浏览器
# browser.quit()







