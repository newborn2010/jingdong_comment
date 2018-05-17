#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 16 17:15:44 2018

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
        con = sql.connect(host='localhost', user='root', passwd='', db=brand, charset='utf8')
        temp = 'create table temp as select name, item, page, time, score, day, after_day, good, bad, exp, pic, level, comments, after_comments from ' + name
        drop = 'drop table ' + name
        rename = 'rename table temp to ' + name
        cursor = con.cursor()
        cursor.execute(temp)
        cursor.execute(drop)
        cursor.execute(rename)
        con.commit()
end = time.time()
print('Total {0:.3f} min !'.format((end-begin)/60))  

  