#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 23:39:12 2018

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
    url = 'https://mall.jd.com/advance_search-394872-1000000127-1000000127-2-0-0-1-' + str(page) + '-60.html?keyword=%25E6%2589%258B%25E6%259C%25BA&other=&isRedisstore=0'
    browser = webdriver.Chrome()
    browser.get(url)
    html = browser.page_source
    browser.close()
    ifo = re.findall('item.jd.com\/(.*?).html', html)
    for i in ifo:
        if i.isdigit():
            all_id.append(int(i))

item_id = list(set(all_id))
length = len(item_id)

# connect mysql
con = sql.connect(host='localhost', user='root',passwd='',db='iphone',charset='utf8')

# begin
number = 1
for itemId in item_id:
    total_pages = 200
    count = 0
    comments = []
    times = []
    names = []
    scores = []
    pages = []
    days = []
    afterdays = []
    goods = []
    bads = []
    exps = [] 
    aftercomments = []
    levels = [] 
    pic_num = [] 
    for i in range(total_pages):
        url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv8571&productId=' + str(itemId) + '&score=0&sortType=6&page=' + str(i) + '&pageSize=10&isShadowSku=0&fold=1'
        myweb = rq.get(url)
        comment_time_name = re.findall('\"topped\":(.*?)\,\"referenceName\"', myweb.text)
        item_name = re.findall('\"referenceName\":(\".*?\")\,\"referenceTime\"', myweb.text)
        score = re.findall('\"referenceType\":\"Product\"(.*?)\,\"status\"', myweb.text)
        ifo = re.findall('{\"id\":(.*?),\"afterDays\":(.*?)}', myweb.text)
        afterday = re.findall('\"afterDays\":(.*?)}',myweb.text)
        day = re.findall('\"days\":(.*?),\"afterDays\"', myweb.text)
        for mess in ifo:
            good_bad = re.findall('\"usefulVoteCount\":(.*?),\"uselessVoteCount\":(.*?),\"userImage', mess[0])
            good = good_bad[0][0]
            bad = good_bad[0][1]
            if re.findall('\"anonymousFlag\":(.*?),\"userExpValue\":(.*?),\"productSales', mess[0]) == []:
                exp = '0'
            else:
                exp = re.findall('\"anonymousFlag\":(.*?),\"userExpValue\":(.*?),\"productSales', mess[0])[0][1]
            level_aftercomment = re.findall('anonymousFlag\":(.*?),\"userLevelName\":(.*?),\"plusAvailable\"', mess[0])[0][1]
            aftercomment = ''.join(re.findall('\"content\":\"(.*?)\",\"discuss', level_aftercomment))
            level = level_aftercomment[1:level_aftercomment.find('\"',1)]
            pic = ''.join(re.findall('\"images\":(.*?),\"showOrderComment', mess[0])).count('jShow') + ''.join(re.findall('\"afterImages\":(.*?)]', mess[0])).count('jShow')
            goods.append(good)
            bads.append(bad)
            exps.append(exp)
            aftercomments.append(aftercomment)
            levels.append(level)      
            pic_num.append(str(pic))
        for mes in comment_time_name:
            comment = re.findall('\"content\":(\".*?\")\,\"creationTime\"', mes)
            co_time = re.findall('\"creationTime\":(\".*?\")\,\"', mes)
            comments.append(comment[0][1:-1])
            times.append(co_time[0][1:-1])
        for num in range(len(score)):
            names.append(item_name[num][1:-1])
            scores.append(score[num][-1])
            afterdays.append(afterday[num])
            days.append(day[num])
            pages.append(i)
            count += 1
            print('get No. {0} in item {1} total {2}'.format(count, number, length))
    number += 1
    # mysql
    cursor = con.cursor()
    item_table = 'create table table' + str(itemId) + '(id int not null auto_increment primary key, name varchar(1000),item int, page int, time datetime,score int,day int,after_day int,good int, bad int,exp int,pic int, level varchar(30),comments varchar(10000000),after_comments varchar(10000000))' 
    cursor.execute(item_table)
    cursor.close()
    for i in range(len(comments)):
        cursor = con.cursor()
        query = ('insert into table' + str(itemId) + '(name, item, page, time, score, day, after_day, good, bad, exp, pic, level, comments, after_comments) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
        cursor.execute(query, (names[i], itemId, pages[i], times[i], scores[i], days[i], afterdays[i], goods[i], bads[i], exps[i], pic_num[i], levels[i], comments[i], aftercomments[i]))
        con.commit()
        cursor.close()
con.close()
end = time.time()
print('Total {0:.1f} min !'.format((end-begin)/60))


