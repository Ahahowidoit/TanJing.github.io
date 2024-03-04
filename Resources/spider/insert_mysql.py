""" 将数据存入到 Mysql 数据库中 """
import pymysql

# 1.创建数据库连接对象
db = pymysql.connect('localhost','root','123456','mydb',charset='utf8')

# 2.创建游标对象
cur = db.cursor()

# 3.执行SQL命令
ins = 'insert into mytab values(%s,%s,%s)'
li = ['大话西游','周星驰','1994-01-01']
cur.execute(ins,li)

# 4.提交到数据库执行
db.commit()

# 5.关闭游标
cur.close()

# 6.断开数据库连接
db.close()


""" 将数据存入到 csv 文件中  csv模块示例 """
import csv

with open('test.csv' , 'w') as f:
    # 初始化 csv 文件的写入对象
    writer = csv.writer(f)
    writer.writerow(['大话西游','周星驰','1994-01-01'])



""" python 与 MongoDB 交互
    库名 : testdb
    集合名 : testset
    文档 : {'name':'雄霸' ,'tools':'三分归元气'}
"""
# 1.创建数据库连接对象
conn = pymysql.MongoClient('localhost' , 27017)
# 2.创建库对象
db =conn['testdb']
# 3.创建集合对象
myset = db['testset']
# 4.插入文档
myset.inset_one({'name':'雄霸' ,'tools':'三分归元气'})




