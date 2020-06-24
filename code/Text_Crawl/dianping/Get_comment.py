# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 11:07:29 2018

@author: KeXie
"""
import datetime
import random
import time
import urllib.request
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class shop_more:
    def __init__(self , shangquan , url, name, path , referer):
        self.url = url
        if 'p101' in self.url:
            return
        else:
            self.shangquan = shangquan
            self.name = name
            self.savepath = path
            self.timenow = datetime.datetime.now().strftime("%H:%M:%S")
            self.header = {}
    
            self.star_list={
                'sml-str00':'0.0',
                'sml-str05':'0.5',
                'sml-str10':'1.0',
                'sml-str15':'1.5',
                'sml-str20':'2.0',
                'sml-str25':'2.5',
                'sml-str30':'3.0',
                'sml-str35':'3.5',
                'sml-str40':'4.0',
                'sml-str45':'4.5',
                'sml-str50':'5.0'
            }
    
            self.longitude = ''
            self.latitude = ''
            self.header['Referer'] = referer
            if self.getsource() == True:
                self.analyse()

    def get_cookies(self):
        cookies = []
        with open('many_cookies.txt' , 'r') as f:
            for line in f.readlines():
                items = line.strip().split('\t')
                if len(items) == 3:
                    cookies.append(items[2].strip())
        self.cookies = cookies

    def get_a_cookie(self):
        cookies = []
        with open('cookie.txt' , 'r') as f:
            line = f.readline().strip()
        cookies.append(line)
        self.cookies = cookies

    def get_header_cookie(self):
        #self.get_cookies()
        self.get_a_cookie()
        ua = UserAgent()
        self.header = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            #'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Cookie': random.choice(self.cookies) ,
            'Host':'www.dianping.com',
            #'If-Modified-Since':'Tue, 24 Jul 2018 00:25:37 GMT',
            #'If-None-Match':'"'+'20f1a0216597902b286206f9d13fa4b5' + '"',
            'Referer':'http://www.dianping.com/' ,
            'Upgrade-Insecure-Requests':'1',
            'User-Agent': ua.random
        }

    def getsource(self):
        for tryNum in range(5):
            try:
                self.get_header_cookie()
                request = urllib.request.Request(url=self.url, headers=self.header )
                response = urllib.request.urlopen(request)
                data = response.read()
                try:
                    self.source = data.decode('utf-8')
                except:
                    try:
                        self.source = data.decode('ansi')
                    except:
                        try:
                            self.source = data.decode('gb2312')
                        except:
                            print('decode error!', self.url)
                            with open('dianping_error.txt', 'a', encoding='utf-8') as f:
                                f.write(self.timenow + '\t' + "decode error!\t" + self.url + '\t' + '\n')
                            self.source = ''
                            return False
                return True
                '''
                '''
            except:
                if tryNum < 4:
                    sleep_time = random.randint(21, 30)
                    print('Internet error, sleep for ' + str(sleep_time) + ' seconds......')
                    time.sleep(sleep_time)
                else:
                    print('Internet error!', self.url)
                    with open('dianping_error.txt', 'a', encoding='utf-8') as f:
                        f.write(self.timenow + '\t' + "Internet connect error!\t" + self.url + '\t' + '\n')
                    self.sourse = ''
                    return False

    def analyse(self):
        try:
            soup = BeautifulSoup(self.source , 'lxml').body
            d1 = soup.find('div' , {'class':'reviews-items'})
            d2 = d1.ul.find_all('li', recursive=False)
            for d in d2:
                self.star = ''  # 几颗星
                self.taste = ''  # 口味，环境，服务
                self.environment = ''
                self.service = ''
                self.commentBody = ''  # 评论内容
                self.time = ''

                d3 = d.find('div' , {'class':'review-rank'})
                d5 = d3.find('span')
                star = d5.get('class')
                if len(star) > 2:
                    star = star[1]
                    self.star = self.star_list[star]
                else:
                    self.star = star
                d6 = d3.find_all('span' , {'class':'item'})
                if len(d6) > 2:
                    self.taste = d6[0].text.strip()
                    self.environment = d6[1].text.strip()
                    self.service = d6[2].text.strip()
                    #self.aver = d6[3].text

                try:
                    d4 = d.find('div' , {'class':'review-words Hide'})
                    self.commentBody = d4.text.strip().split()[:-1]
                    self.commentBody = ' '.join(self.commentBody)
                except:
                    try:
                        d4 = d.find('div', {'class': 'review-words'})
                        self.commentBody = d4.text.strip()
                    except:
                        try:
                            d4 = d.find('div', {'class': 'review-truncated-words'})
                            self.commentBody = d4.text.strip()
                        except:
                            print('dianping content error!')
                            with open('dianping_error.txt' , 'a') as f:
                                f.write(self.timenow + '\t' + "dianping content error!\t" + self.url + '\n')

                d7 = d.find('span' , {'class':'time'})
                self.time = d7.text.strip().split('\n')
                self.time = ' '.join(self.time)
                print(self.time)
                self.save()

            pages = soup.find('div', {'class': 'reviews-pages'})
            if pages != None:
                pages = pages.find_all('a')
                if '下一页' in pages[len(pages) - 1].text:
                    self.has_more = True
                    self.nexturl = pages[len(pages) - 1].get('href')
                    self.nexturl = 'http://www.dianping.com' + self.nexturl
                    print('next url\n', self.nexturl)
                    #self.sleep()
                    shop_more(self.shangquan, self.nexturl, self.name, self.savepath , self.url)


        except:
            try:
                soup = BeautifulSoup(self.source , 'lxml').body
                d1 = soup.find('div' , {'class':'review-list-header'})
                print(d1.text)
            except:
                try:
                    soup = BeautifulSoup(self.source , 'lxml').body
                    d1 = soup.find('p' , {'class':'not-found-words'})
                    print(d1.text)
                    if '不展示评价' not in d1.text and '政府' not in d1.text:
                        with open('dianping_error.txt' , 'a') as f:
                            f.write(self.timenow + '\t' + "no content error!\t" + self.url + '\n')
                        #self.sleep()
                except:
                    soup = BeautifulSoup(self.source , 'lxml').body
                    d1 = soup.find('div' , {'id':'not-found-tip'})
                    print(d1.text)
                    if '不展示评价' not in d1.text and '政府' not in d1.text:
                        with open('dianping_error.txt' , 'a') as f:
                            f.write(self.timenow + '\t' + "no content error!\t" + self.url + '\n')
                        #self.sleep()

    def save(self):
        with open(self.savepath, 'a', encoding='utf-8') as f:
            line = str(self.shangquan) + '\t' + str(self.name) + '\t' + str(self.time) + '\t' + str(self.star) + '\t' + str(self.taste) + '\t' + str(self.environment) + '\t' + str(self.service) + '\t' + str(self.commentBody)
            f.write(line + '\n')

    def sleep(self):
        sleep_time = random.randint(20, 30)
        print('sleep for ' + str(sleep_time) + ' seconds......')
        time.sleep(sleep_time)


def get_comment_more(path1 , path2):
    shangquans = []
    with open('la_lo_shangquan.txt' , 'r' , encoding='utf-8') as f:
        for line in f.readlines():
            items = line.strip().split('\t')
            if len(items) == 3:
                shangquans.append(items)
            else:
                print(line)

    with open(path1 , 'r' , encoding='utf-8') as f:
        for line in f.readlines():
            items = line.strip().split("\t")
            if len(items) > 3:
                district = ''
                shangquan = ''
                for sq in shangquans:
                    if sq[1] in items[0]:
                        district = sq[0]
                        shangquan = sq[1]
                        break
                url = items[1]# + '/review_all
                print(url)
                referer = url[:-11]#'http://www.dianping.com/' 
                name = items[2]
                savepath = path2 + district + ' ' + items[0] + '.txt'
                '''
                '''
                if '榛果民宿' not in items[0]:
                    shop_more( shangquan , url, name, savepath , referer)
                else:
                    f = open(savepath , 'w')
                    f.close()
            else:
                print(items)


if __name__ == '__main__':
    #path_url_name = 'shops_urls_temp.txt'
    path_comment = 'comment/'
    path_url_less = 'shops_urls_less.txt'
    path_url_more = 'shops_urls_more.txt'
    get_comment_more(path_url_more , path_comment)
    #get_comment_more(path_url_less , path_comment)