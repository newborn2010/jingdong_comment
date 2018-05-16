#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 21:06:22 2018

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
import datetime

# import last time
with open('/Users/zt/Desktop/time.txt','r') as lt:
    last_time = lt.read()

# time
end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
with open('/Users/zt/Desktop/time.txt','w') as nt:
    nt.write(end_time)
    
# get id
brands = ['xiaomi', 'huawei', 'iphone', 'samsung', 'honor']
urls = {'xiaomi': ['https://mi.jd.com/view_search-442829-1000004123-1000004123-0-2-0-0-1-', '-60.html?keyword=%25E6%2589%258B%25E6%259C%25BA&isGlobalSearch=0&other=&isRedisstore=0'],
        'huawei': ['https://huawei.jd.com/view_search-466323-1000004259-1000004259-0-2-0-0-1-', '-60.html?keyword=%25E6%2589%258B%25E6%259C%25BA&isGlobalSearch=0&other=&isRedisstore=0'],
        'iphone': ['https://mall.jd.com/advance_search-394872-1000000127-1000000127-2-0-0-1-', '-60.html?keyword=%25E6%2589%258B%25E6%259C%25BA&other=&isRedisstore=0'],
        'samsung': ['https://samsung.jd.com/view_search-418163-1000003443-1000003443-0-2-0-0-1-', '-60.html?isGlobalSearch=0&other=&isRedisstore=0'],
        'honor': ['https://honor.jd.com/view_search-394032-1000000904-1000000904-0-2-0-0-1-', '-60.html?keyword=%25E6%2589%258B%25E6%259C%25BA&isGlobalSearch=0&other=&isRedisstore=0']}
begin = time.time()
updates = []
for brand in brands:
    all_id = []
    pages = range(1,6)
    for page in pages:
        url = urls[brand][0] + str(page) + urls[brand][1]
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
    con = sql.connect(host='localhost', user='root',passwd='',db=brand,charset='utf8')

    # begin
    number = 1
    update = 0
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
                level_aftercomment = re.findall('userImgFlag\":(.*?),\"userLevelName\":(.*?),\"plusAvailable\"', mess[0])[0][1]
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
                print('get No. {0} in item {1} total {2} brand {3}'.format(count, number, length, brand))
        
        # select
        if len(times) != 0:
            for i in range(len(times)):
                if times[i] < last_time:
                    cut = i
                    break
            comments = comments[:cut]
            times = times[:cut]
            names = names[:cut]
            scores = scores[:cut]
            pages = pages[:cut]
            days = days[:cut]
            afterdays = afterdays[:cut]
            goods = goods[:cut]
            bads = bads[:cut]
            exps = exps[:cut]
            aftercomments = aftercomments[:cut]
            levels = levels[:cut]
            pic_num = pic_num[:cut]
            update += len(times)
            number += 1
                
            # mysql
            cursor = con.cursor()
            item_table = 'create table if not exists table' + str(itemId) + '( name varchar(1000),item int, page int, time datetime,score int,day int,after_day int,good int, bad int,exp int,pic int, level varchar(30),comments varchar(10000000),after_comments varchar(10000000))' 
            cursor.execute(item_table)
            cursor.close()
            for i in range(len(comments)):
                cursor = con.cursor()
                query = ('insert into table' + str(itemId) + '(name, item, page, time, score, day, after_day, good, bad, exp, pic, level, comments, after_comments) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
                cursor.execute(query, (names[i], itemId, pages[i], times[i], scores[i], days[i], afterdays[i], goods[i], bads[i], exps[i], pic_num[i], levels[i], comments[i], aftercomments[i]))
                con.commit()
                cursor.close()         
    con.close()
    updates.append(update)
    time.sleep(300)
end = time.time()
print('Total {0:.1f} min , xiaomi update {1} huawei update {2} iphone update {3} sumsang update {4} honor update {5}!'.format((end-begin)/60, updates[0], updates[1], updates[2], updates[3], updates[4]))
with open('/Users/zt/Desktop/update.txt', 'a') as ud:
    ud.writelines(str(updates) + '\n')
    


    
