#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 17:23:11 2018

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
brands = ['del']#, 'huawei', 'iphone']
for brand in brands:
    # connect mysql
    db_info = {'user': 'root',
               'password': '',
               'host': 'localhost',
               'database': brand}
    engine = create_engine('mysql+pymysql://%(user)s:%(password)s@%(host)s/%(database)s?charset=utf8' % db_info,encoding='utf-8')  
    con = sql.connect(host='localhost', user='root', passwd='', db=brand, charset='utf8')
    find_name = 'select table_name from information_schema.tables where table_schema=\'' + brand + '\' and table_type=\'base table\';'
    table_names = list(pd.read_sql(find_name, con)['table_name'])
    for name in table_names:
        rid = []
        ifo = 'select * from ' + name
        data = pd.read_sql(ifo, con)
        ori = len(data)
        for i in range(ori):
            if i != ori-1:
                if str(data[i:i+1]['comments'].values[0]) == str(data[i+1:i+2]['comments'].values[0]):
                    rid.append(i+1)
        data = data.drop(rid)
        data.to_sql(name, engine, if_exists='replace', index=False)  
    con.close() 
end = time.time()
print('Total {0:.3f} min !'.format((end-begin)/60))  
  
