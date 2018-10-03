#-*-coding:utf-8-*- 
"""
@author: Rorschach
@e_mail: 13456019833@163.com
@I hope you find your peace.
"""
#-*-coding:utf-8-*-

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
import pandas as pd
from gensim.models import word2vec
import os
import numpy as np

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

# stage 2 输入一个小分句，输出分句中的词性，找到 cd,adj。写入字典
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
    ddict = defaultdict(int)
    adjdict = defaultdict(int)
    for i in range(len(AllCx)):
        for j in range(len(AllCx[i])):
            if AllCx[i][j] == 'd':
                ddict[AllComment[i][j]] += 1
            if AllCx[i][j] in ['a', 'b', 'h', 'i', 'z']:
                adjdict[(AllComment[i][j], AllCx[i][j])] += 1
    with open('/Users/zhengtian/Desktop/cd/all_cd.txt', 'a', encoding='utf-8') as f:
        for i in ddict:
            f.write(i + ',' + str(ddict[i]) + '\n')
    with open('/Users/zhengtian/Desktop/adj/all_adj.txt', 'a', encoding='utf-8') as f:
        for i in adjdict:
            f.write(i[0] + ',' + i[1] + ',' + str(adjdict[i]) + '\n')



# stage 3 训练模型，标注 adj
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
p_word = list(set(p_word).difference(set(cd_word + fd_word)))
for i in p_word:
    p_words[i] = 1

n_words = defaultdict(int)
n_word = []
for i in n_dir:
    with open(n_path + i, 'r', encoding='utf-8') as inp:
        a = inp.readlines()
        for j in a:
            n_word.append(j.replace('\n', '').replace(' ', ''))
n_word = list(set(n_word).difference(set(cd_word + fd_word)))
for i in n_word:
    n_words[i] = -1

# stage 3.1 读取数据库
for brand in brands:
    # connect mysql
    con = sql.connect(host='localhost', user='root', passwd='', db=brand, charset='utf8')
    find_name = 'select table_name from information_schema.tables where table_schema=\'' + brand + '\' and table_type=\'base table\';'
    table_names = list(pd.read_sql(find_name, con)['table_name'])
    for name in table_names:
        ifo = 'select comments from ' + name
        data = pd.read_sql(ifo, con)
        with open('/Users/zhengtian/Desktop/adj/train/' + brand + '.txt', 'a') as com:
            for i in range(len(data['comments'])):
                com.writelines(data['comments'][i] + '\n')
    con.close()

# stage 3.2 分词
jieba.load_userdict('/Users/zhengtian/Desktop/sentiment dict/ud/ud.txt')
stop_words = lda.get_stopword()
for brand in brands:
    f1 = open('/Users/zhengtian/Desktop/adj/train/' + brand + '.txt')
    f2 = open('/Users/zhengtian/Desktop/adj/train/' + brand + '_cut.txt', 'a')
    lines = f1.readlines()
    c = 0
    for line in lines:
        c += 1
        out = []
        print(2, c, len(lines))
        line_now = line.replace('\t', '').replace('\n', '').replace('，', '').replace('。', '').replace(' ', '')
        seg_list = list(jieba.cut(line_now, cut_all=False))
        for word in seg_list:
            if stop_words[word] != 1:
                out.append(word)
        f2.write(' '.join(out) + '\n')
    f1.close()
    f2.close()

# stage 3.3 清洗
import re

sub = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~┗ ]+'
begin = time.time()
for brand in brands:
    f1 = open('/Users/zhengtian/Desktop/adj/train/' + brand + '_cut.txt')
    f2 = open('/Users/zhengtian/Desktop/adj/train/all_cut_clean.txt', 'a')
    lines = f1.readlines()
    c = 0
    for line in lines:
        c += 1
        print(3, c, len(lines))
        line_now = lda.Traditional2Simplified(re.sub(sub, '', line))
        f2.write(line_now + '\n')
    f1.close()
    f2.close()

# stage 3.4 训练，标注
begin = time.time()
print('training......')
sentences = word2vec.Text8Corpus(u'/Users/zhengtian/Desktop/adj/train/all_cut_clean.txt')
model = word2vec.Word2Vec(sentences, sg=0, size=100, iter=30, window=5, min_count=3, hs=1)
print('training done!')
end = time.time()
print((end-begin)/60)

adj_score = dict()
for i in adjdict:
    good_s = np.mean(model.similarity('好', i[0]), model.similarity('漂亮', i[0]), model.similarity('不错', i[0]))
    bad_s = np.mean(model.similarity('发烫', i[0]), model.similarity('卡', i[0]), model.similarity('垃圾', i[0]))
    if good_s > bad_s:
        adj_score[i[0]] = 1
    elif good_s < bad_s:
        adj_score[i[0]] = -1
    else:
        adj_score[i[0]] = 0

with open('/Users/zhengtian/Desktop/adj/adj_score.txt', 'a', encoding='utf-8') as f:
    for i in adj_score:
        f.write(i + ',' + str(adj_score[i]) + '\n')


