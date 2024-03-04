"""  作者：愤怒的it男
链接：https://www.zhihu.com/question/40680662/answer/3391121667
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。"""



from lxml import etree
import csv
from prettytable import PrettyTable
from playwright.sync_api import sync_playwright

def getData():
    with sync_playwright() as p:
        browser_type = p.chromium
        browser = browser_type.launch()
        page = browser.new_page(ignore_https_errors=True)
        page.goto('https://data.stats.gov.cn/easyquery.htm')
        page.get_by_text("交通运输").click()
        page.get_by_text("旅客运输量").click()
        page.locator("//div[@class='dtHead']").click()
        page.get_by_text("最近36个月").click()
        html = etree.HTML(page.content())
        thead = html.xpath("//table[@class='public_table table_column']/thead/tr/th/strong/text()")
        tbody = []
        trs = html.xpath("//table[@class='public_table table_column']/tbody/tr")
        for tr in trs:
            row = []
            index1 = tr.xpath("td[1]/a/following::text()[1]")[0]
            index2 = tr.xpath("td[1]/a/following::text()[2]")[0]
            index = str(index1) + '|' + str(index2)
            row.append(index)
            row = row + tr.xpath("td[@align='right']/text()")
            tbody.append(row)
        browser.close()
    return (thead, tbody)

def printData(thead, tbody):
    table = PrettyTable()
    table.add_column("时间",thead[1:])
    for index,row in enumerate(tbody):
        if index in [0,4,8,12,16]:
            table.add_column(row[0],row[1:])
    print(table)

    #table.add_column("时间",thead[1:])

def saveData(thead, tbody):
    with open('旅客运输量.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(thead)
        writer.writerows(tbody)

def main():
    print('数据采集中，请耐心等待……')
    result = getData()
    printData(result[0], result[1])
    saveData(result[0], result[1])

if __name__== "__main__" :
    main()