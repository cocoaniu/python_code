# coding = utf-8

# python version 3.6

from datetime import datetime
import requests
from bs4 import BeautifulSoup
import os
import time


# 确定需要爬取的链接

# 输入一个日期，爬取这一天到今天所有的斗图表情
# 有个地方写得糙，只会爬到第一个没有这个日期的页码，所以可能爬到几条这个日期之前的日期
endDate = datetime.strptime(input('输入YYYY-mm-dd格式的截止日期：'), '%Y-%m-%d')

# 模拟浏览器UA
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'}

pageNo = 1
response = requests.get(
    'http://www.doutula.com/article/list/?page=1', headers=headers)
bsObj = BeautifulSoup(response.text, 'lxml')
# 所有待爬取的主题url
global urlSet
urlSet = set()
# 初始化创建时间集合，用于保存每一页所有主题的创建时间，判断是否小于输入的截止日期
cDateList = []

# 只要一个页面中的所有主题的创建时间都大于等于设置的截止日期，循环就继续
while all(cDateList) and len(bsObj.find_all('a', class_='list-group-item')) > 0:
    # 在本页的所有主题链接中
    for url in bsObj.find_all('a', class_='list-group-item'):
        # 如果有href属性
        if 'href' in url.attrs:
            # 把这个url加入到待爬取的主题url集合中
            urlSet.add(url.attrs['href'])
    cDateList = []
# 把专题的添加时间收集到集合中
    for cdate in bsObj.find_all('small'):
        cDateList.append(datetime.strptime(cdate.text, '%Y-%m-%d') >= endDate)
# 采集完一个页面中的链接后，页码加1，继续循环采集
    pageNo = pageNo + 1
    response = requests.get(
        'http://www.doutula.com/article/list/?page=' + str(pageNo), headers=headers)
    bsObj = BeautifulSoup(response.text, 'lxml')
#   time.sleep(1)


# 读取已下载过的链接


# 初始化已下载列表
doneList = []

# 如果本地有已下载链接记录文件
if os.path.isfile(r'./doneSet'):
    with open('doneSet', 'r') as f:
        for line in f.read().splitlines():
            # 把文件中的内容读入到doneList
            doneList.append(line)
    f.close()

# 将doneList转化为集合
doneSet = set(doneList)
# 将全部待下载链接与已下载链接取差集
urlSet = urlSet - doneSet

print(len(urlSet))
# 下载链接里的文件

for link in urlSet:
    print(link)
    response = requests.get(link, headers=headers)
    bsObj = BeautifulSoup(response.text, 'lxml')
# 取主题名称
    if len(bsObj.h3.a.text) > 0:
        dirName = bsObj.h3.a.text.replace('/','')
    else:
        dirName = link.split('/')[-1] + '-noname'
# 以主题名称创建文件夹
    if os.path.isdir(dirName):
        pass
    else:
        os.mkdir(dirName)
# 转到文件夹
    os.chdir(dirName)
# 查找图片所在td
    for l1 in bsObj('td'):
        # 查找图片所在的img标签
        for l2 in l1('img'):

# 如果src地址可用就用src的地址，如果不可用就用onerror的地址，都不可用就跳过
            if  len(l2.attrs['src']) > 20 and requests.get(l2.attrs['src']).status_code == 200:
                downUrl = l2.attrs['src']
            elif len(l2.attrs['onerror'].split("'")[-2]) > 20 and requests.get(l2.attrs['onerror'].split("'")[-2]).status_code == 200 :
                downUrl = l2.attrs['onerror'].split("'")[-2]
            else:
                continue
# 如果这张图丢了，显示为网站的默认替代图片，就不下载
            if downUrl == 'http://img7.doutula.com/production/uploads/image/':
                continue

# 创建文件，文件名称为alt属性（描述图片）+'.'+文件链接地址以点分割后的最后一组，即扩展名
# 如果有alt属性且长度不为0就用alt为文件名，否则以链接地址为文件名
            if 'alt' in l2.attrs:
                if len(l2.attrs['alt']) == 0:
                    with open('noname-' + downUrl.split('/')[-1], 'wb') as f:
                        f.write(requests.get(downUrl).content)
                    f.close
                else:
                    with open(l2.attrs['alt'].replace('/','') + '.' + downUrl.split('.')[-1], 'wb') as f:
                        f.write(requests.get(downUrl).content)
                    f.close
            else:
                with open('noname-' + downUrl.split('/')[-1], 'wb') as f:
                    f.write(requests.get(downUrl).content)
                f.close

#            time.sleep(0.5)

    os.chdir('..')
    with open('doneSet', 'a') as f:
        f.writelines(link + '\n')
    f.close


# print(urlSet)
# print(len(urlSet))

# print(cDateList)
# print(pageNo)
