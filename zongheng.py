import requests
import re
import os
from lxml import etree

path='E:\\纵横小说\\'
url='http://book.zongheng.com/store/c1/c0/b0/u0/p1/v0/s9/t0/u0/i1/ALL.html'
headers={
    'Host':'book.zongheng.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
}

def got_page(url,headers):
    response=requests.get(url=url,headers=headers)
    html=etree.HTML(response.text)
    return html

response=requests.get(url,headers=headers)
html=got_page(url,headers)

books_name=html.xpath('//div[@class="bookname"]/a/text()')
books_url=html.xpath('//div[@class="bookname"]/a/@href')

for book_name in books_name:
# 生成小说名字的文件夹
    book_name=str(book_name)
    directory = path + book_name
    if not os.path.exists(directory):
        os.makedirs(directory)

for book_url in books_url:
    book_url=str(book_url)
    hh=re.search(r'(\d+)\.html',book_url).group()
    directory_book_url='http://book.zongheng.com/showchapter/'+hh#小说章节目录网址

    html_book=got_page(directory_book_url,headers)
    urls_chapter = str(html_book.xpath('//li[@class=" col-4"]/a/@href')).strip('[]').split(',')

    for url_chapter in urls_chapter:
        url_chapter = eval(url_chapter)
        print(urls_chapter)
        response_chapter = requests.get(url=url_chapter, headers=headers)
        result_chapter = response_chapter.text

        html_chapter = etree.HTML(result_chapter)
        title = eval(str(html_chapter.xpath('//div[@class="title_txtbox"]/text()')).strip('[]'))
        pp = eval(str(html_chapter.xpath('//div[@class="content"]/p/text()')).strip('[]'))
        full_path = directory+'\\'+ str(title) + '.txt'

        with open(full_path, 'w', encoding='utf-8') as file:
            file.write(str(pp))
            file.close()
