from fake_useragent import UserAgent
import requests
import os
""" 抓取图片到本地 
        一定要找到图片的真实完整URL地址
"""
url = 'https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fsafe-img.xhscdn.com%2Fbw1%2F7be91090-9aa6-4f32-89ea-9979324a6dc6%3FimageView2%2F2%2Fw%2F1080%2Fformat%2Fjpg&refer=http%3A%2F%2Fsafe-img.xhscdn.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1688866361&t=eb1567a67a56be7782cea706cdae1bc2'
url1 = 'https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fsafe-img.xhscdn.com%2Fbw1%2F9c5efebc-8284-42e5-836c-d3a798e2c10d%3FimageView2%2F2%2Fw%2F1080%2Fformat%2Fjpg&refer=http%3A%2F%2Fsafe-img.xhscdn.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1688867186&t=91af5f4d8e3be58d627524269f3afbfb'
url2 = 'https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fsafe-img.xhscdn.com%2Fbw1%2F650f5a4c-9bfc-4ef1-ae1f-8ebb6cd3e221%3FimageView2%2F2%2Fw%2F1080%2Fformat%2Fjpg&refer=http%3A%2F%2Fsafe-img.xhscdn.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1688867186&t=bf83679140ff130feb8a4491da70f9f5'
url3 = 'https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fsafe-img.xhscdn.com%2Fbw1%2F57d018e3-b9ff-490f-bfed-3b94d93e27c9%3FimageView2%2F2%2Fw%2F1080%2Fformat%2Fjpg&refer=http%3A%2F%2Fsafe-img.xhscdn.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1688867365&t=481bf0c812142061ed97dc55be71f37a'
url4 = 'https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fsafe-img.xhscdn.com%2Fbw1%2F57d018e3-b9ff-490f-bfed-3b94d93e27c9%3FimageView2%2F2%2Fw%2F1080%2Fformat%2Fjpg&refer=http%3A%2F%2Fsafe-img.xhscdn.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1688867365&t=481bf0c812142061ed97dc55be71f37a'
url5 = 'https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fc-ssl.duitang.com%2Fuploads%2Fblog%2F202107%2F16%2F20210716162038_5060f.png&refer=http%3A%2F%2Fc-ssl.duitang.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1688867603&t=192e0b06c1f7ebb0dae59c849b84131f'
url6 = 'https://img2.huashi6.com/images/resource/thumbnail/2022/02/03/2035_83548648415.jpg?imageMogr2/quality/75/interlace/1/thumbnail/700x%3E'
url7 = 'https://inews.gtimg.com/newsapp_bt/0/15112725378/1000'
pic_list = [url , url1 , url2 , url3 , url4 , url5 , url6 , url7 ]
num = ['pic1' , 'pic2' ,  'pic3' ,  'pic4' ,  'pic5' ,  'pic6' , 'pic7' ]
# print(pic_list)
headers = {'User-Agent' :UserAgent().random }

# 遍历列表中的每一个网址 , 一个URL请求一次 , 抓取保存本地
for item in pic_list:
    # 一定要使用content属性 , 因为图片是以二进制的方式存储的
    html = requests.get(url=item , headers=headers).content
    # 检查当前目录下是否存在名为 web_Spider 的文件夹，如果不存在，则创建一个新的文件夹
    if not os.path.exists('web_Spider'):
        os.mkdir('web_Spider')

# 保存图片到本地 ,二进制的文件 ,要用 'wb' 方式 , 一般结构化数据用 'w'方式
    for i , item in enumerate(pic_list):
        html = requests.get(url=item, headers=headers).content
        with open(f'web_Spider/pic{i + 1}.jpg', 'wb') as f:
            f.write(html)
print('图片下载完成，请在文件夹查看')