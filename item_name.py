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

brands = ['xiaomi_new'] #['xiaomi', 'huawei', 'iphone', 'samsung', 'honor']
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
        all_names.append((count-1,item))
        con.close()

iphone_need = [1, 12, 13, 14, 15, 28, 29, 30, 31, 32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49, 52, 60, 61, 62, 73, 74, 96, 97,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122, 174,175,176,204,205,222,223,224,226,227,228,229,231]
samsung_need = [28, 29, 31, 32, 35, 36, 38, 39, 40, 41, 42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,85,86,87,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,109,110,111,112,113,114,115,116,117,118,119,120,121,122]
huawei_not_sneed = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,27,28,29,30,31,33,34,35,36,37,39,40,42,43,48,49,51,60,61,62,63,64,65,76,77,78,79,80,81,82,83,84,85,97,99,100,101,102,103,
        106,107,108,114,117,118,120,127,128,129,130,131,132,135,136,143,144,145,151,152,153,154,158,164,183,184,185,186,187,188,189,190,191,192,193,194,198,199,220,221,244,245,246,262,263,264,
        265,267,268,269,289,290,292,293,295,298,301,311]
honor_need = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,44,46,47,48,49,50,51,54,55,57,58,59,60,61,62,69,70,74,75,76,77,78,79,87,95,97,
        98,99,100,101,102,103,108,112,113,114,115,116,117,118,120,123,132,147,164,165,166,167,168,169,173,174,175,181,186,187,188,191,193,194,195,197,198,199,200,201,202,208,216,217,219,237,
        239,240,247,249,250,262]
need = [31,32,45,47,51,52,53,55,56,57,61,63,66,67,69,74,75,76,85,90,91,92,96,97,98,99,102,107,108,109,111,112,114,116,117,118,119,122,123,124,125,132,136,140,141,142,143,144,145,146,147,148,149,150,151,152,
        153,156,163,164,165,166,168,169,170,171,172,173,174,175,176,177,178,180,181,187,188,189,192,193,194,195,196,197,198,199,200,201,203,204,205,207,208,210,211,217,218,219,220,221,222,223,224,225,226,
        227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,246,247,248,250,251,253,257,258,259,260,261,262,268,283,274,276,277,278,279,280,281,282,283,284,286,287,288,289,290,291,292,
        293,294,297,298,301,302,305,306,307,309,310,313,314,315,316,319,321,322,323,324,325,326,327,328,329,330,334,335,336,337,338,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,357,
        361,362,363,364,366,367,368,369,370,371,372,373,374,375,376,377,378,379,380,381,382,383,384,385,386,387,388,391,392,393,396,397,398,399,400,401,402,403,404,405,406,408,409,410,411,412,413,414,
        415,416,417,418,419,420,421,422,423,424,425,426,427,428,429,430,431,432,433,435,436,437,438,439,440,441,442,443,444,448,449,450,451,452,453,454,459,460,462,463,463,465]

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
        if count-1 not in need:
            con = sql.connect(host='localhost', user='root', passwd='', db=brand, charset='utf8')
            delete = 'drop table  ' + name
            cursor = con.cursor()
            cursor.execute(delete)
            con.commit()
            cursor.close()
            con.close()














