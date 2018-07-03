#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 22:18:52 2018

@author: Rorschach
@mail: 188581221@qq.com
"""
import warnings
warnings.filterwarnings('ignore')

import os
import pandas as pd

path = '/Users/zt/Desktop/xls表'
folder = os.listdir(path)
empty = pd.DataFrame(columns=['评论', '时间', '评分'])
for table in folder:
    if table != '.DS_Store':
        data = pd.read_excel(path + '/' + table)
        empty = empty.append(data, ignore_index=False)
empty.to_excel('/Users/zt/Desktop/yeah.xlsx')
    


























