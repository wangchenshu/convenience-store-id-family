import os
import sys
import csv
import pymysql


dir_family = './store_family2'
file_list = os.listdir(dir_family)
store_type = 'family'

conn = pymysql.connect(host = '127.0.0.1', user = 'root', passwd = "123456", db = 'test', charset='utf8')
cursor = conn.cursor()

for file in file_list:
    city = file.split('.')[0]

    with open(dir_family + '/' + file, newline='') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            if '店舖名稱' in row:
                continue
            effect_row = cursor.execute(
                'INSERT INTO `convenience_store` (`type`, `city`, `store_name`, `store_num`, `service_num`, `address`, `phone`) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (store_type, city, row[0], row[1], row[2], row[3], row[4])
            )

conn.commit()
cursor.close()
conn.close()