"""
    有道翻译
        https://fanyi.youdao.com/
"""
from selenium.webdriver import Chrome , ChromeOptions
from selenium.webdriver.common.by import By
import time

option = ChromeOptions()
option.add_argument("--haedless")
with Chrome(options=option) as driver:
    driver.get("https://fanyi.youdao.com/")
    input_txt = driver.find_element(By.XPATH ,'//div[@id="js_fanyi_input"]')


    while True :
        input_txt.send_keys(input("请输入要翻译的内容:"))
        # 如果网速慢,需要强制等待
        time.sleep(2)
        result = driver.find_element(By.XPATH, '//div[@id="js_fanyi_output"]//span[@class="tgt color_text_1"]').text
        print(result)
        input_txt.clear()   # 清空标签




