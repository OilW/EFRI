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

def get_real_url(company):
    browser = webdriver.Chrome()
    for name in company.keys():
        if 'jump?target=' in company[name]:
            browser.get(company[name])
            company[name] = browser.current_url

def get_companies():
    #urls = ['http://cd.ganji.com/zpbiaoqian/wuhou/' , 'http://cd.ganji.com/zpbiaoqian/qingyang/' ,  'http://cd.ganji.com/zpbiaoqian/jinniu/' , 'http://cd.ganji.com/zpbiaoqian/jinjiang/' , 'http://cd.ganji.com/zpbiaoqian/chenghua/']
    urls = ['http://cd.ganji.com/zpbiaoqian/qingyang/o58',
            'http://cd.ganji.com/zpbiaoqian/jinniu/', 'http://cd.ganji.com/zpbiaoqian/jinjiang/',
            'http://cd.ganji.com/zpbiaoqian/chenghua/']

    company_type_1 = {}
    company_type_2 = {}

    for url in urls:
        while url != '':
            print(url)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            data = BeautifulSoup(response.read().decode('utf-8'), "lxml").body
            list1 = data.find_all('dl' , {'class':'list-noimg job-list clearfix new-dl'})
            for d in list1:
                try:
                    d1 = d.find('div' , {'class':'new-dl-company'}).a
                    company_name = d1.text.strip()
                    company_url = d1.get('href')
                    company_type_1[company_name] = company_url
                except:
                    print('error')
                    with open('error.txt' , 'a' , encoding='utf-8') as f:
                        f.write(d + '\n\n\n\n')


            list2 = data.find_all('dl' , {'class':'con-list-zcon new-dl'})
            for d in list2:
                try:
                    d1 = d.find('div' , {'class':'fl con-l-exp new-dl-company'}).a
                    company_name = d1.text.strip()
                    company_url = d1.get('href')
                    company_type_2[company_name] = company_url
                except:
                    print('error')
                    with open('error.txt' , 'a' , encoding='utf-8') as f:
                        f.write(d + '\n\n\n\n')

            try:
                nextpage = data.find('div' , {'class':'pageBox'}).find('a' , {'class':'next'})
                url = 'http://cd.ganji.com' + nextpage.get('href')
            except:
                url = ''

        #company_type_1 = get_real_url(company_type_1)
        with open('list1.txt' , 'a' , encoding='utf-8') as f:
            for name in company_type_1.keys():
                f.write(name + '\t' + company_type_1[name] + '\n')

        #company_type_2 = get_real_url(company_type_2)
        with open('list2.txt' , 'a' , encoding='utf-8') as f:
            for name in company_type_2.keys():
                f.write(name + '\t' + company_type_2[name] + '\n')
        time.sleep(50)

def get_contents_1():
    browser = webdriver.Chrome()
    with open('list1.txt' , 'r' , encoding='utf-8') as fin:
        for line in fin.readlines():
            line = line.strip().split('\t')
            url = line[1]
            print(url)
            name = ''
            coordinate = ''
            address = ''
            content = ''
            if 'jump?target=' in url:
                browser.get(url)
                data = BeautifulSoup(browser.page_source.encode('utf-8'), "lxml").body
            else:
                request = urllib.request.Request(url)
                response = urllib.request.urlopen(request)
                data = BeautifulSoup(response.read().decode('utf-8'), "lxml").body

            try:
                name = data.find('div' , {'class':'compT'}).a.text.strip()
                msg = data.find('div' , {'class':'basicMsg'})
                add = msg.find_all('li')
                for ad in add:
                    if '公司地址' in ad.text:
                        address = ad.text.replace('查看地图' , '')
                        if '地图' in ad.a.text:
                            string = ad.a.get('href')
                            lalo = re.findall(r'(\d+(\.\d+)?)', string)
                            coordinate = str(lalo[2][0]) + ' ' + str(lalo[4][0])
                        break
                content = ' '.join(msg.find('div' , {'class':'compIntro'}).text.strip().split())
            except:
                try:
                    intro = data.find('div' , {'class':'intro_middle'})
                    name = intro.h3.text
                    if '查看全部' in intro.p.text:
                        content = intro.find('p' , {'class':'dis_con'}).text
                    else:
                        content = intro.p.text

                    map = data.find('div' , {'class':'intro_down'}).find('tr' , {'class':'tr_l6'}).find('td' , {'class':'td_c1'})
                    address = map.span.text
                    if '地图' in map.a.text:
                        lalo = re.findall(r'(\d+(\.\d+)?)', map.a.get('href'))
                        coordinate = str(lalo[2][0]) + ' ' + str(lalo[4][0])

                except:
                    print('error')
                    with open('error.txt' , 'a' ) as f:
                        f.write(url + '\n')

            with open('company_content_1.txt', 'a', encoding='utf-8') as f:  # 公司名，坐标，大厦名，文字描述
                f.write(name + '\t' + coordinate + '\t' + address + '\t' + content + '\n')

            time.sleep(10)

def get_contents_2():
    with open('company_content_2.txt' , 'a' , encoding='utf-8') as fout: #公司名，坐标(empty)，大厦名，文字描述
        print('company content txt initial success!')
        with open('list2.txt', 'r', encoding='utf-8') as fin:
            for line in fin.readlines():
                line = line.strip().split('\t')
                name = line[0]
                url = line[1]
                print(name, url)
                request = urllib.request.Request(url)
                response = urllib.request.urlopen(request)
                data = BeautifulSoup(response.read().decode('utf-8'), "lxml").body
                address = ''
                content = ''
                try:
                    information = data.find('p' , {'id':'company_description'})
                    try:
                        temp = information.a.get('data-description')
                    except:
                        temp = information.text
                    temp = temp.strip().split()
                    content = ' '.join(temp)
                except:
                    try:
                        information = data.find_all('ul' , {'class':'info-list clearfix'})
                        if len(information) == 2:
                            for infor in information[0].find_all('li'):
                                if "简介" in infor.text:
                                    temp = infor.find('span' , {'id':'company_description'})
                                    try:
                                        temp = temp.a.get('data-description')
                                    except:
                                        temp = temp.text
                                    temp = temp.strip().split()
                                    content = ' '.join(temp)
                                    break
                            for infor in information[1].find_all('li'):
                                if "注册地址" in infor.text:
                                    address = infor.text
                                    break
                        else:
                            for infor in information[0].find_all('li'):
                                if "简介" in infor.text:
                                    temp = infor.find('span' , {'id':'company_description'})
                                    try:
                                        temp = temp.a.get('data-description')
                                    except:
                                        temp = temp.text
                                    temp = temp.strip().split()
                                    content = ' '.join(temp)
                                if "注册地址" in infor.text:
                                    address = infor.text
                    except:
                        with open('error.txt' , 'a') as f:
                            f.write(url + '\n')
                fout.write(name + '\t \t' + address + '\t' + content + '\n')
                print(content)
                time.sleep(15)

def sort_comment():
    with open('company_content_all.txt' , 'w' , encoding='utf-8') as fout:
        count = 0
        with open('company_content_1.txt' , 'r' , encoding='utf-8') as fin:
            for line in fin.readlines():
                line = line.replace('&nbsp&nbsp&nbsp[收起]' , '')
                if '地址' in line:
                    count += 1
                items = line.strip().split('\t')
                if len(items) > 2:
                    lalo = items[1].split(' ')
                    if len(lalo) == 2 and lalo[0][0] == '1' and lalo[0][1] == '0' and lalo[0][3] == '.' and lalo[1][0] == '3' and lalo[1][1] == '0' and lalo[1][2] == '.':
                            fout.write(line)
                            #count += 1
                    else:
                        print(lalo)
                        items[1] = ' '
                        line = '\t'.join(items)
                        print(line)
                        fout.write(line + '\n')

        with open('company_content_2.txt', 'r', encoding='utf-8') as fin:
            for line in fin.readlines():
                line = line.replace('&nbsp&nbsp&nbsp[收起]' , '')
                if '地址' in line:
                    count += 1
                items = line.strip().split('\t')
                if len(items) > 2:
                    fout.write(line)
        print(count)

if __name__ == "__main__":
    #get_companies()
    #get_contents_2()
    #get_contents_1()
    sort_comment()

