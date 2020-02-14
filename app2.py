#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

import os
import sys
import csv
import time
# import concurrent.futures
import asyncio
import requests
from bs4 import BeautifulSoup

def check_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def mapping_csv_to_list(csv_file):
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        new_list = list(reader)
    return new_list

def get_data(data):
    driver = webdriver.Chrome()
    data_list = mapping_csv_to_list(data['file'])

    with open(dir_family2 + '/' + data['city'] + '.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['店舖名稱','店舖號','服務編號','地址','電話'])

        for link in data_list:
            driver.get(link[0])
            time.sleep(0.5)

            name_tag = driver.find_element_by_name('shopName')
            table_tag = driver.find_element_by_id('shop_content_table')
            table_list = table_tag.text.split('\n')

            tmp_list = [name_tag.text]
            for d in table_list:
                tmp_list.append(d.split('：')[1].strip(' '))
            writer.writerow(tmp_list)
    driver.close()

async def get_data_async(data):
    res = await loop.run_in_executor(None, get_data, data)

dir_family = './store_family'
dir_family2 = './store_family2'

## 建立資料夾
check_dir(dir_family2)

## headless ##
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# executable_path = '/home/walter/bin/chromedriver'
# driver = webdriver.Chrome(executable_path=executable_path,
# chrome_options=chrome_options)

## 取得所有 csv 檔
file_list = os.listdir(dir_family)

# 同步版本
for file in file_list:
    data = {
        'city': file.split('.')[0],
        'file': dir_family + '/' + file
    }
    get_data(data)

# 異步版本
# tasks = []
# loop = asyncio.get_event_loop()

# for file in file_list:
#     data = {
#         'city': file.split('.')[0],
#         'file': dir_family + '/' + file
#     }
#     task = loop.create_task(get_data_async(data))
#     tasks.append(task)

# loop.run_until_complete(asyncio.wait(tasks))