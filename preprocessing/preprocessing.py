#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 09:57:23 2018

@author: Rorschach
@mail: 188581221@qq.com
"""
import warnings
warnings.filterwarnings('ignore')

import pymysql as sql
import pandas as pd
from sqlalchemy import create_engine
import time 
from sklearn.feature_extraction.text import TfidfVectorizer

begin = time.time()
brands = ['jd'] #['xiaomi', 'huawei', 'iphone', 'samsung', 'honor']
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
    for name in [table_names[0], ]:
        ifo = 'select * from ' + name
        # 删除默认好评
        default_comment = 'delete from ' + name + ' where comments like \'%此用户未填写%\' and after_comments = \'\';'
        # 删除换行符
        enter = 'update ' + name + ' set comments = replace(comments,\'\\n\',\',\') where comments like \'%\\\\n%\';'
        # 删除空格
        space = 'update ' + name + ' set comments = replace(comments,\' \',\'\') where comments like \'% %\';'
        cursor = con.cursor()
        cursor.execute(default_comment)
        con.commit()
        cursor.close()
        data = pd.read_sql(ifo, con)
        
        comment = []
        with open('/Users/zt/Desktop/test_cut.txt', 'r') as i:
            for line in i.readlines():
                comment.append(line.rstrip("\n"))
        comment = comment[1:]
        
        stop_word = []
        with open('/Users/zt/Desktop/project/stop_words/stop_test.txt', 'r') as stop:
            for line in stop.readlines():
                stop_word.append(line.rstrip("\n"))
        tfidf = TfidfVectorizer(stop_words=stop_word)
        result = tfidf.fit_transform(comment)
        word = tfidf.get_feature_names()
        weight = result.toarray()
        for i in range(len(weight)):
            for j in range(len(word)):
                print(word[j], weight[i][j])
        
        
        
end = time.time()
print('Time: {0:.3f} min !'.format((end - begin)/60))
        
        
        
        























