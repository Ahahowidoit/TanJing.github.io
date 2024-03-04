# ###  创建一个按钮
# from tkinter import *
# def xinlabel():
#     global xin
#     s = Label(xin , text = '完成')
#     s.pack()
# xin = Tk()
# b1 = Button(xin ,text = '下一步' , command = xinlabel)
# b1.pack()
# xin.mainloop()



## 输出日历 (时间设定为2023年5月)
import calendar  # 导入日历
year = int(2023) # 设定年
moon = int(5)  # 设定月
print(calendar.month(year,moon))  # 输出日历


import time  # 添加时间模块
ticks = time.time()
print(f'2023年5月23日17时20分的时间戳为:',ticks)  #时间戳模式



# localtime()函数用于捕获当前的时间
localtim = time.localtime(time.time())
print(f'当前时间为:',localtim)
# 输出结果为:2023年5月23日,17时25分14秒,星期四,全年第143天

# 格式化另外一种时间形式
# 格式化当前时间
print(time.strftime(f'当前时间为: %Y-%m-%d %H:%M:%S',time.localtime()))

