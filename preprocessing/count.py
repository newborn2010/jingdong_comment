#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 12 15:25:18 2018

@author: Rorschach
@mail: 188581221@qq.com
"""
import warnings
warnings.filterwarnings('ignore')

import pymysql as sql
import pandas as pd
import time 

begin = time.time()
brands = ['xiaomi_new', 'huawei_new', 'iphone_new', 'samsung_new', 'honor_new'] #['xiaomi', 'huawei', 'iphone', 'samsung', 'honor']
al = 0
for brand in brands:
    all_records = 0
    rid_number = []
    # connect mysql
    con = sql.connect(host='localhost', user='root', passwd='', db=brand, charset='utf8')
    find_name = 'select table_name from information_schema.tables where table_schema=\'' + brand + '\' and table_type=\'base table\';'
    table_names = list(pd.read_sql(find_name, con)['table_name'])
    con.close() 
    for name in table_names:
        ifo = 'select * from ' + name
        con = sql.connect(host='localhost', user='root', passwd='', db=brand, charset='utf8')
        data = pd.read_sql(ifo, con)
        con.close() 
        ori = len(data)
        all_records += len(data)
    al += all_records
    print('we have {0} of {1} in {2}'.format(all_records, len(table_names), brand))
end = time.time()
print('Total {0} in {1:.3f} min !'.format(al, (end-begin)/60))  

  
