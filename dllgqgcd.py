#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 14:51:36 2018

@author: Rorschach
@e_mail: 13456019833@163.com
@I hope you find your peace.
"""

import pandas as pd
import numpy as np


data = pd.read_excel('/Users/zhengtian/Desktop/情感词汇本体/情感词汇本体.xlsx')
p = dict()
n = dict()

for i in range(len(data)):
    print(i)
    data.loc[i, '极性'] = np.nan_to_num(data.loc[i]['极性'])
    data.loc[i, '极性2'] = np.nan_to_num(data.loc[i]['极性2'])
    if int(data.loc[i]['极性']) == 3:
        data.loc[i, '极性'] = 1.5
    if int(data.loc[i]['极性2']) == 3:
        data.loc[i, '极性2'] = 1.5
    word = data.loc[i]['词语']
    if int(data.loc[i]['极性2']) == 0:
        jixing = float(data.loc[i]['极性'])
    else:
        jixing = (float(data.loc[i]['极性']) + float(data.loc[i]['极性2']))/2
    if jixing < 1.5 and data.loc[i]['词性种类'] != 'idiom':
        p[word] = 1
    if jixing > 1.5 and data.loc[i]['词性种类'] != 'idiom':
        n[word] = -1

with open('/Users/zhengtian/Desktop/sentiment dict/p/dllg.txt', 'a') as f:
    for i in p:
        f.write(str(i) + '\n')

with open('/Users/zhengtian/Desktop/sentiment dict/n/dllg.txt', 'a') as f:
    for i in n:
        f.write(str(i) + '\n')













