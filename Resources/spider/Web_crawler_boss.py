import requests
import pandas as pd
from bs4 import BeautifulSoup

# 构造请求头部信息
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# 构造查询参数和URL
url = 'https://www.zhipin.com/job_detail/?query=Python&scity=101010100'
params = {'page': 1}

# 创建一个空的dataframe，用于存储爬取的数据
df = pd.DataFrame()

# 爬取前5页数据
for page in range(1, 6):
    # 更新查询参数中的页码信息
    params['page'] = page

    # 发送请求，获取响应
    response = requests.get(url, headers=headers, params=params)
    response.encoding = 'utf-8'

    # 创建BeautifulSoup对象解析页面内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取搜索结果内容
    results = soup.find_all('div', class_='job-list')
    for result in results:
        # 获取职位名称、公司名称和薪资信息
        job_name = result.find('div', class_='job-name').get_text()
        company_name = result.find('div', class_='company-text').find('h3').get_text()
        salary = result.find('span', class_='red').get_text()

        # 将提取到的数据存储到dataframe中
        df = df.append({'职位名称': job_name, '公司名称': company_name, '薪资': salary}, ignore_index=True)

# 输出爬取到的数据
print(df)



