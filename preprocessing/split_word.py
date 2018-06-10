#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 17:03:21 2018

@author: Rorschach
@mail: 188581221@qq.com
"""
import warnings
warnings.filterwarnings('ignore')
import jieba
from collections import defaultdict
import time 


def word_split(input_path, output_path, dict_path=None, stop_word=None):
    '''
    加载自定义词典并去除停用词，对文本进行分词。
    '''
    begin = time.time()
    jieba.enable_parallel(4)
    train = []
    # 设置 user_dict
    if dict_path != None:
        jieba.load_userdict(dict_path)
    # 分词
    f1 = open(input_path)  
    f2 = open(output_path + '/cut.txt', 'a')  
    lines =f1.readlines()  
    for line in lines:  
        line = line.replace('\t', '').replace('\n', '').replace('，', '').replace('。', '').replace(' ', '')
        seg_list = list(jieba.cut(line, cut_all=False))
        out = []
        # 设置 stop_word
        stop_words = defaultdict(int)
        with open('/Users/zt/Desktop/project/stop_words/stop_1.txt', 'r') as stop:
            for line in stop.readlines():
                stop_words[line.rstrip('\n')] = 1
        with open('/Users/zt/Desktop/project/stop_words/stop_2.txt', 'r') as stop:
            for line in stop.readlines():
                stop_words[line.rstrip('\n')] = 1
        #  设置额外的 stop_word
        if stop_word != None:
            stop_words = defaultdict(int)
            with open(stop_word, 'r') as stop:
                for line in stop.readlines():
                    stop_words[line.rstrip('\n')] = 1
        # 去 stop_word
        for word in seg_list:
            if stop_words[word] != 1:
                out.append(word)
        if out != []:
            #train.append(out)
            f2.write(' '.join(out) + '\n')  
    f1.close()  
    f2.close()
    end = time.time()
    print('Total {0:.3f} min !'.format((end-begin)/60))
    #return train
