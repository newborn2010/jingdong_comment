#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 21:28:33 2018

@author: Rorschach
@mail: 188581221@qq.com
"""
import warnings
warnings.filterwarnings('ignore')
from selenium import webdriver
import re
import requests as rq
import re
import time
import pymysql as sql

all_id = []
pages = range(1,6)
for page in pages:
    url = 'https://mideash.jd.com/view_search-402471-1000001281-1000001281-0-2-0-0-1-'+ str(page) + '-60.html?isGlobalSearch=0&other='
    browser = webdriver.Chrome()
    browser.get(url)
    html = browser.page_source
    browser.close()
    ifo = re.findall('item.jd.com\/(.*?).html', html)
    for i in ifo:
        all_id.append(int(i))

id = list(set(all_id))

# check
# =============================================================================
# count = 0
# browser = webdriver.Chrome()
# for a in id:
#     url = 'https://item.jd.com/' + str(a) + '.html'
#     browser.get(url)
#     count += 1
#     browser.execute_script('window.open()')
#     browser.switch_to_window(browser.window_handles[count])
# =============================================================================






















