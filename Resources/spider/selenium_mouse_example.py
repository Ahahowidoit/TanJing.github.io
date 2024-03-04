"""
 selenium操作鼠标
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
# 导入鼠标事件类
from selenium.webdriver import ActionChains

#1.打开浏览器,输入百度地址
driver = webdriver.Chrome()
driver.maximize_window()
driver.get('http://www.baidu.com/')

#2.找到右上角设置节点,把鼠标移动过去
set_node = driver.find_element(By.XPATH,'//*[@id="s-usersetting-top"]')

# 3.移动鼠标
ActionChains(driver).move_to_element(to_element=set_node).perform()
# 谨记三步走 : 1.实例化 2.指定行为 3.执行行为




