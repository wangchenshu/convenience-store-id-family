#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

import os
import sys
import csv
import time
# import concurrent.futures
import asyncio
import requests

def check_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def get_area(city):
    driver = webdriver.Chrome()
    area_store_dict[city] = {}
    driver.get(url_city + '?city=' + city)
    area_list_tag = driver.find_element_by_id('areaList')
    area_store_list = area_list_tag.text.split('\n')
    
    with open(dir_family + '/' + city + '.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for area in area_store_list:
            area_store_dict[city][area] = {}
            driver.get(url_area + '?city=' + city + '&area=' + area)
            road_list_tag = driver.find_element_by_id('roadList')
            road_store_list = road_list_tag.text.split('\n')
            for road in road_store_list:
                try:
                    driver.get(url_road + '?city=' + city + '&area=' + area + '&road=' + road)
                    elems = driver.find_elements_by_xpath("//a[@href]")
                    for elem in elems:
                        if 'shop_place' in elem.get_attribute("href"):
                            writer.writerow([elem.get_attribute("href")])
                except Exception as ex:
                    print(ex)
    driver.close()

async def get_area_async(city):
    res = await loop.run_in_executor(None, get_area, city)

load_dotenv()
url_index = 'https://www.family.com.tw/mobile/wtb/shop_next.aspx'
url_city = 'https://www.family.com.tw/mobile/wtb/shop_next2.aspx'
url_area = 'https://www.family.com.tw/mobile/wtb/shop_next3.aspx'
url_road = 'https://www.family.com.tw/mobile/wtb/shop_near.aspx'
city_store_list = []
area_store_dict = {}
shop_list = []
dir_family = './store_family'

## 建立資料夾
check_dir(dir_family)

## headless ##
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# executable_path = '/home/walter/bin/chromedriver'
# driver = webdriver.Chrome(executable_path=executable_path,
# chrome_options=chrome_options)
driver = webdriver.Chrome()
driver.get(url_index)
city_list_tag = driver.find_element_by_id('cityList')
city_list = city_list_tag.text.split('\n')

for city in city_list:
    if '重新查詢' in city:
        continue
    city_store_list.append(city)

# 同步版本
# for city in city_store_list:
#     get_area(city)

# 異步版本
tasks = []
loop = asyncio.get_event_loop()

for city in city_store_list:
    task = loop.create_task(get_area_async(city))
    tasks.append(task)

loop.run_until_complete(asyncio.wait(tasks))