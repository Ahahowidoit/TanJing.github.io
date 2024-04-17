"""
    识别图片中的文字 , 并将识别到的内容存储到 Excel中 ;
    Python中的 Pillow 库来读取图片 , 以及使用 OpenCV 或者 PyTesseract 来进行图片内容的识别
    Image.open() 函数只能打开本地文件，无法直接打开远程 URL。要处理远程图片，可以使用 requests 库来下载图片后再进行识别
"""
from PIL import Image
import pytesseract
import cv2
import os
from openpyxl import Workbook


# 设置路径
# 图片所在的路径
image_folder = r'D:\Users\Desktop\test\code\test_code\Img'
# 识别后的表格存储的路径
excel_file = r'D:\Users\Desktop\test\code\test_code\Feature\images_content.xlsx'

# 初始化Excel工作簿和表格
wb = Workbook()
ws = wb.active
ws.append(['Image Name', 'Content'])

# 循环处理每张图片
for filename in os.listdir(image_folder):
    if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
        image_path = os.path.join(image_folder, filename)

        # 读取图片
        img = Image.open(image_path)

        # # 使用OpenCV读取图片，如果你选择了使用OpenCV进行内容识别
        # image = cv2.imread(image_path)
        # content = pytesseract.image_to_string(image)

        # 使用Pillow库进行图片内容识别
        # content = pytesseract.image_to_string(img, lang='eng')
        content = pytesseract.image_to_string(img, lang='chi_sim')  # 使用简体中文语言包

        # 将识别的内容存储到Excel中
        ws.append([filename, content])

# 保存Excel文件
wb.save(excel_file)
