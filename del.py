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

# connect mysql
con = sql.connect(host='localhost', user='root',passwd='',db='huawei',charset='utf8')
sat = {}

find_name = 'select table_name from information_schema.tables where table_schema=\'huawei\' and table_type=\'base table\';'
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
    sat[name] = data
   
con.close() 
    
  
