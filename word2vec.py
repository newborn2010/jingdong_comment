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
from collections import defaultdict
import os

p_path = '/Users/zhengtian/Desktop/sentiment dict/p/'
n_path = '/Users/zhengtian/Desktop/sentiment dict/n/'
cd_path = '/Users/zhengtian/Desktop/sentiment dict/cd/'
fd_path = '/Users/zhengtian/Desktop/sentiment dict/fd/'
p_dir = os.listdir(p_path)
n_dir = os.listdir(n_path)
cd_dir = os.listdir(cd_path)
fd_dir = os.listdir(fd_path)
for i in [p_dir, n_dir, cd_dir, fd_dir]:
    if '.DS_Store' in i:
        i.remove('.DS_Store')

# 程度词典
cd_words = defaultdict(int)
cd_word = []
for i in cd_dir:
    with open(cd_path + i, 'r', encoding='utf-8') as inp:
        a = inp.readlines()
        for j in a:
            cd_word.append(j.replace('\n', '').replace(' ', ''))
cd_word = list(set(cd_word))   
for i in cd_word:
    cd_words[i] = 2
    
# 反义词典
fd_words = defaultdict(int)
fd_word = []
for i in fd_dir:
    with open(fd_path + i, 'r', encoding='utf-8') as inp:
        a = inp.readlines()
        for j in a:
            fd_word.append(j.replace('\n', '').replace(' ', ''))
fd_word = list(set(fd_word))   
for i in fd_word:
    fd_words[i] = -1


# 正负情感词典
p_words = defaultdict(int)
p_word = []
for i in p_dir:
    with open(p_path + i, 'r', encoding='utf-8') as inp:
        a = inp.readlines()
        for j in a:
            p_word.append(j.replace('\n', '').replace(' ', ''))
p_word = list(set(p_word).difference(set(cd_word+fd_word))) 
for i in p_word:
    p_words[i] = 1

n_words = defaultdict(int)
n_word = []
for i in n_dir:
    with open(n_path + i, 'r', encoding='utf-8') as inp:
        a = inp.readlines()
        for j in a:
            n_word.append(j.replace('\n', '').replace(' ', ''))
n_word = list(set(n_word).difference(set(cd_word+fd_word)))         
for i in n_word:
    n_words[i] = -1
    
# stage 1 读取数据库
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

# stage 2 分词
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

# stage 3 清洗
import re

sub = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
begin = time.time()
brands = ['xiaomi_new', 'huawei_new', 'iphone_new', 'samsung_new', 'honor_new']   
for brand in brands:
    f1 = open('/Users/zhengtian/Desktop/word2vec/'+ brand + '_cut.txt')  
    f2 = open('/Users/zhengtian/Desktop/word2vec/'+ brand + '_cut_clean.txt', 'a')  
    lines =f1.readlines()  
    c = 0
    for line in lines:  
        c += 1
        print(c, len(lines))
        line_now = lda.Traditional2Simplified(re.sub(sub, '', line))
        f2.write(line_now + '\n')  
    f1.close()  
    f2.close()
        


# stage 4 找拓展词典
import jieba.posseg as posseg

begin = time.time()
brands = ['samsung_new'] #['xiaomi_new', 'huawei_new', 'iphone_new', 'samsung_new', 'honor_new']   
for brand in brands:
    sentences = word2vec.Text8Corpus(u'/Users/zhengtian/Desktop/word2vec/'+ brand + '_cut.txt')
    model = word2vec.Word2Vec(sentences, size=1000, iter=50, sg=0, window=6, min_count=5)
    
    # p 
    p_add = []
    c = 0
    for word in p_words:
        c += 1
        print(c, len(p_words), brand)
        if word in model.wv.vocab:
            like = model.most_similar(word, topn=30)
            for i in like:
                if posseg.cut(i)[0].flag in ['a', 'ad', 'an', 'd'] and i[0] not in p_words:
                    p_add.append(i[0])
    p_add = list(set(p_add))
    with open('/Users/zhengtian/Desktop/word2vec/'+ brand + '_p_add.txt', 'a') as w:
        for i in p_add:
            w.write(i + '\n')
    # n 
    n_add = []
    c = 0
    for word in n_words:
        c += 1
        print(c, len(n_words), brand)
        if word in model.wv.vocab:
            like = model.most_similar(word, topn=30)
            for i in like:
                if posseg.cut(i)[0].flag in ['a', 'ad', 'an', 'd'] and i[0] not in n_words:
                    n_add.append(i[0])
    n_add = list(set(n_add))
    with open('/Users/zhengtian/Desktop/word2vec/'+ brand + '_n_add.txt', 'a') as w:
        for i in n_add:
            w.write(i + '\n')
    # cd
    cd_add = []
    c = 0
    for word in cd_words:
        c += 1
        print(c, len(cd_words), brand)
        if word in model.wv.vocab:
            like = model.most_similar(word, topn=30)
            for i in like:
                if posseg.cut(i)[0].flag in ['d', 'zg'] and i[0] not in cd_words:
                    cd_add.append(i[0])
    cd_add = list(set(cd_add))
    with open('/Users/zhengtian/Desktop/word2vec/'+ brand + '_cd_add.txt', 'a') as w:
        for i in cd_add:
            w.write(i + '\n')
    # fd
    fd_add = []
    c = 0
    for word in fd_words:
        c += 1
        print(c, len(fd_words), brand)
        if word in model.wv.vocab:
            like = model.most_similar(word, topn=30)
            for i in like:
                if posseg.cut(i)[0].flag in ['c'] and i[0] not in fd_words:
                    fd_add.append(i[0])
    fd_add = list(set(fd_add))
    with open('/Users/zhengtian/Desktop/word2vec/'+ brand + '_fd_add.txt', 'a') as w:
        for i in fd_add:
            w.write(i + '\n')
            
end = time.time()
print('Total {0:.3f} min !'.format((end-begin)/60))  

  





# model.save('/Users/zt/Desktop/word2vec_model')
# model = gensim.models.Word2Vec.load('/Users/zt/Desktop/model/cbow,size1000,iter15/word2vec_model')

























