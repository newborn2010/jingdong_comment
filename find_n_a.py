#-*-coding:utf-8-*-
"""
@author: Rorschach
@e_mail: 13456019833@163.com
@I hope you find your peace.
"""

from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
import lda
import pandas as pd
import pymysql as sql
import time
from sqlalchemy import create_engine
import jieba
from collections import defaultdict
import re
import os
import math

# stage 0 准备
jieba.load_userdict('/Users/zhengtian/Desktop/sentiment dict/ud/ud.txt')
stop_words = lda.get_stopword()
sub = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~┗ ]+'

# stage 1 定义函数
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
    # words = segmentor(sentence)
    postagger = Postagger()
    postagger.load('/Users/zhengtian/Documents/ltp_data/pos.model')
    postags = postagger.postag(sentence)
    postagger.release()
    return list(postags)

# stage 2 输入一个小分句，输出分句中的词性，找到n_a对。写入字典
begin = time.time()
brands = ['xiaomi_new', 'huawei_new', 'iphone_new', 'samsung_new', 'honor_new']
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
    con.close()
    cc = 0
    AllComment = []
    for name in table_names:
        cc += 1
        ifo = 'select * from ' + name
        con = sql.connect(host='localhost', user='root', passwd='', db=brand, charset='utf8')
        data = pd.read_sql(ifo, con)
        comments = list(data['comments'])
        tt = 0
        for comment in comments:
            tt += 1
            print('Now : table {0} in {1} total {2}'.format(cc, brand, len(table_names)))
            print(tt,len(comments))
            comment_c = lda.Traditional2Simplified(re.sub(sub, '', comment))
            co_split = lda.split_sentence(comment_c)  # 得到一个分句后的评论
            if co_split != []:
                for i in co_split:
                    out = []
                    seg_list = list(jieba.cut(i, cut_all=False))
                    for word in seg_list:
                        if stop_words[word] != 1:
                            out.append(word)
                    AllComment.append(out)
    AllCx = []
    postagger = Postagger()
    postagger.load('/Users/zhengtian/Documents/ltp_data/pos.model')
    aa = 0
    for i in AllComment:
        aa += 1
        print(aa, len(AllComment))
        postags = postagger.postag(i)
        AllCx.append(list(postags))
    postagger.release()
    nadict = defaultdict(int)
    for i in range(len(AllCx)):
        CoSplit = AllComment[i]
        MaxLoc = -1
        while 'n' in AllCx[i] and 'a' in AllCx[i]:  # 怎么定位所有的 n_a
            nloc = AllCx[i].index('n')
            aloc = AllCx[i].index('a')
            n = CoSplit[nloc+MaxLoc+1]
            a = CoSplit[aloc+MaxLoc+1]
            nadict[(n, a)] += 1
            MaxLoc = max(nloc, aloc)
            AllCx[i] = AllCx[i][MaxLoc+1:]
            if 'n' not in AllCx[i] or 'a' not in AllCx[i]:
                break
    with open('/Users/zhengtian/Desktop/na/' + brand +'.txt', 'a', encoding='utf-8') as f:
        for i in nadict:
            f.write(i[0] + ',' + i[1] + ',' + str(nadict[i]) + '\n')
# stage 3 整合 n_a 对
path = '/Users/zhengtian/Desktop/na/'
p_dir = os.listdir(path)
out = dict()
for i in p_dir:
    if i == '.DS_Store':
        p_dir.remove('.DS_Store')
number = [1559354, 458269, 510058, 24809, 1407282]
for brand in brands:
    num = number[brands.index(brand)]
    with open(path + brand + '.txt', 'r', encoding='utf-8') as r:
        for i in r.readlines():
            mes = i.split(',')
            if int(mes[2]) > math.floor(0.0001 * num):
                out[(mes[0], mes[1])] = 1
with open(path + 'all.txt', 'a', encoding='utf-8') as f:
    for i in out:
        f.write(i[0] + ',' + i[1] + '\n')




