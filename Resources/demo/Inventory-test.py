'''
            历史库存查询 , 按天输出行
            此代码以博越数据库 2019 年库存查询为例 , 将库存数据输出为Excel文件后保存在代码路径
            查询其余年度库存需替换数据库连接信息/SQL查询语句/查询中引用的日期遍历变量i
'''

from datetime import datetime, timedelta
import pyodbc
import pandas as pd

input_start_date = input("请输入查询开始日期(格式形如2023-01-01):")
input_edd_date = input("请输入查询结束日期(格式形如2023-01-01):")

# 创建日期变量列表 , 元素为查询日期的每一天
start_date = datetime.strptime(input_start_date, '%Y-%m-%d')
end_date = datetime.strptime(input_edd_date, '%Y-%m-%d')
delta = timedelta(days=1)

date_list = []

while start_date <= end_date:
    date_list.append(start_date.strftime('%Y-%m-%d'))
    start_date += delta


# 连接数据库 , 按需更换数据库连接信息
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=222.221.246.99;'
    'DATABASE=YTXdata;'
    'UID=user;'
    'PWD=ytxdata;'
)
cursor = conn.cursor()

# 创建一个空列表，用于存储所有行数据
rows = []

# 遍历生成的日期列表 ,引入sql查询语句 ,根据查询年份的不同更换sql语句和sql中where后日期筛选的i
for i in date_list:
    query = f'''
    SELECT
        A.[仓库名称],
        CASE 
            WHEN A.[仓库名称] = 'KA' THEN '昆明机场一店'
            WHEN A.[仓库名称] = 'KC' THEN '昆明机场三店'
            WHEN A.[仓库名称] = 'KH' THEN '昆明机场五店'
            WHEN A.[仓库名称] = '怡泰祥HA店' THEN '洲际店'
            WHEN A.[仓库名称] IN('大理一店', '大理二店', '大理三店') THEN '大理店'
            WHEN A.[仓库名称] IN('丽江一店', '丽江二店', '丽江三店') THEN '丽江店'
            WHEN A.[仓库名称] IN('版纳一店', '版纳怡禧A店')  THEN '版纳店'
            ELSE '其他'
        END AS 大门店,
        B.[品类],
        CASE
            WHEN A.[零售价] >= 0 AND A.[零售价] < 500 THEN '0_500元'
            WHEN A.[零售价] >= 500 AND A.[零售价] < 1000 THEN '500_1000元'
            WHEN A.[零售价] >= 1000 AND A.[零售价] < 5000 THEN '1000_5000元'
            WHEN A.[零售价] >= 5000 AND A.[零售价] < 10000 THEN '5000_10000元'
            WHEN A.[零售价] >= 10000 AND A.[零售价] < 50000 THEN '1万_5万元'
            WHEN A.[零售价] >= 50000 AND A.[零售价] < 100000 THEN '5万_10万元'
            WHEN A.[零售价] >= 100000 AND A.[零售价] < 500000 THEN '10万_50万元'
            WHEN A.[零售价] >= 500000 AND A.[零售价] < 1000000 THEN '50万_100万元'
            WHEN A.[零售价] >= 1000000 THEN '100万元以上'
            ELSE 'other'
        END AS 价格段,
        SUM (库存数量) 库存数量,
        SUM (库存金额) 库存成本,
        SUM ([库存标价额])  库存零售价
    FROM [F_库存与结存] AS A
    LEFT JOIN [D_五级分类] AS B ON A.[五级编码] = B.[五级编码]
    WHERE [开单日期] BETWEEN '2019-01-01 00:00:00' AND '{i} 23:59:59'
    AND CASE 
        WHEN A.[仓库名称] = 'KA' THEN '昆明机场一店'
        WHEN A.[仓库名称] = 'KC' THEN '昆明机场三店'
        WHEN A.[仓库名称] = 'KH' THEN '昆明机场五店'
        WHEN A.[仓库名称] = '怡泰祥HA店' THEN '洲际店'
        WHEN A.[仓库名称] IN('大理一店', '大理二店', '大理三店') THEN '大理店'
        WHEN A.[仓库名称] IN('丽江一店', '丽江二店', '丽江三店') THEN '丽江店'
        WHEN A.[仓库名称] IN('版纳一店', '版纳怡禧A店')  THEN '版纳店'
        ELSE '其他'
    END != '其他' 
    GROUP BY
        A.[仓库名称],
        CASE 
            WHEN A.[仓库名称] = 'KA' THEN '昆明机场一店'
            WHEN A.[仓库名称] = 'KC' THEN '昆明机场三店'
            WHEN A.[仓库名称] = 'KH' THEN '昆明机场五店'
            WHEN A.[仓库名称] = '怡泰祥HA店' THEN '洲际店'
            WHEN A.[仓库名称] IN('大理一店', '大理二店', '大理三店') THEN '大理店'
            WHEN A.[仓库名称] IN('丽江一店', '丽江二店', '丽江三店') THEN '丽江店'
            WHEN A.[仓库名称] IN('版纳一店', '版纳怡禧A店')  THEN '版纳店'
            ELSE '其他'
        END,
        B.[品类],
        CASE
            WHEN A.[零售价] >= 0 AND A.[零售价] < 500 THEN '0_500元'
            WHEN A.[零售价] >= 500 AND A.[零售价] < 1000 THEN '500_1000元'
            WHEN A.[零售价] >= 1000 AND A.[零售价] < 5000 THEN '1000_5000元'
            WHEN A.[零售价] >= 5000 AND A.[零售价] < 10000 THEN '5000_10000元'
            WHEN A.[零售价] >= 10000 AND A.[零售价] < 50000 THEN '1万_5万元'
            WHEN A.[零售价] >= 50000 AND A.[零售价] < 100000 THEN '5万_10万元'
            WHEN A.[零售价] >= 100000 AND A.[零售价] < 500000 THEN '10万_50万元'
            WHEN A.[零售价] >= 500000 AND A.[零售价] < 1000000 THEN '50万_100万元'
            WHEN A.[零售价] >= 1000000 THEN '100万元以上'
            ELSE 'other'
        END
    HAVING
        SUM(库存数量) != 0
    '''
    cursor.execute(query)
    data = cursor.fetchall()

    # 遍历查询结果 ,i作为第一个元素 ,并将每列数据添加到 rows 列表中
    for row_data in data:
        row = [
            i ,
            row_data[0],
            row_data[1],
            row_data[2],
            row_data[3],
            row_data[4],
            row_data[5],
            row_data[6]
        ]
        rows.append(row)

# 键入列表中的元素 , 后续为 DataFrame 创建列名
column_names = ['库存日期','仓库名称', '大门店', '品类', '价格段', '库存数量', '库存成本', '库存零售价']

# 使用 from_records() 方法将 rows 转换为 DataFrame , 并将column_names中的元素作为列名
df = pd.DataFrame.from_records(rows, columns=column_names)
# print(df)

# 指定文件名和是否包含索引 , 输出库存数据为Excel
df.to_excel('inventory_output2019.xlsx', index=False)
print("DataFrame已成功导出到Excel文件。")

# 关闭数据库连接
cursor.close()
conn.close()