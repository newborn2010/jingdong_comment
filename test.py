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
    for i in range(total_pages):
        url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv8571&productId=' + str(itemId) + '&score=0&sortType=5&page=' + str(i) + '&pageSize=10&isShadowSku=0&fold=1'
        myweb = rq.get(url)
        ifo = re.findall('{\"id\":(.*?),\"afterDays\":(.*?)}', myweb.text)
        afterdays.append(ifo[1])
        for mess in ifo:
            comment_time_name = re.findall('\"topped\":(.*?)\,\"referenceName\"', mess[0])
            item_name = re.findall('\"referenceName\":(\".*?\")\,\"referenceTime\"', mess[0])
            score = re.findall('\"referenceType\":\"Product\"(.*?)\,\"status\"', mess[0])
            for mes in comment_time_name:
                comment = re.findall('\"content\":(\".*?\")\,\"creationTime\"', mes)
                co_time = re.findall('\"creationTime\":(\".*?\")\,\"', mes)
                comments.append(comment[0][1:-1])
                times.append(co_time[0][1:-1])
            for num in range(len(score)):
                names.append(item_name[num][1:-1])
                scores.append(score[num][-1])
                pages.append(i)
        
