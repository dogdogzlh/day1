# -*- codeing = utf-8 -*-
# @Time : 2021/1/26 12:43
# @Author:  Enchanted
# @File : demo1.py
# @Software: PyCharm

# print("hehe")
# '''
# 多行注释
# '''
# print("www", "baidu", "com", sep=".")

import random
import re
import urllib.request,urllib.error,urllib.parse
import xlwt
import sqlite3
import bs4

findLink = re.compile(r'<a href="(.*?)">')

findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)

findTitle =re.compile(r'<span class="title">(.*)</span>')

findRating =re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>',re.S)

findJudge = re.compile(r'<span>(\d*)人评价</span>')
#找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
#找到影片的相关内容
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)

def main():
    baseurl = "https://movie.douban.com/top250?start="
    datalist=getData(baseurl)
    savepath="豆瓣电影TOP250.xls"
    saveData(datalist,savepath)

def getData(baseurl):
    datalist = []
    for i in range(0, 10):  # 调用获取页面信息的函数，10次
        url = baseurl + str(i * 25)
        html = askURL(url)  # 保存获取到的网页源码

        # 2.逐一解析数据
        soup = bs4.BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):  # 查找符合要求的字符串，形成列表
            # print(item)   #测试：查看电影item全部信息
            data = []  # 保存一部电影的所有信息
            item = str(item)

            # 影片详情的链接
            link = re.findall(findLink, item)[0]  # re库用来通过正则表达式查找指定的字符串
            data.append(link)  # 添加链接

            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)  # 添加图片

            titles = re.findall(findTitle, item)  # 片名可能只有一个中文名，没有外国名
            if (len(titles) == 2):
                ctitle = titles[0]  # 添加中文名
                data.append(ctitle)
                otitle = titles[1].replace("/", "")  # 去掉无关的符号

                data.append(otitle)  # 添加外国名
            else:
                data.append(titles[0])
                data.append(' ')  # 外国名字留空

            rating = re.findall(findRating, item)[0]
            data.append(rating)  # 添加评分

            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)  # 提加评价人数

            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")  # 去掉句号
                data.append(inq)  # 添加概述
            else:
                data.append(" ")  # 留空

            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)  # 去掉<br/>
            bd = re.sub('/', " ", bd)  # 替换/
            data.append(bd.strip())  # 去掉前后的空格


            datalist.append(data)  # 把处理好的一部电影信息放入datalist

    return datalist

def askURL(url):
    header = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"

    }
    req = urllib.request.Request(url=url,headers=header)
    response = urllib.request.urlopen(req)
    html = ""
    try:
        response = urllib.request.urlopen(req)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html

def saveData(datalist,savepath):
    print("存到Excel")
    book=xlwt.Workbook(encoding="utf-8",style_compression=0)
    sheet = book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)
    col = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价数", "简介", "相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i])  # 列名
    for i in range(0, 250):
        print("第%d条" % (i + 1))
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])  # 数据

    book.save(savepath)  # 保存


if __name__ == "__main__":          #当程序执行时
#调用函数
    main()
    #init_db("movietest.db")
    print("爬取完毕！")