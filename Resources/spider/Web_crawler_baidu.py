from urllib import parse

import requests
from bs4 import BeautifulSoup

# ### 爬取百度搜索页面
#
# # 构造请求头部信息
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
#
# # 构造查询参数
# # params参数是一个包含了三个键值对的字典,使用requests库发送GET请求时，将这个字典作为参数传入，
# # requests库会将其自动拼接成URL的查询字符串，然后将其附带到URL结尾，发送给服务器。
# # 最后输出response.request.url，可以查看发送到服务器的完整URL，即可发现URL的结尾附带了我们构造的查询参数
# url = 'https://www.baidu.com/s'
# params = {'wd': 'Python爬虫'}
# print(params)
# # 发送请求，获取响应
# response = requests.get(url, headers=headers, params=params)
# response.encoding = 'utf-8'
#
# # 创建BeautifulSoup对象解析页面内容
# soup = BeautifulSoup(response.text, 'html.parser')
#
# # 提取搜索结果内容
# results = soup.find_all('div', class_='result')
# for result in results:
#     # 获取标题和链接信息
#     title = result.find('h3', class_='t').get_text()
#     link = result.find('a').get('href')
#     print(title, link)
#
import requests
from bs4 import BeautifulSoup
# 编码模块的使用
# 导入编码模块
import urllib.parse
# from urllib import parse
# params = parse.urlencode
# # 网址 :http://www.baidu.com/s?wd=赵丽颖
# print(params)


# 第一版
# -*-coding:utf-8-*-
import os
import re
import time
import requests
import bs4
from bs4 import BeautifulSoup

# 手动写入目标套图的首页地址
download_url = "https://www.xgmn09.com/XiaoYu/XiaoYu23172.html"

# 手动写入目标套图的页数
page_num = 25

# 创建一个文件夹用来保存图片
file_name = "测试图库"

# 目标图片下载地址的前半部分(固定不变那部分，后半段是变化的，需要解析网页得到)
imgae_down_url_1 = "https://jpxgyw.net"


# 创建文件夹
def CreateFolder(file):
    """创建存储数据文件夹"""
    flag = 1
    while flag == 1:  # 若文件已存在，则不继续往下走以免覆盖了原文件
        if not os.path.exists(file):
            os.mkdir(file)
            flag = 0
        else:
            print('该文件已存在，请重新输入')
            flag = 1
            time.sleep(1)
        # 返回文件夹的路径，这里直接放这工程的根目录下
        path = os.path.abspath(file) + "\\"
    return path


# 下载图片
def DownloadPicture(download_url, list, path):
    # 访问目标网址
    r = requests.get(url=download_url, timeout=20)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "html.parser")

    # 解析网址，提取目标图片相关信息，注：这里的解析方法是不固定的，可以根据实际的情况灵活使用
    p = soup.find_all("p")
    tag = p[0].find_all("img")  # 得到该页面目标图片的信息

    # 下载图片
    j = 0
    for i in range(list, list + 3):
        if (j < len(tag) and tag[j].attrs['src'] != None):
            img_name = str(i) + ".jpg"  # 以数字命名图片，图片格式为jpg
            # 获取目标图片下载地址的后半部分
            imgae_down_url_2 = tag[j].attrs['src']
            j = j + 1
            # 把目标图片地址的前后两部分拼接起来，得到完整的下载地址
            imgae_down_url = imgae_down_url_1 + imgae_down_url_2
            print("imgae_down_url: ", imgae_down_url)

            # 下载图片
            try:
                img_data = requests.get(imgae_down_url)
            except:
                continue
            # 保存图片
            img_path = path + img_name
            with open(img_path, 'wb') as fp:
                fp.write(img_data.content)
            print(img_name, "   ******下载完成！")


# 主函数
if __name__ == "__main__":
    # 创建保存数据的文件夹
    path = CreateFolder(file_name)
    print("创建文件夹成功: ", path)

    # 按页下载图片
    for i in range(0, page_num):
        if i == 0:
            page_url = download_url  # 首页网址，注：因为这个网站首页和后面那些页面网址的规则不一样，所以这里要区分开来
        else:
            page_url = download_url[:-5] + "_" + str(i) + ".html"  # 第2页往后的网址，都是用数字来排布页面
        # 下载图片
        # print("page_url: ", page_url)
        DownloadPicture(page_url, i * 3, path)  # 注:这个网站每一页最多是3张图片，每张图片我都用数字命名

    print("全部下载完成！", "共" + str(len(os.listdir(path))) + "张图片")




# 第二版
# -*-coding:utf-8-*-
import os
import re
import time
import requests
import bs4
from bs4 import BeautifulSoup

# 手动写入目标套图的首页地址
download_url = "https://www.xgmn09.com/XiaoYu/XiaoYu23172.html"

# 这里不需要手动输入页面数量了，可以通过解析首页地址得到总页面数
# page_num = 25

# 文件保存的绝对路径(D:\imgae\test_file)，注：这个路径上面的文件夹一定是要已经创建好了的，不然运行会报错
file_path = "D:\\imgae\\test_file"

# 文件名通过网页得到，注：以网页上套图的名字命名
file_name = " "

# 目标图片下载地址的前半部分，注：固定不变那部分，后半段是变化的，需要解析网页得到
imgae_down_url_1 = "https://jpxgyw.net"

# 修改请求headers以伪装成浏览器访问，从而绕开网站的反爬机制获取正确的页面，注：这个需要根据自己浏览器的实际的信息改
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
}

# 访问网页并返回HTML相关的信息
def getHTMLText(url, headers):
    # 向目标服务器发起请求并返回响应
    try:
        r = requests.get(url=url, headers=headers, timeout=20)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, "html.parser")
        return soup
    except:
        return ""


# 获取该套图的名称和总页面数
def getFileName(url, headers):
    # 从目标地址上面获取套图的名称
    soup = getHTMLText(url, headers)
    head1 = soup.find_all("header")
    h1 = head1[1].find_all("h1")
    name = h1[0].text
    pagination = soup.find_all("div", "pagination")
    a = pagination[0].find_all("a")
    page = int(a[len(a) - 2].text)
    return name, page

# 创建文件夹
def CreateFolder(file_name):
    flag = True
    num = 0
    while flag == 1:
        if num <= 0:
            file = file_path + '\\' + file_name  # 如果文件夹不存在，则创建文件夹
        else:
            file = file_path + '\\' + str(num) + '_' + file_name  # 如果文件夹已存在，则在文件夹前面加上数字，防止覆盖掉以前保存过的文件
        if not os.path.exists(file):
            os.mkdir(file)
            flag = False
        else:
            print('该文件名已存在，已重新命名')
            flag = True
            num += 1
            # time.sleep(1)
    # 返回文件存放的路径
    path = os.path.abspath(file) + '\\'
    return path

# 下载图片
def DownloadPicture(url, img_num, path):
    # 访问目标网址
    soup = getHTMLText(url, headers)

    # 解析网址，提取目标图片相关信息，注：这里的解析方法是不固定的，可以根据实际的情况灵活使用
    p = soup.find_all("p")
    tag = p[0].find_all("img")  # 得到该页面目标图片的信息

    # 下载图片
    for i in range(0, len(tag)):
        if (tag[i].attrs['src'] != None):
            # 解析网址，得到目标图片的下载地址
            imgae_down_url_2 = tag[i].attrs['src']  # 获取目标图片下载地址的后半部分
            imgae_url = imgae_down_url_1 + imgae_down_url_2  # 把目标图片地址的前后两部分拼接起来，得到完整的下载地址
            print("imgae_url: ", imgae_url)
            # 给图片命名
            img_num += 1
            name = tag[i].attrs['alt'] + '_' + str(img_num)  # 获取img标签的alt属性，用来给保存的图片命名，图片格式为jpg
            img_name = name + ".jpg"
            # 下载图片
            timeout = 5  # 超时重连次数
            while timeout > 0:
                try:
                    img_data = requests.get(url=imgae_url, headers=headers, timeout=30)
                    # 保存图片
                    img_path = path + img_name
                    with open(img_path, 'wb') as fp:
                        fp.write(img_data.content)
                    print(img_name, "******下载完成！")
                    timeout = 0
                except:
                    print(img_name, "******等待超时，下载失败！")
                    time.sleep(1)
                    timeout -= 1
    return img_num

# 主函数
if __name__ == "__main__":
    # 记录下载时间
    start = time.time()

    # 检查网址，如果输入的网址不是首页，则改成首页地址
    result = download_url.find('_')
    if(result != -1):
        new_str = ''
        check_flag = 1
        for i in range(0, len(download_url)):
            if(download_url[i] != '_' and check_flag):
                new_str = new_str + download_url[i]
            else:
                if(download_url[i] == '_'):
                    check_flag = 0
                if(download_url[i] == '.'):
                    new_str = new_str + download_url[i]
                    check_flag = 1
        download_url = new_str
        print("new download_url: ", download_url)

    # 创建保存数据的文件夹
    file_name, page_num = getFileName(download_url, headers)  # 获取套图名称
    print("page_num: ", page_num)
    path = CreateFolder(file_name)
    print("创建文件夹成功: ", path)

    # 按页下载图片
    image_num = 0  # 当前累计下载图片总数
    for i in range(0, int(page_num)):
        if i == 0:
            page_url = download_url  # 首页网址，注：因为这个网站首页和后面那些页面网址的规则不一样，所以这里要区分开来
        else:
            page_url = download_url[:-5] + "_" + str(i) + ".html"  # 第2页往后的网址，都是用数字来排布页面
        # 下载图片
        print("page_url: ", page_url)
        image_num = DownloadPicture(page_url, image_num, path)
        # image_num = num  # 每下载完一页图片就累计当前下载图片总数

    print("全部下载完成！", "共" + str(len(os.listdir(path))) + "张图片")

    # 打印下载总耗时
    end = time.time()
    print("共耗时" + str(end - start) + "秒")





import requests

url = 'https://www.baidu.com/'
response = requests.get(url)
print(response.status_code)  # 打印响应状态码
if response.status_code == 200:
    print(response.text)  # 打印网页HTML源代码
# 通过 requests.get()函数来实现对百度首页的请求，将返回的响应结果保存在response变量中。
# 调用 status_code() 方法获取响应状态码，
# 如果状态码为200则表示请求成功，并调用 text 属性获取网页HTML源代码，最后将网页代码输出到控制台上。

import requests

url = 'https://www.xxx.com/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
data = {'username': 'xxx', 'pw': '123456'}
response = requests.post(url, headers=headers, data=data)
print(response.json())  # 打印JSON格式响应数据
# 该示例代码利用 requests.post() 方法向一个URL发起POST请求，并通过设置请求头及请求数据，模拟用户登录行为。
# 调用 json() 属性解析返回的JSON格式数据，最终输出结果到控制台。



# Python爬虫示例，用于从指定网站上获取小说内容
import requests
from bs4 import BeautifulSoup

url = 'https://www.example.com/novel/1234'
response = requests.get(url)   # 发送请求

if response.status_code == 200:  # 判断是否成功响应
	soup = BeautifulSoup(response.content, 'html.parser')
	title = soup.h1.text.strip()  # 获取小说名称
	content = soup.find(id='content')  # 查找小说内容
	content = content.text.replace('\r\n\r\n', '\n').strip()  # 清理字符串的空白和换行符

	with open(title + '.txt', 'w', encoding='utf-8') as file:
    	    file.write(content)

	print('小说{}已经存储在本地文件{}中'.format(title, title+'.txt'))
else:
	print('小说获取失败')

from selenium import webdriver
import time
import xlwt
import datetime



'''get the url of the aim'''
url = '初始网址'

browser = webdriver.Chrome('/Users/kakufumisakai/Downloads/chromedriver')
browser.get(url)
time.sleep(10)

html_text = browser.page_source

time.sleep(5)

# get all elements that their css style contian class = 'extra-header-right'
elements = browser.find_elements_by_css_selector("[class = 'extra-header-right']")
# get the aim
element = elements[1]
browser.execute_script("arguments[0].click()", element)
# get the url of the aim
aimurl = browser.current_url

'''drop the scroll bar'''
js = "return action = document.body.scrollHeight"
height = browser.execute_script(js)

browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
time.sleep(5)

dates = browser.find_elements_by_xpath("//uni-view[@class = 'item item']/uni-view[@class = 'time']")

status = True

# Number
num = 0
# the position of starting index
n = 0

# judge the last date in one page is more than 5, or less than 5. former, flag = 1, else flag = 0
flag = 0

while status:
    for date in dates[n:]:
        num += 1
        if date.text[1] in ['小', '分', '秒', '天'] or date.text[2] in ['小', '分', '秒']:
            if date.text[1] == '天' and date.text[0] > '5':
                flag = 1
                break
        else:
            flag = 1
            break

    if flag == 0:
        new_height = browser.execute_script(js)
        if new_height > height:
            time.sleep(1)
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            # get the new page's height
            height = new_height
    else:
        print("已抓取完所需要的信息")
        status = False
        browser.execute_script('window.scrollTo(0, 0)')
        break

    time.sleep(3)
    n = num
    dates = browser.find_elements_by_xpath("//uni-view[@class = 'item item']/uni-view[@class = 'time']")

time.sleep(2)
html_text = browser.page_source
time.sleep(2)
names = browser.find_elements_by_xpath("//uni-view[@class = 'item item']/uni-view[@class = 'info']")
things = browser.find_elements_by_xpath("//uni-view[@class = 'item item']/uni-view[@class = 'title']")
prices = browser.find_elements_by_xpath("//uni-view[@class = 'item item']/uni-view[@class = 'price']")

'''save in excel'''
n = 0
datas = xlwt.Workbook()

sheet1 = datas.add_sheet(u'purchase', cell_overwrite_ok=True)

rowTitle = [u'用户名', u'商品', u'价格', u'购买时间']

for i in range(0, len(rowTitle)):
    sheet1.write(0, i, rowTitle[i])

for j in range(1, num):
    sheet1.write(j, 0, names[j - 1].text)
    sheet1.write(j, 1, things[j - 1].text)
    sheet1.write(j, 2, prices[j - 1].text)

'''cope with the time'''
z = 1
for date in dates[0:num - 1]:
    if date.text[2] in ['小', '分', '秒'] or date.text[1] in ['小', '分', '秒']:
        dt = datetime.datetime.now()
        if date.text[2] == '小':
            if dt.hour < int(date.text[0:2]):
                dt -= datetime.timedelta(days=1)
        elif date.text[1] == '小':
            if dt.hour < int(date.text[0]):
                dt -= datetime.timedelta(days=1)
        m = str(dt.month) + '月' + str(dt.day) + '日'
        sheet1.write(z, 3, m)
    elif date.text[1] == '天':
        tmp = int(date.text[0])
        datestart = datetime.datetime.now()
        datestart -= datetime.timedelta(days=tmp)
        n = str(datestart.month) + '月' + str(datestart.day) + '日'
        sheet1.write(z, 3, n)
    else:
        sheet1.write(z, 3, date.text)
    z += 1

datas.save('purchase.xls')


