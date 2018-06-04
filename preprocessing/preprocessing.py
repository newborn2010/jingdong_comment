#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 09:57:23 2018

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
brands = ['jd'] #['xiaomi', 'huawei', 'iphone', 'samsung', 'honor']
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
    for name in [table_names[0], ]:
        ifo = 'select * from ' + name
        default_comment = 'delete from ' + name + ' where comments like \'%此用户未填写%\' and after_comments = \'\';'
        enter = 'update ' + name + ' set comments = replace(comments,\'\\n\',\',\') where comments like \'%\\\\n%\';'
        space = 'update ' + name + ' set comments = replace(comments,\' \',\'\') where comments like \'% %\';'
        cursor = con.cursor()
        cursor.execute(default_comment)
        con.commit()
        cursor.close()
        data = pd.read_sql(ifo, con)
        
end = time.time()
print('Time: {0:.3f} min !'.format((end - begin)/60))
        
        
        
        























