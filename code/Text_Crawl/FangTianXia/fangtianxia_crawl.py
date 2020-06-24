# -*- coding: utf-8 -*-
#Time:2018/11/28 17:02
#Author: yuyou

import os
import random
import re
import time
import requests
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'}


#遍历爬所有的楼盘地址，存在loupan_url.txt中
def find_urls():
    urls_old = ['http://cd.esf.fang.com/housing/129__0_0_0_0_1_0_0_0/',
                'http://cd.esf.fang.com/housing/130__0_0_0_0_1_0_0_0/',
                'http://cd.esf.fang.com/housing/132__0_0_0_0_1_0_0_0/',
                'http://cd.esf.fang.com/housing/133__0_0_0_0_1_0_0_0/',
                'http://cd.esf.fang.com/housing/131__0_0_0_0_1_0_0_0/']
    urls_new = ['http://cd.newhouse.fang.com/house/s/qingyang/',
                'http://cd.newhouse.fang.com/house/s/jinjiang/',
                'http://cd.newhouse.fang.com/house/s/wuhou/',
                'http://cd.newhouse.fang.com/house/s/chenghua/',
                'http://cd.newhouse.fang.com/house/s/jinniu/']
    loupan = []
    for url in urls_old:
        while url != '':
            data = requests.get(url, headers=headers)
            data.encoding = 'gb18030'
            d1 = BeautifulSoup(data.text, "lxml").body
            try:
                d_list = d1.find('div', {'class': 'wid1000'}).find('div', {'class': 'houseList'}).find_all('div', {'class': 'list rel mousediv'})
                for d in d_list:
                    d_data = d.find('dl').find('dd').find('p')
                    d_name = d_data.a.text
                    d_href = 'http:' + d_data.a.get('href')
                    d_price = d.find('div' ,{'class':'listRiconwrap'}).find('p' , {'class':'priceAverage'}).text.strip()
                    loupan.append(d_href + '\t' + d_name + '\t' + d_price + '\n')
                try:
                    url = 'http://cd.esf.fang.com' + d1.find('div', {'class': 'fanye gray6'}).find('a', {'id': 'PageControl1_hlk_next'}).get('href')
                    print(url)
                except:
                    url = ''
            except:
                url = ''

    for url in urls_new:
        while url != '':
            data = requests.get(url, headers=headers)
            data.encoding = 'gb18030'
            d1 = BeautifulSoup(data.text, "lxml").body
            try:
                d_list = d1.find('div', {'id': 'newhouse_loupai_list'}).ul.find_all('li')
                for d in d_list:
                    try:
                        if d.get('id') == None:
                            d_data = d.find('div', {'class': 'nlcd_name'})
                            d_name = d_data.a.text.strip()
                            d_href = 'http:' + d_data.a.get('href')
                            try:
                                d_price = d.find('div', {'class': 'nhouse_price'}).text.strip()
                            except:
                                d_price = '0'
                            loupan.append(d_href + '\t' + d_name + '\t' + d_price + '\n')
                    except:
                        print(d)
                try:
                    url = 'http://cd.newhouse.fang.com' + d1.find('div', {'class': 'page'}).find('a', {'class': 'next'}).get('href')
                    print(url)
                except:
                    url = ''
            except:
                url = ''

    with open('loupan_url.txt' , 'w' , encoding='utf-8') as f:
        for item in loupan:
            f.write(item)


#遍历loupan_url.txt中每一个url，爬所有评论存在loupan_comment.txt中
def find_comments_directly():
    f = open('loupan_comment.txt' , 'w')
    f.close()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'}
    with open('loupan_url.txt' , 'r' , encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip().split('\t')
            url = line[0]
    '''
            name = line[1]
            price = line[2]
            #get latitude and longitude
            data = requests.get(url, headers=headers)
            data.encoding = 'gb18030'
            d1 = BeautifulSoup(data.text, "lxml").body
            
            
            #get comments
            data = requests.get(url + 'dianping', headers=headers)
            data.encoding = 'gb18030'
            d1 = BeautifulSoup(data.text, "lxml").body
            with open('loupan_comment.txt' , 'a' , encoding='utf-8') as f:
                for i in come:
                    f.write()
    '''
#直接找逆向网址，失败了

#遍历loupan_url.txt中每一个url，爬所有评论存在loupan_comment.txt中
def find_xinfang_comments_selenium():
    f = open('comments_xinfang.txt' , 'w')
    f.close()
    browser = webdriver.Chrome()
    with open('loupan_url_xinfang.txt' , 'r' , encoding='utf-8') as fin:
        for line in fin.readlines():
            line = line.strip().split('\t')
            #url = 'http://jinguangexxw.fang.com/dianping/'
            name = line[1]
            url = line[0] + 'dianping'
            print(url)
            browser.get(url)

            Is_continue = True
            while Is_continue:
                for i in range(3):
                    try:
                        nextPage = browser.find_element_by_xpath("//div[@class='more10']")
                        print(nextPage.text)
                        if nextPage.text == '再显示20条':
                            nextPage.click()
                        elif nextPage.text == '没有更多点评':
                            Is_continue = False
                    except:
                        if i < 2:
                            print('NextPage error!' + str(i))
                        else:
                            Is_continue = False

            content = browser.find_elements_by_xpath("//div[@class='comm_list_con']/a/p")
            times = browser.find_elements_by_xpath("//p[@class='look_hou']/em/span")
            print(len(content))
            if len(content) == len(times):
                with open('comments_xinfang.txt' , 'a' , encoding='utf-8') as f:
                    for cont , t in zip(content , times):
                        f.write(name + '\t' + t.text.strip() + '\t' + cont.text.strip() + '\n')
                print(name , 'write success!')
            else:
                with open('comments_xinfang.txt' , 'a' , encoding='utf-8') as f:
                    for cont in content:
                        f.write(name + '\t\t' + cont.text.strip() + '\n')
                print(name , 'write success!')

#爬二手房的评论（前20条）
def find_ershou_comments_selenium():
    f = open('comments_ershou.txt' , 'w')
    f.close()
    with open('loupan_url_ershou.txt' , 'r' , encoding='utf-8') as fin:
        for line in fin.readlines():
            line = line.strip().split('\t')
            #url = 'http://jinguangexxw.fang.com/dianping/'
            name = line[1]
            url = line[0] + 'dianping'
            print(url)
            try:
                data = requests.get(url, headers=headers)
                data.encoding = 'gb18030'
                d1 = BeautifulSoup(data.text, "lxml").body

                d_list = d1.find('ul', {'id': 'dplist'}).find_all('li')
                if d_list!=[]:
                    print(len(d_list))
                    with open('comments_ershou.txt', 'a', encoding='utf-8') as f:
                        for d in d_list:
                            comm = d.find('div', {'class': 'text '})
                            t = comm.text.strip().split('\n')
                            comm = ' '.join(t)
                            f.write(name + '\t' + comm + '\n')
            except:
                with open('error_comments_ershou.txt', 'a', encoding='utf-8') as f:
                    f.write(url + '\t' + name + '\n')

def sort_comment():
    '''
    key = {}
    with open('comments_xinfang.txt' , 'r' , encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip().split('\t')
            if len(line) == 3:
                line = line[0] + '\t' + line[2] + '\n'
                key[line] = 0
            else:
                print(line)
    with open('comments_ershou.txt' , 'r' , encoding='utf-8') as f:
        for line in f.readlines():
            items = line.strip().split('\t')
            if len(items) == 2:
                key[line] = 0
            else:
                print(line)
    with open('comments_fangtianxia.txt' , 'w' , encoding='utf-8') as fout:
        for k in key.keys():
            fout.write(k)
    '''
    loupan = {}
    with open('comments_fangtianxia.txt' , 'r' , encoding='utf-8') as fin:
        for line in fin.readlines():
            line = line.strip().split('\t')[0]
            loupan[line] = 0
    print(len(loupan.keys()))

def get_coordinate():
    with open('loupan_url.txt' , 'r' , encoding='utf-8') as fin:
        for line in fin.readlines():
            line = line.strip().split('\t')
            url = line[0]
            print(url)
            name = line[1]
            price = line[2]
            la = ''
            lo = ''
            try:
                data = requests.get(url, headers=headers)
                data.encoding = 'gb18030'
                data = BeautifulSoup(data.text, "lxml").body
                try:
                    map = data.find('div' , {'class' , 'mapbox'}).iframe.get('src').strip()
                    map = 'http:' + map
                    data = requests.get(map, headers=headers)
                    data.encoding = 'gb18030'
                    data = BeautifulSoup(data.text, "lxml").body.script.text
                    if 'coord' in data:
                        meta = data.strip().split(',')
                        for item in meta:
                            if 'coordx' in item or 'baidu_coord_x' in item:
                                la = item.strip().split(':')[1].replace('"' , '')
                            if 'coordy' in item or 'baidu_coord_y' in item:
                                lo = item.strip().split(':')[1].replace('"' , '')
                except:
                    print('error\t' , url)
                    with open('error_lalo.txt' , 'a') as f:
                        f.write(url + '\n')
            except:
                print('error\t' , url)
                with open('error_lalo.txt' , 'a') as f:
                    f.write(url + '\n')

            if la != '' or lo != '':
                with open('loupan_url_lalo.txt' , 'a' , encoding='utf-8') as f:
                    f.write(url + '\t' + name + '\t' + price + '\t' + la + ' ' + lo + '\n')
            time.sleep(3)



if __name__ == "__main__":
    find_urls()
    #find_xinfang_comments_selenium()
    #find_ershou_comments_selenium()
    #sort_comment()
    #get_coordinate()
