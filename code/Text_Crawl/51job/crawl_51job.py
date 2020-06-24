# -*- coding: utf-8 -*-
#Time:2018/12/2 16:23
#Author: yuyou

import datetime
import random
import time
import urllib.request
import re
from bs4 import BeautifulSoup
from selenium import webdriver

def get_all_urls():
    url = 'https://www.51job.com/chengdu/'
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    source = response.read().decode('gb18030')
    data = BeautifulSoup(source, "lxml").body
    companies = {}

    g1 = data.find('div' , {'id':'ad_a'}).find_all('td')
    print(len(g1))
    for c in g1:
        temp = c.a
        companies[temp.get('title')] = temp.get('href')

    g2 = data.find('div' , {'id':'ad_b'}).find_all('td')
    print(len(g2))
    for c in g2:
        temp = c.a
        companies[temp.get('title')] = temp.get('href')

    g3 = data.find('div' , {'id':'ad_c'}).find_all('td')
    print(len(g3))
    for c in g3:
        temp = c.a
        companies[temp.get('title')] = temp.get('href')

    c1 = data.find('div' , {'id':'companyarea1'}).find_all('li')
    for c in c1:
        temp = c.a
        companies[temp.text] = temp.get('href')

    c2 = data.find('div' , {'id':'jobarea1'}).find_all('li')
    print(len(c2))
    for c in c2:
        temp = c.a
        companies[temp.text] = temp.get('href')

    with open('company_url.txt' , 'w' , encoding='utf-8') as f:
        for name in companies:
            f.write(name + '\t' + companies[name] + '\n')

def get_content():
    with open('company_url.txt' , 'r' , encoding='utf-8') as fin:
        for line in fin.readlines():
            line = line.strip().split('\t')
            name = line[0]
            url = line[1]
            url = 'https://jobs.51job.com/hot/30135945-0.html'
            print(url)
            coordinate = ''
            address = ''
            content = ''
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            source = response.read().decode('gb18030')
            data = BeautifulSoup(source, "lxml").body
            try:
                content = ' '.join(data.find('div' , {'class':'con_txt'}).text.strip().split())
                msg = data.find('div' , {'class':'tBorderTop_box bmsg'})
                address = ' '.join(msg.p.text.strip().split())
                lalo = re.findall(r'(\d+(\.\d+)?)', msg.a.get('href'))
                print(lalo)
            except:
                try:
                    print(1)
                except:
                    with open('error.txt' , 'a') as f:
                        f.write(url + '\n')
            with open('content_51job.txt' , 'a' , encoding='utf-8') as fout: # 公司名，坐标，大厦名，文字描述
                fout.write(name + '\t' + coordinate + '\t' + address + '\t' + content + '\n')
            time.sleep(10)


if __name__ == '__main__':
    #get_all_urls()
    get_content()
