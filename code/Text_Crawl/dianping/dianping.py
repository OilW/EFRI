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



class menu:
    def __init__(self , url , typ , path2):
        self.path = path2
        if 'http:' not in url:
            url = 'http://' + url
        self.url = url
        self.typ = typ
        self.source = ''
        self.shop_url = ''
        self.shop_name = ''
        self.shop_address = ''
        self.shop_type = ''
        self.shop_num_of_dianping = ''
        self.has_more = False
        self.timenow = datetime.datetime.now().strftime("%H:%M:%S")
        self.proxy_list = self.get_proxy_ips()
        if self.getsource()== True:
            self.analyse()

    def getsource(self):
        for tryNum in range(5):
            try:
                header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'}  
                request = urllib.request.Request(url = self.url , headers = header)
                response = urllib.request.urlopen(request)
                data = response.read()
                #print(data)
                try:
                    self.source = data.decode('utf-8')
                except:
                    try:
                        self.source = data.decode('ansi')
                    except:
                        try:
                            self.source = data.decode('gb2312')
                        except:
                            print('decode error!' , self.url)
                            with open('error.txt' , 'a' , encoding = 'utf-8') as f:
                                f.write(self.timenow + '\t' + "decode error!\t" + self.url + '\t' + self.typ + '\n')
                            self.source = ''
                            return False
                return True
            except:
                if tryNum < 4:
                    sleep_time = random.randint(11, 20)
                    print('Internet error, sleep for ' + str(sleep_time) + ' seconds......')
                    time.sleep(sleep_time)
                else:
                    print('Internet error!' , self.url)
                    with open('error.txt' , 'a' , encoding = 'utf-8') as f:
                        f.write(self.timenow + '\t' + "Internet connect error!\t" + self.url + '\t' + self.typ + '\n')
                    self.sourse = ''
                    return False

    def analyse(self):
        try:
            d1 = BeautifulSoup(self.source , "lxml").body
            try:
                d3 = d1.find('div' , {'id':'shop-all-list'})
                d4 = d3.ul
                d2 = d4.find_all('li')
                for d in d2:
                    d3 = d.find('div' , {'class':'tit'})
                    self.shop_name = d3.h4.text
                    print(self.shop_name)
                    self.shop_url = d3.a.get("href")
                    d4 = d.find('div' , {'class':'tag-addr'})
                    self.shop_type = d4.find('a' , {'data-click-name':'shop_tag_cate_click'}).text
                    self.shop_address = d4.find('a' , {'data-click-name':'shop_tag_region_click'}).text + ' ' + d4.find('span' , {'class':'addr'}).text
                    try:
                        d5 = d.find('span' , {'class':'sear-highlight'})
                        self.shop_num_of_dianping = d5.b.text
                    except:
                        d5 = d.find('div' , {'class':'comment'}).find('a' , {'target':'_blank'})
                        self.shop_num_of_dianping = d5.text.strip()
                    self.save()
                    
                pages = d1.find('div' , {'class':'page'})
                if pages != None:
                    pages = pages.find_all('a')
                    if '下一页' in pages[len(pages)-1].text:
                        self.has_more = True
                        self.nexturl = pages[len(pages)-1].get('href')
                        print('next url' , self.nexturl)
                        self.sleep()
                        x = menu(self.nexturl , self.typ , self.path)
                    else:
                        self.sleep()

            except:
                try:
                    d2 = d1.find('ul', {'class': 'shop-list'}).find_all('li')
                    for d in d2:
                        d3 = d.find('p' , {'class':'title'}).a
                        self.shop_name = d3.text
                        print(self.shop_name)
                        self.shop_url = d3.get("href")
                        d4 = d.find('p' , {'class':'area-list'})
                        #self.shop_type = ''
                        self.shop_address = d4.text.strip()
                        d5 =  d.find('p' , {'class':'remark'}).find('a' , {'target':'_blank'})
                        self.shop_num_of_dianping = d5.text
                        self.save()
                    pages = d1.find('div' , {'class':'Pages'})
                    if pages != None:
                        pages = pages.find_all('a')
                        if '下一页' in pages[len(pages)-1].text:
                            self.has_more = True
                            nexturl = pages[len(pages)-1].get('href')
                            if 'http' not in nexturl:
                                self.nexturl = 'www.dianping.com' + nexturl
                            else:
                                self.nexturl = nexturl
                            print('next url' , self.nexturl)
                            self.sleep()
                            x = menu(self.nexturl , self.typ , self.path)
                        else:
                            self.sleep()
                except:
                    try:
                        d2 = d1.find('div', {'class': 'shop-list'}).find_all('li')
                        for d in d2:
                            d3 = d.find('div' , {'class':'shop-title'}).a
                            self.shop_name = d3.text
                            print(self.shop_name)
                            self.shop_url = d3.get("href")
                            d9 = d.find('div' , {'class':'row shop-info-text-i'})
                            try:
                                d4 = d9.find('span' , {'class':'shop-location'})
                                #self.shop_type = ''
                                shop_address = d4.text.strip().split()
                                self.shop_address = ' '.join(shop_address)
                                d5 =  d9.find('a' , {'target':'_blank'})
                                self.shop_num_of_dianping = d5.text
                            except:
                                print('address and num error!')
                            self.save()
                        pages = d1.find('div' , {'class':'pages'})
                        if pages != None:
                            pages = pages.find_all('a')
                            if '下一页' in pages[len(pages)-1].text:
                                self.has_more = True
                                nexturl = pages[len(pages)-1].get('href')
                                if 'http' not in nexturl:
                                    self.nexturl = 'http://www.dianping.com' + nexturl
                                else:
                                    self.nexturl = nexturl
                                print('next url' , self.nexturl)
                                #self.sleep()
                                x = menu(self.nexturl , self.typ , self.path)
                    except:
                        try:
                            d2 = d1.find('ul', {'class': 'shop-list'}).find_all('li')
                            for d in d2:
                                d3 = d.find('p' , {'class':'title'}).a
                                self.shop_name = d3.text
                                print(self.shop_name)
                                self.shop_url = d3.get("href")
                                d9 = d.find('p' , {'class':'baby-info-scraps'})
                                shop_address = d9.text
                                self.shop_address = ' '.join(shop_address)
                                d5 =  d9.find('span' , {'class':'comment-count'})
                                self.shop_num_of_dianping = d5.text
                                self.save()
                            pages = d1.find('div' , {'class':'Pages'})
                            if pages != None:
                                pages = pages.find_all('a')
                                if '下一页' in pages[len(pages)-1].text:
                                    self.has_more = True
                                    nexturl = pages[len(pages)-1].get('href')
                                    if 'http' not in nexturl:
                                        self.nexturl = 'www.dianping.com' + nexturl
                                    else:
                                        self.nexturl = nexturl
                                    print('next url' , self.nexturl)
                                    #self.sleep()
                                    x = menu(self.nexturl , self.typ , self.path)
                        except:
                            try:
                                d2 = d1.find('div', {'class': 'content-wrap'}).find('div', {'class': 'not-found'})
                                print(self.typ + 'not found')
                            except:
                                try:
                                    title = data.head.title.string
                                    if title == '验证中心':
                                        print('验证码！！')
                                        self.sleep()
                                        with open('error.txt' , 'a' , encoding = 'utf-8') as f:
                                            f.write(self.timenow + '\t' + "caught error!\t" + self.url + '\t' + self.typ + '\n')
                                except:
                                    print('content error!' , self.url)
                                    with open('error.txt' , 'a' , encoding = 'utf-8') as f:
                                        f.write(self.timenow + '\t' + "content read error!\t" + self.url + '\t' + self.typ + '\n')

        except:
            print('analyse error!' , self.url)
            with open('error.txt' , 'a' , encoding = 'utf-8') as f:
                f.write(self.timenow + '\t' + "analyse error!\t" + self.url + '\t' + self.typ + '\n')


    def get_proxy_ips(self):
        proxy_list = []
        with open('DianPinCrawler/proxy.txt' , 'r') as f:
            for line in f.readlines():
                items = line.strip().split('\t')
                if len(items) == 2:
                    line = ':'.join(items)
                    proxy_list.append(line)
                else:
                    print(items)
        return proxy_list

    def save(self):
        with open(self.path , 'a' , encoding='utf-8') as f:
            line = str(self.typ) + '\t' + str(self.shop_url) + '\t' + str(self.shop_name) + '\t' + str(self.shop_num_of_dianping) + '\t' + str(self.shop_address) + '\t' + str(self.shop_type)
            f.write(line + '\n')

    def sleep(self):
        sleep_time = random.randint(11, 20)
        print('sleep for ' + str(sleep_time) + ' seconds......')
        time.sleep(sleep_time)

def get_all_urls(path1):
    urls = []
    items_code = ['ch10','ch25','ch30','ch60','ch50','ch15','ch45','ch35','ch70','ch55','ch20','ch95','ch80','ch75','ch65','ch85','ch90','ch40','ch33954']
    items_name = ['美食','电影演出赛事','休闲娱乐','酒店','丽人','K歌','运动健身','周边游','亲子','结婚','购物','宠物','生活服务','学习培训','爱车','医疗健康','家装','宴会','榛果民宿']
    place_code = [['r1577o11','r5894o11','r1601o11','r7764o11','r1602o11','r7766o11','r9347o11','r1972o11','r7765o11','r1579o11','r5893o11','r70187o11','r25448o11','r28854o11'],['r7767o11','r7769o11','r1597o11','r7768o11','r1604o11','r1583o11','r1584o11','r7770o11','r1586o11','r12361o11','r12360o11','r12369o11','r1973o11','r80885o11','r81425o11'],['r7949o11','r1592o11','r70146o11','r7771o11','r1578o11','r1591o11','r1596o11','r1593o11','r1599o11','r9344o11','r7772o11','r66694o11','r67333o11','r70611o11','r84319o11','r11313o11','r70608o11','r70637o11','r85003o11'],['r1974o11','r1588o11','r12315o11','r12366o11','r8950o11','r12316o11','r8949o11','r70537o11','r7760o11','r8948o11','r8952o11','r12317o11','r8951o11'],['r7761o11','r12368o11','r1581o11','r12365o11','r5895o11','r7901o11','r7763o11','r1590o11','r1605o11','r12372o11','r12374o11','r12362o11','r1580o11','r12371o11','r12364o11','r12367o11','r12370o11','r12373o11','r7762o11','r1582o11','r12363o11']]
    place_name = [['春熙路','盐市口','锦华万达','大慈寺','四川师大','九眼桥','红星路','书院街','双桥子','牛市口','合江亭','U37创意仓库','兰桂坊','水锦界'],['宽窄巷子','光华','人民公园','金沙','骡马市','杜甫草堂','青羊宫','太升路','府南新区','北门大桥','北较场','同盛路','草市街','中坝','天府广场'],['高新区','科华北路','跳伞塔','磨子桥','玉林','双楠','桐梓林','武侯祠','高升桥','少陵路','红牌楼','龙湖金楠天街','新街里','中粮大悦城','世豪广场','簇桥','机投','石羊场','复城国际'],['建设路','双林路','望平街','驷马桥','东区音乐公园','八里庄','电视塔','成渝立交','万年场','火车东站','十里店','龙潭寺','熊猫基地'],['九里堤','人民北路','西南交大','李家沱','沙湾','一品天下大街','蜀汉路','梁家巷','抚琴','营门口','羊西线','花牌坊','茶店子','西安北路','荷花池','马家花园','五块石','中海国际','高笋塘','火车站','欢乐谷']]

    for i in range(len(place_code)):
        for j in range(len(place_code[i])):
            for k in range(len(items_code)):
                url = 'http://www.dianping.com/chengdu/' + items_code[k] + '/' + place_code[i][j] + '\t' + place_name[i][j] + ' ' + items_name[k]
                print(url)
                urls.append(url)

    with open(path1 , 'w' , encoding='utf-8') as f:
        for i in urls:
            f.write(i + '\n')
    
def get_shops_menu(path1 , path2):
    urls = []
    with open(path1 , 'r' , encoding='utf-8') as f:
        for line in f.readlines():
            items = line.strip().split('\t')
            if len(items) == 2:
                url = items[0].strip()
                typ = items[1].strip()
                print(url)
                x = menu(url , typ , path2)
                urls.append(url)


def sort_error():
    lines = []
    with open('error.txt' , 'r' , encoding='utf-8') as f:
        for line in f.readlines():
            items = line.strip().split('\t')
            if len(items) == 4:
                items = items[2:]
                if 'http:' not in items[0]:
                    items[0] = 'http://' + items[0]
                line = '\t'.join(items)
                if line not in lines:
                    lines.append(line)

    lines.sort()
    with open('error2.txt' , 'w' , encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')

def re_get_shops_menu(path1 , path2):
    urls = []
    with open(path1 , 'r' , encoding='utf-8') as f:
        for line in f.readlines():
            items = line.strip().split('\t')
            if len(items) == 2:
                url = items[0].strip()
                if 'http:' not in url:
                    url = 'http://' + url
                typ = items[1].strip()
                #print(url)
                x = menu(url , typ , path2)
                urls.append(url)
    '''
    url = 'http://news.sina.com.cn/c/xl/2018-07-15/doc-ihfhfwmv7351257.shtml'
    typ = ' '
    x = menu(url , typ , path2)
    '''

def sort_shop(path):
    urls = []#'http://www.dianping.com/shop/4525935' , 'http://www.dianping.com/shop/6346026']
    lines_less = []
    lines_more = []
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
                    if '封点评' in items[3] or '条点评' in items[3]:
                        items[3] = items[3][:-3]
                    if '我要点评' not in items[3] and items[3] != '0':
                        line = '\t'.join(items)
                        lines.append(line)
                        
    lines.sort()
    with open('shops_urls_all.txt' , 'w' , encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')
                        '''
                        try:
                            items[3] = int(items[3])
                            if items[3] < 10:
                                items[3] = str(items[3])
                                line = '\t'.join(items)
                                lines_less.append(line)
                            else:
                                if 'review_all' not in items[1]:
                                    items[1] = items[1]# + '/review_all'
                                items[3] = str(items[3])
                                line = '\t'.join(items)
                                lines_more.append(line)
                        except:
                            print(items)
            else:
                print(line)

    lines_less.sort()
    with open('shops_urls_less.txt' , 'w' , encoding='utf-8') as f:
        for line in lines_less:
            f.write(line + '\n')
    lines_more.sort()
    with open('shops_urls_more.txt' , 'w' , encoding='utf-8') as f:
        for line in lines_more:
            f.write(line + '\n')
                        '''



def temp():
    return 0
    
    
    
if __name__ == "__main__":
    path1 = 'menu_url.txt'
    path2 = 'shops_urls.txt'
    path3 = 'comments.txt'
    #url = get_all_urls(path1)
    #get_shops_menu(path1 , path2)
    #sort_error()
    #re_get_shops_menu('error2.txt' , path2)
    sort_shop(path2)
    #get_comment(path2 , path3)
    #temp()