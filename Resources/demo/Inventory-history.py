import pyodbc
import pandas as pd
from datetime import datetime, timedelta

# 连接SQL Server数据库
print(pyodbc.drivers())
# 数据库连接设置
server = '222.221.246.99'
database = 'YTXdata'
username = 'user'
password = 'ytxdata'
cnxn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
cursor = cnxn.cursor()

# 设置起始和结束日期
start_date = datetime(2020, 1, 1)
end_date = datetime(2020, 1, 2)

# 创建一个空的DataFrame来存储所有库存数据
all_inventory_data = pd.DataFrame()

# 循环遍历日期范围
current_date = start_date
while current_date <= end_date:
    # 构建当前日期的查询条件
    next_date = current_date + timedelta(days=1)
    date_range = f"[开单日期] >= '{current_date.strftime('%Y-%m-%d')}' AND [开单日期] <= '{next_date.strftime('%Y-%m-%d')}'"
    # date_range = f"[开单日期] >= '{current_date.strftime('%Y-%m-%d %H:%M:%S')}' AND [开单日期] <= '{next_date.strftime('%Y-%m-%d %H:%M:%S')}'"
    # date_range = f"[开单日期] >= '{current_date.strftime('%Y-%m-%d 00:00:00')}' AND [开单日期] <= '{next_date.strftime('%Y-%m-%d 23:59:59')}'"


    # 查询当前日期的库存数据
    query = f'''
    SELECT
    YEAR([开单日期]) AS 年 ,
    MONTH([开单日期]) AS 月 ,
    DAY([开单日期]) AS 日 ,
    A.[仓库名称] ,
    CASE 
        WHEN A.[仓库名称] = 'KMA01' THEN '昆明机场一店'
        WHEN A.[仓库名称] = 'KMA03' THEN '昆明机场三店'
        WHEN A.[仓库名称] = 'KMA05' THEN '昆明机场五店'
        WHEN A.[仓库名称] = 'KMB01' THEN '洲际店'
        WHEN A.[仓库名称] IN('DLA01' ,'DLA02' ,'DLA03') THEN '大理店'
        WHEN A.[仓库名称] IN('LJA01' , 'LJA02' ,'LJA03') THEN '丽江店'
        WHEN A.[仓库名称] IN('BNA01' , 'BNA03' )  THEN '版纳店'
        ELSE '其他'
    END AS 大门店 ,
    B.[品类] ,
    CASE
        WHEN A.[零售价] >= 0
        AND A.[零售价] < 500 THEN '0_500元'
        WHEN A.[零售价] >= 500
        AND A.[零售价] < 1000 THEN '500_1000元'
        WHEN A.[零售价] >= 1000
        AND A.[零售价] < 5000 THEN '1000_5000元'
        WHEN A.[零售价] >= 5000
        AND A.[零售价] < 10000 THEN '5000_10000元'
        WHEN A.[零售价] >= 10000
        AND A.[零售价] < 50000 THEN '1万_5万元'
        WHEN A.[零售价] >= 50000
        AND A.[零售价] < 100000 THEN '5万_10万元'
        WHEN A.[零售价] >= 100000
        AND A.[零售价] < 500000 THEN '10万_50万元'
        WHEN A.[零售价] >= 500000
        AND A.[零售价] < 1000000 THEN '50万_100万元'
        WHEN A.[零售价] >= 1000000 THEN '100万元以上'
        ELSE 'other'
    END AS 价格段 ,
    SUM (库存数量) 库存数量 ,
    SUM (库存金额) 库存成本 ,
    SUM ([库存标价额])  库存零售价
    FROM [F_库存与结存] AS A LEFT JOIN [D_五级分类] AS B
    ON A.[五级编码] = B.[五级编码]
    WHERE {date_range}
    AND CASE 
        WHEN A.[仓库名称] = 'KMA01' THEN '昆明机场一店'
        WHEN A.[仓库名称] = 'KMA03' THEN '昆明机场三店'
        WHEN A.[仓库名称] = 'KMA05' THEN '昆明机场五店'
        WHEN A.[仓库名称] = 'KMB01' THEN '洲际店'
        WHEN A.[仓库名称] IN('DLA01' ,'DLA02' ,'DLA03') THEN '大理店'
        WHEN A.[仓库名称] IN('LJA01' , 'LJA02' ,'LJA03') THEN '丽江店'
        WHEN A.[仓库名称] IN('BNA01' , 'BNA03' )  THEN '版纳店'
        ELSE '其他'
    END != '其他' 
    GROUP BY
    YEAR([开单日期])  ,
    MONTH([开单日期]) ,
    DAY([开单日期])  ,
    仓库名称 ,
    B.[品类] ,
    CASE 
        WHEN A.[仓库名称] = 'KMA01' THEN '昆明机场一店'
        WHEN A.[仓库名称] = 'KMA03' THEN '昆明机场三店'
        WHEN A.[仓库名称] = 'KMA05' THEN '昆明机场五店'
        WHEN A.[仓库名称] = 'KMB01' THEN '洲际店'
        WHEN A.[仓库名称] IN('DLA01' ,'DLA02' ,'DLA03') THEN '大理店'
        WHEN A.[仓库名称] IN('LJA01' , 'LJA02' ,'LJA03') THEN '丽江店'
        WHEN A.[仓库名称] IN('BNA01' , 'BNA03' )  THEN '版纳店'
        ELSE '其他'
    END  ,
    CASE
        WHEN A.[零售价] >= 0
        AND A.[零售价] < 500 THEN '0_500元'
        WHEN A.[零售价] >= 500
        AND A.[零售价] < 1000 THEN '500_1000元'
        WHEN A.[零售价] >= 1000
        AND A.[零售价] < 5000 THEN '1000_5000元'
        WHEN A.[零售价] >= 5000
        AND A.[零售价] < 10000 THEN '5000_10000元'
        WHEN A.[零售价] >= 10000
        AND A.[零售价] < 50000 THEN '1万_5万元'
        WHEN A.[零售价] >= 50000
        AND A.[零售价] < 100000 THEN '5万_10万元'
        WHEN A.[零售价] >= 100000
        AND A.[零售价] < 500000 THEN '10万_50万元'
        WHEN A.[零售价] >= 500000
        AND A.[零售价] < 1000000 THEN '50万_100万元'
        WHEN A.[零售价] >= 1000000 THEN '100万元以上'
        ELSE 'other'
    END 
    HAVING
    SUM ( 库存数量 ) != 0
    '''

    if current_date > end_date:
        break

    # 使用pandas将结果存储到DataFrame中
    df = pd.read_sql(query, cnxn )
    print(df)
    df.to_excel(f"temp.xlsx", index=False)
    # 添加当前日期的库存数据到总库存数据中
    # all_inventory_data = all_inventory_data.append(df, ignore_index=True)

    # 更新当前日期
    # current_date = next_date

# 将结果保存到Excel文件
# all_inventory_data.to_excel("inventory_summary.xlsx", index=False)

