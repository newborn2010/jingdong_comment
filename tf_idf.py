#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 10:09:24 2018

@author: Rorschach
@mail: 188581221@qq.com
"""
import warnings
warnings.filterwarnings('ignore')
from sklearn.feature_extraction.text import TfidfVectorizer
import time
import numpy as np

# 读取数据
corpus = ['今天 天气 不错 但是 有 一点 热', 
          '他 赢 了 篮球 总决赛', 
          '糯米饭 很 好吃 闻 起来 很 香', 
          '海南省 是 中国 的 旅游 胜地', 
          '太阳系 是 银河系 的 一部分']

def tf_idf(input_path, stop_word=None, show=10):
    '''
    输入已分词文本，以空格隔开，每一行为一个记录，输出 TF_IDF 主题。
    '''
    begin = time.time()
    with open('/Users/zt/Desktop/cut.txt', 'r') as i:
        corpus = []
        for line in i.readlines():
            corpus.append(line.rstrip('\n'))
    # 设置停用词
    with open('/Users/zt/Desktop/project/stop_words/stop_1.txt', 'r') as stop:
        stop_words = []
        for line in stop.readlines():
            stop_words.append(line.rstrip('\n'))
    with open('/Users/zt/Desktop/project/stop_words/stop_2.txt', 'r') as stop:
        for line in stop.readlines():
            stop_words.append(line.rstrip('\n'))
    stop_words = list(set(stop_words))
    # tf_idf
    vectorizer = TfidfVectorizer(stop_words=stop_words, min_df=1)
    vectorizer.fit_transform(corpus)
    name = vectorizer.get_feature_names()
    array = vectorizer.fit_transform(corpus).toarray()
    # 结果
    result = []
    for i in range(array.shape[0]):
        topic = []
        sort = np.argsort(array[i])[::-1][:10]
        for j in sort:
            topic.append(name[j])
        result.append((corpus[i], topic))
    end = time.time()
    print('Total {0:.3f} min !'.format((end-begin)/60))
    return(result[:show])
        



















