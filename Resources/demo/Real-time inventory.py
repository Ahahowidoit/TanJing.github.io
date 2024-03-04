# -*- coding: <encoding name> -*- : # -*- coding: utf-8 -*-

import pyodbc
import pandas as pd
import numpy as np

print(pyodbc.drivers())
# 数据库连接设置
server = '222.221.246.101'
database = 'AIS20210708164946'
username = 'Cloudytx'
password = 'ytxdata'

cnxn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
cursor = cnxn.cursor()


query_base = '''
SELECT
	a.FID,
	b.[仓库一级分组],
	b.[仓库二级分组],
	a.FSTOCKID AS [仓库id],
	b.[仓库编码],
	b.[仓库名称] AS 门店编码,
	b.[使用组织名称] AS 门店名称,
	a.FMATERIALID AS [商品id],
-- 	c.[五级分类全码],
	c.[商品名称],
	c.[条码],
	c.[五级编码],
	c.[代销自营],
	CONVERT ( DECIMAL ( 18, 3 ), a.FBASEQTY, 3 ) AS 库存量,
-- 	CONVERT ( DECIMAL ( 18, 3 ), a.FBASEQTY * d.[成本单价], 3 ) AS 库存额,
-- 	d.[成本单价],
	c.[物料成本单价],
	c.[零售单价],
	c.[礼钰店单价],
	c.[电商单价],
	c.[商圈单价],
	c.[首次采购日期],
		-- 加工入库年份
	CASE WHEN c.[首次采购日期] IS NOT NULL THEN	
			CAST(YEAR(c.[首次采购日期]) AS varchar(4)) ELSE '入库日期不详' 
END AS 入库年份,

	a.FUPDATETIME AS 最后一次入库时间,
	DATEDIFF(d, a.FUPDATETIME, GETDATE()) AS 库龄,
	c.[图片名称] AS [图片id],
	c.[商品属性] AS [商品属性id],
	c.[质检证书],
	c.[种水id],
	c.[种水],
	c.[颜色id],
	c.[颜色],
	c.[重量],
	c.[圈口],
	c.[规格型号],
	c.[拼音码],
	c.[系列号],
	c.[供应商自定码id],
	c.[供应商自定码],
	c.[供应商id],
	c.[供应商编码],
	c.[供应商名称],
	a.FBASEQTY
FROM
	T_STK_INVENTORY AS a
	LEFT JOIN [ZY_仓库表] AS b ON b.[仓库id] = a.FSTOCKID
	LEFT JOIN [ZY_商品表YTX] AS c ON c.[商品id] = a.FMATERIALID 
-- 	LEFT JOIN [ZJ_T_库存成本计算] AS d ON d.[条码] = c.[条码]
WHERE
	a.FBASEQTY <> 0
'''

cursor.execute(query_base)
result_base = cursor.fetchall()

query_base2 = '''
select * from  [ZJ_T_库存成本计算]
'''
cursor.execute(query_base2)
result_base2 = cursor.fetchall()

#   定义列名
columns_inventory = ['FID','仓库一级分组','仓库二级分组','仓库id','仓库编码','门店编码','门店名称','商品id','商品名称','条码','五级编码','代销自营','库存量','物料成本单价','零售单价','礼钰店单价','电商单价','商圈单价','首次采购日期','入库年份','最后一次入库时间','库龄','图片id','商品属性id','质检证书','种水id','种水','颜色id','颜色','重量','圈口','规格型号','拼音码','系列号','供应商自定码id','供应商自定码','供应商id','供应商编码','供应商名称','FBASEQTY']
#   输出为DataFrame
df_inventory = pd.DataFrame.from_records(result_base, columns=columns_inventory)

columns_cost = ['条码','成本单价']
df_cost = pd.DataFrame.from_records(result_base2,columns=columns_cost)

# 右连接关联两张表
df_inventory = pd.merge(df_inventory, df_cost, on=['条码'], how='left')

# 在表格中新增计算字段
df_inventory["库存额"] = df_inventory["FBASEQTY"].apply(float) * df_inventory["成本单价"].apply(float)

# 将原先DataFrame中某列单独取出作为DataFrame
df1 = df_inventory.库存额
df2 = df_inventory.成本单价

# 删除已取出的列
df_inventory = df_inventory.drop("库存额",axis=1)
df_inventory = df_inventory.drop("成本单价",axis=1)

# 将取出的DataFrame作为列插入到指定位置，第一列索引为0
df_inventory.insert(13,"库存额",df1)
df_inventory.insert(14,"成本单价",df1)

# 删除DataFrame中不需要的列
df_inventory = df_inventory.drop("FBASEQTY",axis=1)
pass

# 导出结果到CSV或Excel文件
df_inventory.to_csv('0522.csv', index=False, encoding='utf_8_sig')
# # 导出结果到Excel文件
# df_base.to_excel('output.xlsx', index=False, float_format='%.2f')
#
print("ok")
#
# # 关闭数据库连接
cursor.close()
cnxn.close()












