#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 13:43:12 2018

@author: Rorschach
@mail: 188581221@qq.com
"""
import warnings
warnings.filterwarnings('ignore')
import pymysql as sql
import pandas as pd
import time 

begin = time.time()
brands = ['haier']
for brand in brands:
    # connect mysql
    con = sql.connect(host='localhost', user='root', passwd='', db=brand, charset='utf8')
    find_name = 'select table_name from information_schema.tables where table_schema=\'' + brand + '\' and table_type=\'base table\';'
    table_names = list(pd.read_sql(find_name, con)['table_name'])
    for name in table_names:
        ifo = 'select comments from ' + name
        data = pd.read_sql(ifo, con)
        with open('/Users/zt/Desktop/' + brand + '.txt', 'a') as com:
            for i in range(len(data['comments'])):
                com.writelines(data['comments'][i] + '\n')
    con.close() 
    print('{} done !'.format(brand))
end = time.time()
print('Total {0:.3f} min !'.format((end-begin)/60))