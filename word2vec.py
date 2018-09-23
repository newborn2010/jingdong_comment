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
import lda
from gensim.models import word2vec

begin = time.time()
# stage 1
brands = ['xiaomi_new', 'huawei_new', 'iphone_new', 'samsung_new', 'honor_new']
for brand in brands:
    # connect mysql
    con = sql.connect(host='localhost', user='root', passwd='', db=brand, charset='utf8')
    find_name = 'select table_name from information_schema.tables where table_schema=\'' + brand + '\' and table_type=\'base table\';'
    table_names = list(pd.read_sql(find_name, con)['table_name'])
    for name in table_names:
        ifo = 'select comments from ' + name
        data = pd.read_sql(ifo, con)
        with open('/Users/zhengtian/Desktop/word2vec/'+ brand + '.txt', 'a') as com:
            for i in range(len(data['comments'])):
                com.writelines(data['comments'][i] + '\n')
    con.close() 

# stage 2
brands = ['xiaomi_new', 'huawei_new', 'iphone_new', 'samsung_new', 'honor_new']
jieba.load_userdict('/Users/zhengtian/Desktop/sentiment dict/ud/ud.txt') 
stop_words = lda.get_stopword()
for brand in brands:
    f1 = open('/Users/zhengtian/Desktop/word2vec/'+ brand + '.txt')  
    f2 = open('/Users/zhengtian/Desktop/word2vec/'+ brand + '_cut.txt', 'a')  
    lines =f1.readlines()  
    c = 0
    for line in lines:  
        c += 1
        out = []
        print(c, len(lines))
        line_now = line.replace('\t', '').replace('\n', '').replace('，', '').replace('。', '').replace(' ', '')
        seg_list = list(jieba.cut(line_now, cut_all=False))
        for word in seg_list:
            if stop_words[word] != 1:
                out.append(word)
        f2.write(' '.join(out) + '\n')  
    f1.close()  
    f2.close()
    
# stage 3
brands = ['xiaomi_new']   
for brand in brands:
    sentences = word2vec.Text8Corpus(u'/Users/zhengtian/Desktop/word2vec/'+ brand + '_cut.txt')
    model = word2vec.Word2Vec(sentences, size=100, iter=30, sg=1, window=10)


end = time.time()
print('Total {0:.3f} min !'.format((end-begin)/60))  

  





# model.save('/Users/zt/Desktop/word2vec_model')
# model = gensim.models.Word2Vec.load('/Users/zt/Desktop/model/cbow,size1000,iter15/word2vec_model')

























