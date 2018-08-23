#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 22:43:14 2018

@author: Rorschach
@e_mail: 13456019833@163.com
@I hope you find your peace.
"""

import pymysql as sql
import pandas as pd
from sqlalchemy import create_engine
import time 
import lda
from collections import defaultdict
import os

p_path = '/Users/zhengtian/Desktop/sentiment dict/p/'
n_path = '/Users/zhengtian/Desktop/sentiment dict/n/'
p_dir = os.listdir(p_path)
n_dir = os.listdir(n_path)
p_dir.remove('.DS_Store')
n_dir.remove('.DS_Store')

for i in p_dir:
    with open(p_path + i, 'r') as inp:
        a = inp.read()
p_word

begin = time.time()
brands = ['samsung_new']#['xiaomi_new', 'huawei_new', 'iphone_new', 'samsung_new', 'honor_new']#['xiaomi', 'huawei', 'iphone', 'samsung', 'honor']
for brand in brands:
    # connect mysql
    db_info = {'user': 'root',
               'password': '',
               'host': 'localhost',
               'database': brand}
    engine = create_engine('mysql+pymysql://%(user)s:@%(host)s/%(database)s?charset=utf8' % db_info,encoding='utf-8')  
    con = sql.connect(host='localhost', user='root', passwd='', db=brand, charset='utf8')
    find_name = 'select table_name from information_schema.tables where table_schema=\'' + brand + '\' and table_type=\'base table\';'
    table_names = list(pd.read_sql(find_name, con)['table_name'])
    con.close()
    cc = 0
    for name in [table_names[0]]: # \
        cc += 1
        print('Now : table {0} in {1} total {2}'.format(cc, brand, len(table_names)))
        ifo = 'select * from ' + name
        con = sql.connect(host='localhost', user='root', passwd='', db=brand, charset='utf8')
        data = pd.read_sql(ifo, con)
        comments = list(data['comments'])
        for comment in [comments[0]]: # \
            zhuti = []
            biaodian = []
            co_split = lda.split_sentence(comment)  # 得到一个分句后的评论
            for i in co_split:
                for j in range(len(i)):
                    if i[j] in '，。！？!?,.;；、':
                        break
                # 划分分句后的句子为主体和标点
                words = i[:j]
                doc = i[j:]
                # 先处理标点
                doc.replace('？！', '！！').replace('?!', '!!')
                doc_score = defaultdict(int)
                for t in doc:
                    doc_score[t] += 1
                k = 1.3**(doc_score['！'] + doc_score['!']) * 0.8**(doc_score['?'] + doc_score['？'])
                # 处理主体
                s_word = lda.word_split(words)
                
                zhuti.append(s_word)
                biaodian.append(doc)
                
                
                
                
        
































