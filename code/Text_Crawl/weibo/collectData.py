# -*- coding: utf-8 -*-

import urllib2
import os
import time
import random
from lxml import etree
import logging
import xlrd
from xlwt import Workbook
from xlutils.copy import copy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CollectData:
    # 利用微博高级搜索功能，按关键字搜集一定时间范围内的微博。
    def __init__(self, save_dir, is_continue=True):
        self.url = ''

        # 设置结果的存储目录
        self.save_dir = save_dir.decode('utf-8')
        if not os.path.exists(self.save_dir):
            work_book = Workbook(encoding='utf-8')
            work_book.add_sheet('Sheet1')
            work_book.save(self.save_dir)

        # 用来判断爬虫是否可以继续爬取
        self.is_continue = is_continue

        # 初始化日志
        self.logger = logging.getLogger('main.CollectData')

    # 爬取一次请求中的所有网页，最多返回50页
    def download(self, url):
        self.url = url

        max_try = 3  # 网络不好时尝试请求的次数
        has_more = True  # 某次请求可能少于50页，设置标记判断是否还有下一页

        i = 1  # 记录本次请求所返回的页数
        while has_more and i <= 50:  # 最多返回50页，对每页进行解析，并写入结果文件
            source_url = self.url + str(i)  # 构建某页的URL
            print(source_url)
            data = ''  # 存储该页的网页数据
            goon = True  # 网络中断标记

            # 网络不好时尝试重新请求
            for tryNum in range(max_try):
                try:
                    send_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'}
                    req = urllib2.Request(source_url, headers=send_headers)
                    html = urllib2.urlopen(req, timeout=12)
                    data = html.read()
                    break
                except:
                    if tryNum < (max_try - 1):
                        print('internet error,wait 6 seconds.')
                        time.sleep(6)
                    else:
                        print('Internet Connect Error!')
                        self.logger.error('Internet Connect Error!')
                        self.logger.info('url: ' + source_url)
                        self.is_continue = False
                        goon = False
                        break

            if not goon:  # 网络已中断，结束爬取
                self.is_continue = False
                break

            is_caught = True  # 设置标记判断是否被抓住，被抓住后则停止爬取，需要进入页面输入验证码
            if '<div class="m-search" id="pl_feedtop_top">' in data:
                is_caught = False
                has_more = self.analysis(data, i)
            '''
            lines = data.splitlines()
            for line in lines:
                # 判断是否有微博内容，没有出现这一行，则说明被认为是机器人
                # 只取含有微博内容的行，其他行不需要
                if line.startswith('<div class="m-search" id="pl_feedtop_top">'):
                    is_caught = False
                    has_more = self.analysis(data, i)
                    break
            '''


            # 处理被认为是机器人的情况
            if is_caught:
                print('Be Caught!Be Caught!Be Caught!!!')
                with open('weibo.html' , 'w') as f:
                    f.write(data)
                self.logger.error('Error: Be Caught!')
                self.logger.info('url: ' + source_url)
                self.is_continue = False
                break

            if not has_more:
                print('No More Results!')

            sleeptime = self.get_sleeptime()
            print('sleeping ' + str(sleeptime) + ' seconds...')
            time.sleep(sleeptime)

            if not has_more:
                break

            i += 1

    # 解析微博数据
    def analysis(self, data, i):
        # 去掉内容前后多余的标签，并去掉所有的\
        content = data
        with open('html.txt' , 'w') as f:
            f.write(content)
        # 有结果的页面
        # 将网页数据转化为能被XPath匹配的格式
        page = etree.HTML(content.decode('utf-8'))
        # 微博内容
        ps = page.xpath("//p[@node-type='feed_list_content']")
        # 微博发布日期
        dates = page.xpath("//p[@class='from']/a[@suda-data]")


        # 获取微博信息
        index = 0
        for p in ps:
            name = str(p.get('nick-name')).encode('utf-8')  # 获取昵称
            txt = ' '.join(str(p.xpath('string(.)')).strip().split()).encode('utf-8')  # 获取微博内容
            date = ' '.join(dates[index].text.strip().split()).encode('utf-8')  # 微博发布日期
            string = date + '\t' + name + '\t' + txt + '\n'
            #print(string)
            with open(self.save_dir , 'a') as f:
                f.write(string)
            index += 1
            '''
            forward = 0  # 转发数
            comment = 0  # 评论数
            praise = 0  # 点赞数

            fcp = fcps[index].xpath("descendant::span")
            for n in fcp:
                if len(n.xpath("text()")) == 0:
                    if len(n.xpath("em/text()")) != 0:
                        praise = n.xpath("em/text()")[0]  # 点赞数
                elif n.xpath("text()")[0] == '转发':
                    if len(n.xpath("em/text()")) != 0:
                        forward = n.xpath("em/text()")[0]  # 转发数
                elif n.xpath("text()")[0] == '评论':
                    if len(n.xpath("em/text()")) != 0:
                        comment = n.xpath("em/text()")[0]  # 评论数
            addr = 'http:' + str(addrs[index].attrib.get('href'))  # 博主网页地址
            # 导出数据到excel中
            if name is not None and txt is not None:
                rows += 1
                new_worksheet.write(rows, 0, str(rows))
                new_worksheet.write(rows, 1, name.decode('utf-8'))
                new_worksheet.write(rows, 2, date)
                new_worksheet.write(rows, 3, txt.decode('utf-8'))
                new_worksheet.write(rows, 4, str(forward))
                new_worksheet.write(rows, 5, str(comment))
                new_worksheet.write(rows, 6, str(praise))
                new_worksheet.write(rows, 7, addr)
                index += 1
            '''
        print('Save %s microblogs from page-%d successfully' % (index, i))
        self.logger.info('Save ' + str(index) + ' microblogs successfully')
        if '<div class="m-page">' in data:
            return True
        else:
            return False

    # 按比例设置随机等待时间
    def get_sleeptime(self):
        which_time = [0, 0, 0, 1, 1, 1, 1, 2, 3, 3]
        index = random.randint(0, 9)
        if which_time[index] == 0:
            return random.randint(5, 9)
        elif which_time[index] == 1:
            return random.randint(10, 19)
        elif which_time[index] == 2:
            return random.randint(20, 29)
        else:
            return random.randint(30, 50)
