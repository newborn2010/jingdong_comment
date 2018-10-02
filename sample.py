import random
import pymysql as sql
import pandas as pd

brands = ['xiaomi_new', 'huawei_new', 'iphone_new', 'samsung_new', 'honor_new']

# stage 1 随机读取数据库
for brand in brands:
    # connect mysql
    con = sql.connect(host='localhost', user='root', passwd='', db=brand, charset='utf8')
    find_name = 'select table_name from information_schema.tables where table_schema=\'' + brand + '\' and table_type=\'base table\';'
    table_names = list(pd.read_sql(find_name, con)['table_name'])
    p_sample = []
    n_sample = []
    for name in table_names:
        ifo = 'select comments, score from ' + name
        data = pd.read_sql(ifo, con)
        for i in range(len(data)):
            if int(data['score'][i]) > 3:
                p_sample.append((data['comments'][i], data['score'][i]))
            if int(data['score'][i]) < 3:
                n_sample.append((data['comments'][i], data['score'][i]))
    p_sam = random.sample(range(len(p_sample)), 500)  # 正例500个
    n_sam = random.sample(range(len(n_sample)), 500)  # 反例500个
    with open('/Users/zhengtian/Desktop/sample/'+ brand + '.txt', 'a') as com:
        for i in p_sam:
            com.writelines(str(p_sample[i][0]) + ',' + str(p_sample[i][1]) + ',' + '\n')
        for j in n_sam:
            com.writelines(str(n_sample[j][0]) + ',' + str(n_sample[j][1]) + ',' + '\n')
    con.close()


