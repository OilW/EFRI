# -*- coding: utf-8 -*-

import urllib
from datetime import datetime
from datetime import timedelta


class SearchData:
    def __init__(self, keyword, region, start_time, end_time, types, contains):
        self.keyword = keyword
        self.region = region
        self.types = types
        self.contains = contains
        self.start_time = start_time
        self.end_time = ''
        self.finish_date = end_time
        self.timescope = ''
        self.begin_url = 'http://s.weibo.com/weibo/'
        self.region_code = ''
        self.generate_region_code()
        self.set_search_data()
        return

    def get_timescope(self):
        return self.start_time + ':' + self.end_time

    # 关键字需要进行两次urlencode，这是为了对不同编码格式的字符串的可以得到统一的结果
    def set_keyword(self):
        self.keyword = urllib.urlencode({'kw': self.keyword})[3:]  # urlencode结果为'kw=xxx'
        self.keyword = urllib.urlencode({'kw': self.keyword})[3:]

    # 设置搜索地区
    def set_region(self):
        if self.region != '':
            self.region = '&region=custom:' + self.region_code[self.region] + ':1000'

    # 设置搜索微博的类型字段
    def set_type(self):
        # 0~5：全部、热门、原创、关注人、认证用户、媒体
        type_code = {'0': '&typeall=1', '1': '&xsort=hot', '2': '&scope=ori',
                     '3': '&atten=1', '4': '&vip=1', '5': '&category=4'}
        if self.types in type_code:
            self.types = type_code[self.types]
        else:
            self.types = '&typeall=1'

    # 设置搜索微博的包含字段
    def set_contain(self):
        # 0~4：全部、含图片、含视频、含音乐、含短链
        contain_code = {'0': '&suball=1', '1': '&haspic=1', '2': '&hasvideo=1',
                        '3': '&hasmusic=1', '4': '&haslink=1'}
        if self.contains in contain_code:
            self.contains = contain_code[self.contains]
        else:
            self.contains = '&suball=1'

    # 设置搜索时间范围
    def set_timescope(self):
        self.timescope = '&timescope=custom:' + self.get_timescope()

    def set_datetime(self, times):
        return datetime(int(times[0:4]),
                        int(times[5:7]),
                        int(times[8:10]),
                        int(times[11:13]))

    def set_search_data(self):
        self.set_keyword()
        self.set_region()
        self.set_type()
        self.set_contain()
        self.finish_date = self.set_datetime(self.finish_date)

    # 设置每次搜索的时间范围，并判断爬取时间是否在指定范围内
    def set_next_timescope(self, interval=1):
        if not self.start_time == '-':
            if self.end_time == '':  # 第一次设置爬取时间范围
                start_date = self.set_datetime(self.start_time)
                end_date = start_date + timedelta(hours=interval-1)
            else:
                start_date = self.set_datetime(self.end_time) + timedelta(hours=1)
                end_date = start_date + timedelta(hours=interval-1)

            if start_date > self.finish_date:  # 超出指定时间范围，爬取结束
                return True

            if end_date > self.finish_date:  # 加上时间间隔后范围会超出的情况
                end_date = self.finish_date

            self.start_time = start_date.strftime("%Y-%m-%d-%H")
            self.end_time = end_date.strftime("%Y-%m-%d-%H")
            self.set_timescope()
            return False
        else:
            return False

    def generate_url(self):
        return self.begin_url + self.keyword + self.region + self.types + self.contains + self.timescope + '&page='

    # 各省市或地区对应的搜索地区代号
    def generate_region_code(self):
        self.region_code = {
            '北京': '11',
            '天津': '12',
            '河北': '13',
            '山西': '14',
            '内蒙古': '15',
            '辽宁': '21',
            '吉林': '22',
            '黑龙江': '23',
            '上海': '31',
            '江苏': '32',
            '浙江': '33',
            '安徽': '34',
            '福建': '35',
            '江西': '36',
            '山东': '37',
            '河南': '41',
            '湖北': '42',
            '湖南': '43',
            '广东': '44',
            '广西': '45',
            '海南': '46',
            '重庆': '50',
            '四川': '51',
            '贵州': '52',
            '云南': '53',
            '西藏': '54',
            '陕西': '61',
            '甘肃': '62',
            '青海': '63',
            '宁夏': '64',
            '新疆': '65',
            '台湾': '71',
            '香港': '81',
            '澳门': '82',
            '其他': '100',
            '海外': '400',
        }
