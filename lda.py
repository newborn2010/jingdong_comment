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
import os
import zhon.hanzi
from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from pyltp import Parser
import lda

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
# 正负情感词典
p_words = defaultdict(int)
p_word = []
for i in p_dir:
    with open(p_path + i, 'r', encoding='utf-8') as inp:
        a = inp.readlines()
        for j in a:
            p_word.append(j.replace('\n', '').replace(' ', ''))
p_word = list(set(p_word))   

n_words = defaultdict(int)
n_word = []
for i in n_dir:
    with open(n_path + i, 'r', encoding='utf-8') as inp:
        a = inp.readlines()
        for j in a:
            n_word.append(j.replace('\n', '').replace(' ', ''))
n_word = list(set(n_word))          
# 程度词典
cd_words = defaultdict(int)
cd_word = []
for i in cd_dir:
    with open(cd_path + i, 'r', encoding='utf-8') as inp:
        a = inp.readlines()
        for j in a:
            cd_word.append(j.replace('\n', '').replace(' ', ''))
cd_word = list(set(cd_word))   
    
# 反义词典
fd_words = defaultdict(int)
fd_word = []
for i in fd_dir:
    with open(fd_path + i, 'r', encoding='utf-8') as inp:
        a = inp.readlines()
        for j in a:
            fd_word.append(j.replace('\n', '').replace(' ', ''))
fd_word = list(set(fd_word))   

def word_split(lines, dict_path=None):
    '''
    加载自定义词典并去除停用词，对文本进行分词
    '''
    jieba.enable_parallel(4)
    # 设置 user_dict
    if dict_path != None:
        jieba.load_userdict(dict_path)
    # 分词
    line = lines.replace('\t', '').replace('\n', '').replace('，', '').replace('。', '').replace(' ', '')
    seg_list = list(jieba.cut(line, cut_all=False))
    out = []
    # 设置 stop_word
    stop_words = lda.get_stopword()
    for word in seg_list:
        if stop_words[word] != 1:
            out.append(word)
    return out
    
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


def get_stopword(path=None):
    '''
    对目录中所有的停用词txt进行合并并去重，返回停用词字典。
    '''
    if path == None:
        path = '/Users/zhengtian/Desktop/jd/loading/stop_words'
    dir_list = os.listdir(path)
    key = []   
    for i in dir_list:
        with open(path+'/'+i, 'r') as ip:
            words = ip.readlines()
            for j in words:
                key.append(j.replace('\n', ''))
    key = list(set(key))
    for j in list(set(p_word+n_word+cd_word+fd_word)):
        if j in key:
            key.remove(j)
    stop_words = defaultdict(int)
    for i in key:
        stop_words[i] = 1
    return stop_words

def split_sentence(sentence):
    '''
    按照 ，。？！ 分割句子
    '''
    out = []
    loc = []
    for i in zhon.hanzi.punctuation.strip().replace('！？｡。', '').replace('，', '').replace('、', '').replace('﹔', '').replace('；', ''):
        sentence.replace(i, '')
    for t in range(len(sentence)):
        if sentence[t] not in '，。！？!?,.;；、':
            loc.append(t-1)
            break
    for j in range(len(sentence)-1):
        if sentence[j] in '，。！？!?,.;；、' and sentence[j+1] not in '，。！？!?,.;；、':
            loc.append(j)
            out.append(sentence[loc[-2]+1:j+1])
    out.append(sentence[loc[-1]+1:])
    return out
            
def sentence_splitter(par):
    '''
    简单的根据标点符号的分句
    '''
    sents = SentenceSplitter.split(par) 
    return list(sents)

def segmentor(sentence, user_dict=None):
    '''
    LTP 实现分词
    user_dict: 一行一个词
    '''
    segmentor = Segmentor()  # 初始化实例
    if user_dict != None:
        segmentor.load('/Users/zhengtian/Documents/ltp_data/cws.model', user_dict)
    else:
        segmentor.load('/Users/zhengtian/Documents/ltp_data/cws.model')
    words = segmentor.segment(sentence)  
    words_list = list(words)
    segmentor.release()  # 释放模型
    return words_list

def posttagger(sentence):
    '''
    LTP 词性标注
    '''
    words = segmentor(sentence)
    postagger = Postagger() 
    postagger.load('/Users/zhengtian/Documents/ltp_data/pos.model')  
    postags = postagger.postag(words)  
    postagger.release()
    return list(postags)

def ner(sentence):
    '''
    LTP 命名实体识别
    '''
    recognizer = NamedEntityRecognizer() 
    recognizer.load('/Users/zhengtian/Documents/ltp_data/ner.model') 
    words = segmentor(sentence)
    postags = posttagger(sentence)
    netags = recognizer.recognize(words, postags)  
    for word, ntag in zip(words, netags):
        if ntag != 'O':
            print(word + ' / ' + ntag)
    recognizer.release() 
    return netags

def parse(sentence):
    '''
    LTP 依存句法分析
    '''
    parser = Parser() 
    parser.load('/Users/zhengtian/Documents/ltp_data/parser.model')  
    words = segmentor(sentence)
    postags = posttagger(sentence)
    arcs = parser.parse(words, postags)  
    res = [(arc.head, arc.relation) for arc in arcs]
    #for i in range(len(res)):
        #return words[i], res[i][1], words[res[i][0]-1]
    parser.release() 
    return [(words[i], res[i][1], words[res[i][0]-1]) for i in range(len(res))]        
        
    

































