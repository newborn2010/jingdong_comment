#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 15:12:16 2018

@author: Rorschach
@mail: 188581221@qq.com
"""
import warnings
warnings.filterwarnings('ignore')
from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from pyltp import Parser

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
        segmentor.load('/Users/zt/Documents/ltp_data/cws.model', user_dict)
    else:
        segmentor.load('/Users/zt/Documents/ltp_data/cws.model')
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
    postagger.load('/Users/zt/Documents/ltp_data/pos.model')  
    postags = postagger.postag(words)  
    postagger.release()
    return list(postags)

def ner(sentence):
    '''
    LTP 命名实体识别
    '''
    recognizer = NamedEntityRecognizer() 
    recognizer.load('/Users/zt/Documents/ltp_data/ner.model') 
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
    parser.load('/Users/zt/Documents/ltp_data/parser.model')  
    words = segmentor(sentence)
    postags = posttagger(sentence)
    arcs = parser.parse(words, postags)  
    res = [(arc.head, arc.relation) for arc in arcs]
    for i in range(len(res)):
        print(words[i], '---', res[i][1], '-->', words[res[i][0]-1])
    parser.release() 


#测试
sentence = '詹姆斯今天在克利夫兰吃汉堡，他觉得汉堡很好吃。但是我不觉得，所以我抽了他一巴掌。'

sentence_splitter(sentence)
segmentor(sentence)
posttagger(sentence)
ner(sentence)
parse(sentence)

