#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 13:19:57 2018

@author: Rorschach
@mail: 188581221@qq.com
"""
import warnings
warnings.filterwarnings('ignore')

from gensim.models import LdaMulticore
from gensim.corpora import Dictionary
from collections import defaultdict
import jieba_fast as jieba 
import time

def word_split(input_path, output_path, dict_path=None, stop_word=None):
    '''
    加载自定义词典并去除停用词，对文本进行分词
    '''
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
        if stop_word != None:
            stop_words = defaultdict(int)
            with open(stop_word, 'r') as stop:
                for line in stop.readlines():
                    stop_words[line.rstrip('\n')] = 1
            for word in seg_list:
                if stop_words[word] != 1:
                    out.append(word)
        else:
            out = seg_list
        if out != []:
            train.append(out)
            f2.write(' '.join(out) + '\n')  
    f1.close()  
    f2.close()
    return train
    
def LDA_model(input_path, output_path, dict_path=None, stop_word=None, topic=10):
    '''
    输入未分词文本，每行为一个记录，输出 LDA 主题模型结果。
    '''
    begin = time.time()
    # 分词
    train = word_split(input_path, output_path, dict_path=dict_path, stop_word=stop_word)
    print('分词成功！')
    # LDA
    dictionary = Dictionary(train)
    corpus = [dictionary.doc2bow(text) for text in train]
    lda = LdaMulticore(corpus=corpus, id2word=dictionary, num_topics=topic, workers=3, passes=1)
    end = time.time()
    print(lda.print_topics(topic))
    print('Total {0:.3f} min !'.format((end-begin)/60))





