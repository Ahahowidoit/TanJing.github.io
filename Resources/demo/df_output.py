import pandas as pd
from itertools import combinations # 迭代工具
# import mysql.connector
from sqlalchemy import create_engine

# 建立与MySQL数据库的连接 (警告)
# cnx = mysql.connector.connect(
#     host='120.78.139.194',
#     user='information',
#     password='information123',
#     database='ytxEbao' )
# query = "SQL代码"
# df = pd.read_sql(query, con=cnx)

# 创建与MySQL数据库的连接
engine = create_engine('mysql+mysqlconnector://information:information123@120.78.139.194/ytxEbao')

# 执行SQL查询并读取结果到DataFrame
query = '''
SELECT A.user_id AS USER_ID,
C.name AS 二级名称 , D.name AS 三级名称 ,
CONCAT_WS('-', C.name , D.name ) AS 分类聚合
FROM `tbl_order_shipping_analysis` AS A 
LEFT JOIN tbl_goods AS B ON A.goods_id = B.id
LEFT JOIN tbl_goods_type AS C ON B.type_id = C.id
LEFT JOIN tbl_goods_subclass AS D ON B.subclass_id = D.id
WHERE A.order_type IN (1, 5, 9)
AND A.user_id IN 
    (SELECT E.user_id 
        FROM (
            SELECT A.user_id , COUNT(A.order_id) AS order_count ,
                 C.name AS 二级名称 , D.name AS 三级名称 ,
                 CONCAT_WS('-', C.name , D.name )  AS 分类聚合
            FROM `tbl_order_shipping_analysis` AS A 
            LEFT JOIN tbl_goods AS B ON A.goods_id = B.id
            LEFT JOIN tbl_goods_type AS C ON B.type_id = C.id
            LEFT JOIN tbl_goods_subclass AS D ON B.subclass_id = D.id
            WHERE A.order_type IN (1, 5, 9) 
            AND A.order_at < '2023-08-01 00:00:00'
            GROUP BY A.user_id
            ) AS E 
    WHERE E.order_count > 2)
'''
df = pd.read_sql(query, con=engine)

# #读取 Excel文件
# df = pd.read_excel('0802.xlsx')

# 按照USER_ID 对商品组合聚合并添加到列表
grouped = df.groupby('USER_ID')['分类聚合'].apply(list)

# 统计所有商品组合出现的次数
pair_counts = {}
for transactions in grouped:
    pairs = list(combinations(transactions, 2))  # 获取任意两个商品的组合
    for pair in pairs:
        if pair in pair_counts:
            pair_counts[pair] += 1
        else:
            pair_counts[pair] = 1

for pair, count in pair_counts.items():
    print(f"商品组合: {pair}, 出现次数: {count}")

# 用结果创建 DataFrame
result_df = pd.DataFrame({'商品组合': list(pair_counts.keys()), '出现次数': list(pair_counts.values())})

# 保存为Excel文件
result_df.to_excel('商品组合出现次数.xlsx', index=False)
print("程序结束 ！")

# 关闭数据库连接
engine.dispose()