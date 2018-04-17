#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 21:28:33 2018

@author: Rorschach
@mail: 188581221@qq.com
"""
import warnings
warnings.filterwarnings('ignore')
from selenium import webdriver
import re
import requests as rq
import time
import pymysql as sql

begin = time.time()
all_id = []
pages = range(1,6)
for page in pages:
    url = 'https://mideash.jd.com/view_search-402471-1000001281-1000001281-0-2-0-0-1-'+ str(page) + '-60.html?isGlobalSearch=0&other='
    browser = webdriver.Chrome()
    browser.get(url)
    html = browser.page_source
    browser.close()
    ifo = re.findall('item.jd.com\/(.*?).html', html)
    for i in ifo:
        all_id.append(int(i))

item_id = list(set(all_id))

# check
# =============================================================================
# count = 0
# browser = webdriver.Chrome()
# for a in id:
#     url = 'https://item.jd.com/' + str(a) + '.html'
#     browser.get(url)
#     count += 1
#     browser.execute_script('window.open()')
#     browser.switch_to_window(browser.window_handles[count])
# =============================================================================

# connect mysql
con = sql.connect(host='localhost', user='root',passwd='',db='jingdong',charset='utf8')

# begin
for itemId in item_id:
    total_pages = 1000
    count = 0
    comments = []
    times = []
    names = []
    for i in range(total_pages):
        page = str(i+1)
        url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv8571&productId=' + str(itemId) + '&score=0&sortType=6&page=' + str(i) + '&pageSize=10&isShadowSku=0&fold=1'
        myweb = rq.get(url)
        comment_time_name = re.findall('\"guid\":(\".*?\")\,\"referenceName\"', myweb.text)
        item_name = re.findall('\"referenceName\":(\".*?\")\,\"referenceTime\"', myweb.text)
        for mes in comment_time_name:
            comment = re.findall('\"content\":(\".*?\")\,\"creationTime\"', mes)
            co_time = re.findall('\"creationTime\":(\".*?\")\,\"', mes)
            for num in range(len(comment)):
                comments.append(comment[num][1:-1])
                times.append(co_time[num][1:-1])
                names.append(item_name[num][1:-1])
                count += 1
                print('get No. {}'.format(count))
    # mysql
    cursor = con.cursor()
    item_table = 'create table table' + str(itemId) + '(id int not null auto_increment primary key, name varchar(1000),time datetime,comments varchar(10000000))' 
    cursor.execute(item_table)
    cursor.close()
    for i in range(len(comments)):
        cursor = con.cursor()
        query = ('insert into table' + str(itemId) + '(name, time, comments) values (%s, %s, %s)')
        cursor.execute(query, (names[i], times[i], comments[i]))
        con.commit()
        cursor.close()
# =============================================================================
#     cursor = con.cursor()
#     delete ='delete from table' + str(itemId) + ' where comments in (select comments from table' + str(itemId) + ' group by comments having count(comments)>1) and comments not in (select min(time) from table' + str(itemId) + 'group by comments having count(comments)>1)' 
#     cursor.execute(delete)
#     cursor.close()
# =============================================================================
con.close()
end = time.time()
print('Total {0:.1f} min !'.format((end-begin)/60))
