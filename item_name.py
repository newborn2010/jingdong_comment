#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 22:32:25 2018

@author: Rorschach
@e_mail: 13456019833@163.com
@I hope you find your peace.
"""

import pymysql as sql
import pandas as pd
from sqlalchemy import create_engine

brands = ['iphone_new'] #['xiaomi', 'huawei', 'iphone', 'samsung', 'honor']
for brand in brands:
    count = 0
    all_names = []
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
        count += 1
        print(count)
        con = sql.connect(host='localhost', user='root', passwd='', db=brand, charset='utf8')
        ifo = 'select name from ' + name
        item = list(set(list(pd.read_sql(ifo, con)['name'])))
        all_names.append(item)
        con.close()





















