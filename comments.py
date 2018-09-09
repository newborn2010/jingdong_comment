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
import random

p_path = '/Users/zhengtian/Desktop/sentiment dict/p/'
n_path = '/Users/zhengtian/Desktop/sentiment dict/n/'
cd_path = '/Users/zhengtian/Desktop/sentiment dict/cd/'
fd_path = '/Users/zhengtian/Desktop/sentiment dict/fd/'
p_dir = os.listdir(p_path)
n_dir = os.listdir(n_path)
cd_dir = os.listdir(cd_path)
fd_dir = os.listdir(fd_path)
for i in [p_dir, n_dir, cd_dir, fd_dir]:
    if '.DS_Store' in i:
        i.remove('.DS_Store')


# 正负情感词典
p_words = defaultdict(int)
p_word = []
for i in p_dir:
    with open(p_path + i, 'r', encoding='utf-8') as inp:
        a = inp.readlines()
        for j in a:
            p_word.append(j.replace('\n', '').replace(' ', ''))
p_word = list(set(p_word))   
for i in p_word:
    p_words[i] = 1

n_words = defaultdict(int)
n_word = []
for i in n_dir:
    with open(n_path + i, 'r', encoding='utf-8') as inp:
        a = inp.readlines()
        for j in a:
            n_word.append(j.replace('\n', '').replace(' ', ''))
n_word = list(set(n_word))          
for i in n_word:
    n_words[i] = -1

# 程度词典
cd_words = defaultdict(int)
cd_word = []
for i in cd_dir:
    with open(cd_path + i, 'r', encoding='utf-8') as inp:
        a = inp.readlines()
        for j in a:
            cd_word.append(j.replace('\n', '').replace(' ', ''))
cd_word = list(set(cd_word))   
for i in cd_word:
    cd_words[i] = 2
    
# 反义词典
fd_words = defaultdict(int)
fd_word = []
for i in fd_dir:
    with open(fd_path + i, 'r', encoding='utf-8') as inp:
        a = inp.readlines()
        for j in a:
            fd_word.append(j.replace('\n', '').replace(' ', ''))
fd_word = list(set(fd_word))   
for i in fd_word:
    fd_words[i] = -1

# 计算得分    
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
    comment_score = []
    for name in table_names:
        cc += 1
        ifo = 'select * from ' + name
        con = sql.connect(host='localhost', user='root', passwd='', db=brand, charset='utf8')
        data = pd.read_sql(ifo, con)
        comments = list(data['comments'])
        score = []
        tt = 0
        for comment in comments:
            tt += 1
            print('Now : table {0} in {1} total {2}'.format(cc, brand, len(table_names)))
            print(tt,len(comments))
            scoress = []
            co_split = lda.split_sentence(comment)  # 得到一个分句后的评论
            for i in co_split: 
                for j in range(len(i)):
                    if i[j] in ' ，。！？!?,.;；、':
                        break
                # 划分分句后的句子为主体和标点
                if j != len(i)-1 or i[j] in ' ，。！？!?,.;；、':
                    words = i[:j]
                    doc = i[j:]
                else:
                    words = i
                    doc = ''
                # 先处理标点
                doc = doc.replace('？！', '！！').replace('?!', '!!').replace('？？','！！').replace('??', '!!')
                doc_score = defaultdict(int)
                for t in doc:
                    doc_score[t] += 1
                k = 1.3**(doc_score['！'] + doc_score['!']) * 0.8**(doc_score['?'] + doc_score['？'])
                # 处理主体
                s_word = lda.word_split(words)
                major = [-1]
                cut = []
                scores = []
                for m in range(len(s_word)):
                    if s_word[m] in p_word+n_word:
                        major.append(m)
                        cut.append(s_word[major[-2]+1:major[-1]+1])
                for n in cut:
                    for m in range(len(n)-1):
                        if n[m] in cd_word:
                            n[m] = 2
                        if n[m] in fd_word:
                            n[m] = -1
                    if n[-1] in p_word:
                        n[-1] = 1
                    if n[-1] in n_word:
                        n[-1] = -1
                    s = n[-1]
                    for i in range(len(n)-1):
                        if type(n[i]) == type(1):
                            s = s*n[i]      
                    scores.append(s)
                scoresss = sum(scores) * k
                scoress.append(scoresss)
            score.append(round(sum(scoress),1))
        for t in range(len(score)):
            comment_score.append((comments[t],score[t]))
end = time.time()
print('Total {0:.1f} min!'.format((end-begin)/60))
                
     





#random.sample(comment_score,100)


with open('/Users/zhengtian/Desktop/att.txt', 'a') as f:
    for i in comment_score:
        f.write(i[0] + ',' + str(i[1]) + '\n')


                    
