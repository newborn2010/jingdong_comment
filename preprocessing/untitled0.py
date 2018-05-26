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
    all_records = 0
    rid_number = []
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
    for name in table_names:
        ifo = 'select * from ' + name
        con = sql.connect(host='localhost', user='root', passwd='', db=brand, charset='utf8')
        data = pd.read_sql(ifo, con)
        con.close()
        data = data.sort_values(by=['time'], ascending=False)
        length = len(data)
        delete = []
        count = 0
        for i in range(3):                      #range(length - 99):
            if i+100 <= len(data):
                dirty = data[i:i+100]
                data = data.drop(list(range(i, i+100)))
                clear = dirty.drop_duplicates(subset=['comments'], keep='last')
                data = data.append(clear, ignore_index=True)
                data = data.sort_values(by=['time'], ascending=False)
                delete.append(100 - len(clear))
                count +=1
        pd.io.sql.to_sql(data, name, engine, if_exists='replace', index=False) 
        print(delete, count)
end = time.time()
print('Time: {0:.3f} min !'.format((end - begin)/60))
        
        
        
        
        
        
        
        