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
brands = ['drinks']#['xiaomi', 'huawei', 'iphone', 'samsung']
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
        rid = []
        ifo = 'select * from ' + name
        con = sql.connect(host='localhost', user='root', passwd='', db=brand, charset='utf8')
        temp = 'create table temp as select distinct * from ' + name
        drop = 'drop table ' + name
        rename = 'rename table temp to ' + name
        cursor = con.cursor()
        cursor.execute(temp)
        cursor.execute(drop)
        cursor.execute(rename)
        cursor.close()
        data = pd.read_sql(ifo, con)
        con.close() 
        ori = len(data)
        for i in range(ori):
            if i != ori-1:
                if str(data[i:i+1]['comments'].values[0]) == str(data[i+1:i+2]['comments'].values[0]):
                    rid.append(i+1)
        data = data.drop(rid)
        rid_number.append(len(rid))
        all_records += len(data)
        pd.io.sql.to_sql(data, name, engine, if_exists='replace', index=False) 
    print('we have {0} in {1}'.format(all_records, brand))
    print('we delete {0} from {1}'.format(len(rid_number), brand))
end = time.time()
print('Total {0:.3f} min !'.format((end-begin)/60))  

  
