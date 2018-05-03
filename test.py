#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 09:57:34 2018

@author: Rorschach
@mail: 188581221@qq.com
"""
import warnings
warnings.filterwarnings('ignore')

import re
import requests as rq

item_id = [7333897]
for itemId in item_id:
    total_pages = 1
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
        url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv8571&productId=' + str(itemId) + '&score=0&sortType=5&page=' + str(i) + '&pageSize=10&isShadowSku=0&fold=1'
        myweb = rq.get(url)
        ifo = re.findall('{\"id\":(.*?),\"afterDays\":(.*?)}', myweb.text)
        afterdays.append(ifo[1])
        for mess in ifo:
            comment_time_name = re.findall('\"topped\":(.*?)\,\"referenceName\"', mess[0])
            item_name = re.findall('\"referenceName\":(\".*?\")\,\"referenceTime\"', mess[0])
            score = re.findall('\"referenceType\":\"Product\"(.*?)\,\"status\"', mess[0])
            day = re.findall('\"days\":(.*?)', mess[0])
            good_bad = re.findall('\"usefulVoteCount\":(.*?),\"uselessVoteCount\":(.*?),\"useImage', mess[0])
            good = good_bad[0]
            bad = good_bad[1]
            exp = re.findall('\"userExpValue\":(.*?),\"productSales', mess[0])
            level_aftercomment = re.findall('anonymousFlag\":(.*?),\"userLevelName\":(.*?),\"plusAvailable\"', mess[0])[1]
            aftercomment = re.findall('\"content\":(\".*?\"),\"discuss', level_aftercomment)
            level = level_aftercomment.rstrip(',\"afterUserComment\":' + re.findall('\"afterUserComment\":(.*?)', level_aftercomment))[1:-1]
            pic = re.findall('\"images\":(.*?),\"showOrderComment', mess[0]).count('imgUrl')
            days.append(day)
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
                pages.append(i)
        
