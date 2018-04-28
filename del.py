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
con = sql.connect(host='localhost', user='root',passwd='',db='del',charset='utf8')

find_name = 'select table_name from information_schema.tables where table_schema=\'del\' and table_type=\'base table\';'
table_names = list(pd.read_sql(find_name, con)['table_name'])
for name in table_names:
    cursor = con.cursor()
    delete = 'delete from ' + name + ' where comments in (select cm from (select comments as cm from ' + name + ' group by comments having count(*)>1) as a) and time not in (select mt from (select max(time) as mt from '+ name +' group by comments having count(*)>1) as b);'
    cursor.execute(delete)
    cursor.close()