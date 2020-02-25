import requests
from lxml import etree
import os
import re
from hashlib import md5

def got_page(url,headers):
    response=requests.get(url=url,headers=headers)
    html=etree.HTML(response.text)
    return html

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
}
s=input('请输入你要查找的书名：')

url='http://search.zongheng.com/s?keyword='+s
html=got_page(url,headers)
bookNu=str(html.xpath('//div[@class="search-tips"]/text()')).strip('[]')
hh=re.search(r'(\d+)',bookNu).group()
bookDu=[]
if int(hh)==0:
    print('没有您要查找的书籍')
else:
    urls=str(html.xpath('//div[@class="imgbox fl se-result-book"]/a/@href')).strip('[]').split(',')
    for url_Intdu in urls:
        url_Intdu=eval(url_Intdu)#书简介地址 用来提取书名和作者以及书的简介

        bookDue={}

        htmlIntroduction=got_page(url_Intdu,headers)

        bookName=str(htmlIntroduction.xpath('//div[@class="book-name"]/text()'))#书名
        bookName=re.findall('[\u4e00-\u9fa5]+',bookName)
        bookDue['书名']=bookName

        authorName=str(htmlIntroduction.xpath('//div[@class="au-name"]/a/text()'))#作者名字
        authorName=re.findall('[\u4e00-\u9fa5]+',authorName)
        bookDue['作者']=authorName

        book_Indu=str(htmlIntroduction.xpath('string(//div[@class="book-info"]/div[contains(@class,Jbook-dec)]/p)'))
        bookDue['简介']=book_Indu

        Num=re.search(r'(\d+)\.html',url_Intdu).group()
        bookDue['url_num']=Num
        bookDu.append(bookDue)
    for i in range(len(bookDu)):
        print(i+1)
        print('书名:%s' %(bookDu[i]['书名'][0]))
        print('作者:%s' %bookDu[i]['作者'][0])
        print('简介:%s' %bookDu[i]['简介'])

    got_book=int(input('请输入你要下载的书编号:'))
    while got_book > len(bookDu)+1 or got_book < 1:
        print('输入有误请重新输入')
        got_book =int(input('请输入你要下载的书编号:'))
    else:
        num=bookDu[got_book-1]['url_num']
        directory_book_url = 'http://book.zongheng.com/showchapter/' +num #这个是书的目录地址 提取章节
        bbook_name=bookDu[got_book-1]['书名'][0]

        html_book = got_page(directory_book_url, headers)
        urls_chapter = str(html_book.xpath('//li[@class=" col-4"]/a/@href')).strip('[]').split(',')#所有章节url的列表

        path=input('请输入小说存放文件夹路径:')
        t_path=path+'\\'+bbook_name
        if not os.path.exists(t_path):#若文件夹不存在则新建
            os.makedirs(t_path)

        for url_chapter in urls_chapter:
            url_chapter = eval(url_chapter)#各个章节的url

            html_chapter=got_page(url_chapter,headers)
            title = eval(str(html_chapter.xpath('//div[@class="title_txtbox"]/text()')).strip('[]'))#章名称
            content = eval(str(html_chapter.xpath('//div[@class="content"]/p/text()')).strip('[]'))#章内容
            full_path = t_path + '\\' + str(title) + '.txt'
            print(full_path)

            with open(full_path, 'w', encoding='utf-8') as file:
                    file.write(str(content))
