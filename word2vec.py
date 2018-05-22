#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 18 13:54:50 2018

@author: Rorschach
@mail: 188581221@qq.com
"""
import warnings
warnings.filterwarnings('ignore')

import pymysql as sql
import pandas as pd
import time 
import jieba
import gensim
from gensim.models import word2vec

begin = time.time()
brands = ['jd']
for brand in brands:
    # connect mysql
    con = sql.connect(host='localhost', user='root', passwd='', db=brand, charset='utf8')
    find_name = 'select table_name from information_schema.tables where table_schema=\'' + brand + '\' and table_type=\'base table\';'
    table_names = list(pd.read_sql(find_name, con)['table_name'])
    for name in table_names:
        ifo = 'select comments from ' + name
        data = pd.read_sql(ifo, con)
        with open('/Users/zt/Desktop/test.txt', 'a') as com:
            for i in range(len(data['comments'])):
                com.writelines(data['comments'][i] + '\n')
    con.close() 
    
f1 = open('/Users/zt/Desktop/test.txt')  
f2 = open('/Users/zt/Desktop/test_cut.txt', 'a')  
lines =f1.readlines()  
for line in lines:  
    line = line.replace('\t', '').replace('\n', '').replace('，', '').replace('。', '').replace('   ', '')
    seg_list = jieba.cut(line, cut_all=False)  
    f2.write(' '.join(seg_list) + '\n')  
f1.close()  
f2.close()

sentences = word2vec.Text8Corpus(u'/Users/zt/Desktop/test_cut.txt')
model = word2vec.Word2Vec(sentences, size=1000, iter=15)

with open('/Users/zt/Desktop/test_cut.txt', 'r') as comm:
    comme = comm.read()

end = time.time()
print('Total {0:.3f} min !'.format((end-begin)/60))  


model.save('/Users/zt/Desktop/word2vec_model')
model = gensim.models.Word2Vec.load('/Users/zt/Desktop/word2vec_model')

























