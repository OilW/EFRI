# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 13:20:46 2018

@author: KeXie
"""

import datetime
import random
import re
import sys
import time
import urllib.request
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def sort_shop(path):
    urls = []
    lines = []
    with open(path , 'r' , encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            items = line.split('\t')
            if len(items) > 4:
                if 'http' not in items[1]:
                    items[1] = 'http:' + items[1]
                if items[1] not in urls:
                    urls.append(items[1])
                    line = '\t'.join(items)
                    lines.append(line)
            else:
                print(items)
                        
    lines.sort()
    with open('shops_urls_all.txt' , 'w' , encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')

def get_lalo(url):
    print(url)
    lalo = ''
    ua = UserAgent()
    timenow = datetime.datetime.now().strftime("%H:%M:%S")
    
    for tryNum in range(3):
        try:
            header = {
                    #'Referer':'http://www.dianping.com/' ,
                    'User-Agent': ua.random
                }
            request = urllib.request.Request(url=url, headers=header )
            response = urllib.request.urlopen(request)
            data = response.read()
            try:
                source = data.decode('utf-8')
            except:
                try:
                    source = data.decode('ansi')
                except:
                    try:
                        source = data.decode('gb2312')
                    except:
                        print('decode error!', url)
                        with open('error_lalo.txt', 'a', encoding='utf-8') as f:
                            f.write(timenow + '\t' + "decode error!\t" + url + '\n')
                        return False
            '''
            '''
        except:
            if tryNum < 2:
                sleep_time = random.randint(21, 30)
                print('Internet error, sleep for ' + str(sleep_time) + ' seconds......')
                time.sleep(sleep_time)
            else:
                print('Internet error!', url)
                with open('error_lalo.txt', 'a', encoding='utf-8') as f:
                    f.write(timenow + '\t' + "Internet connect error!\t" + url + '\n')
                #sys.exit()
                return False
    #print(source)
    
    try:
        d = BeautifulSoup(source , "lxml").body
        d1 = d.find_all('script', recursive=False)
        for d2 in d1:
            if 'shopGlat' in d2.text and 'shopGlng' in d2.text:
                #print(d2.text)
                jj = re.findall( r'(\d+(\.\d+)?)' , d2.text)
                #print(jj)
                for x in jj:
                    if '104.' in x[0] or '103.' in x[0]:
                        longitude = x[0]
                        break
                for x in jj:
                    if '30.' in x[0] or '29.' in x[0] or '31.' in x[0]:
                        latitude = x[0]
                        break
                lalo = longitude + ' ' + latitude
                return lalo
        if lalo == '':
             d1 = d.find('div' , {'class':'aside'})
             d2 = d1.find('script' , recursive=False)
             temp = d2.text.split()
             for line in temp:
                 #print(line)
                 if '104.' in line or '103.' in line:
                     if '30.' in line or '29.' in line or '31.' in line:
                         jj = re.findall( r'(\d+(\.\d+)?)' , line)
                         longitude = jj[0][0]
                         latitude = jj[1][0]
                         lalo = longitude + ' ' + latitude
                         return lalo
        '''
        '''
    except:
        print('content error!', url)
        with open('error_lalo.txt', 'a', encoding='utf-8') as f:
            f.write(timenow + '\t' + "contect error!\t" + url + '\n')
        return False

    return lalo

def main():
    with open('shops_urls_all.txt' , 'r' , encoding = 'utf-8') as f:
        for line in f.readlines():
            items = line.strip().split('\t')
            url = items[1]
            if '结婚' in items[0] or '民宿' in items[0] or '家装' in items[0]:
                x = 'None'
            else:
                x = get_lalo(url)
            if x != False and x != '':
                    items[3] = x
                    print(x)
                    line = '\t'.join(items)
                    with open('shops_urls_all_2.txt' , 'a' , encoding = 'utf-8') as f2:
                        f2.write(line + '\n')
            else:
                with open('shops_urls_all_error.txt' , 'a' , encoding = 'utf-8') as f2:
                    f2.write(line)
                '''
                '''

    
if __name__ == "__main__":
    path1 = 'shops_urls.txt'
    #sort_shop(path1)
    main()