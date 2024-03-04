"""
    反反爬
"""

import os
from selenium.webdriver import Chrome , ChromeOptions
import platform

options = ChromeOptions()
os_name = platform.system()

with Chrome() as driver:
    driver.get("https://www.douyin.com/")
    input()








