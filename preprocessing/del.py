#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 25 16:15:07 2018

@author: Rorschach
@mail: 188581221@qq.com
"""
import warnings
warnings.filterwarnings('ignore')


import pymysql as sql
import pandas as pd
from sqlalchemy import create_engine
import time 

begin = time.time()
brands = ['jd']#['xiaomi', 'huawei', 'iphone', 'samsung', 'honor']
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
    delete = []
    count = 0
    for name in table_names:
        ifo = 'select * from ' + name
        con = sql.connect(host='localhost', user='root', passwd='', db=brand, charset='utf8')
        ori_length = len(pd.read_sql(ifo, con))
        # 去除 ID
        temp_0 = 'create table temp as select name, item, page, time, score, day, after_day, good, bad, exp, pic, level, comments, after_comments from ' + name
        drop_0 = 'drop table ' + name
        rename_0 = 'rename table temp to ' + name
        # 去除完全重复项
        temp_1 = 'create table temp as select distinct * from ' + name
        drop_1 = 'drop table ' + name
        rename_1 = 'rename table temp to ' + name
        cursor = con.cursor()
        cursor.execute(temp_0)
        cursor.execute(drop_0)
        cursor.execute(rename_0)
        print('Delete id complete !')
        cursor.execute(temp_1)
        cursor.execute(drop_1)
        cursor.execute(rename_1)
        print('Distinct complete !')
        con.commit()
        cursor.close()        
        length = len(pd.read_sql(ifo, con))
        distinct = ori_length - length
        data = pd.read_sql(ifo, con)
        con.close()
        # 以 100 为单位去重
        data = data.sort_values(by=['time'], ascending=False)
        for i in range(len(data) - 99):
            if i+100 <= len(data):
                dirty = data[i:i+100]
                data = data.drop(list(range(i, i+100)))
                clear = dirty.drop_duplicates(subset=['comments'], keep='last')
                data = data.append(clear)
                data = data.sort_values(by=['time'], ascending=False)
                data = data.reset_index(drop=True)
                delete.append(100 - len(clear))
                count +=1
        pd.io.sql.to_sql(data, name, engine, if_exists='replace', index=False) 
    print('We delete: {0} and {1} total {2} in {3}, count: {4}, ori:{5}'.format(sum(delete), distinct, sum(delete)+distinct, brand, count, ori_length))
end = time.time()
print('Time: {0:.3f} min !'.format((end - begin)/60))
        
        
        
        
        
        
        
