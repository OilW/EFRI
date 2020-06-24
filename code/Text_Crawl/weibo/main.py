# -*- coding: utf-8 -*-

import logging
import login
import collectData
import searchData


def main():

    # 爬取日志记录
    logger = logging.getLogger('main')  # 创建一个logger并指定名称
    log_file = './weibo_crawler.log'
    logger.setLevel(logging.DEBUG)  # 设置logger级别，低于该级别的信息都不输出
    # 创建一个handler，用于写入日志文件
    filehandler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')  # 指定log输出格式
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)

    print('**********新浪微博爬虫系统**********')
    keyword = raw_input('请输入关键词: ')
    types = raw_input('类型代号(0:全部、1:热门、2:原创、3:关注人、4:认证用户、5:媒体)\n请输入微博的类型代号(默认为0): ')
    contains = raw_input('包含代号(0:全部、1:含图片、2:含视频、3:含音乐、4:含短链)\n请输入微博的包含代号(默认为0): ')
    region = raw_input('请输入搜索省市(默认为所有地区): ')
    start_time = raw_input('请输入搜索起始时间(yyyy-mm-dd-hh): ')
    end_time = raw_input('请输入搜索结束时间(yyyy-mm-dd-hh): ')
    interval = raw_input('请输入一次搜索的小时间隔(默认为2): ')
    # save_path = 'H:\\weibo_data\\weiboData.xls'
    save_path = 'weibo_data_' + keyword + '.txt'

    if types == '':
        types = '0'
    if contains == '':
        contains = '0'
    if interval == '':
        interval = 2
    else:
        interval = int(interval)
    if start_time == '':
        start_time = '2016-11-01-00'
    if end_time == '':
        end_time = '2016-11-30-23'

    sd = searchData.SearchData(keyword, region, start_time, end_time, types, contains)
    cd = collectData.CollectData(save_path)

    while cd.is_continue:
        is_finish = sd.set_next_timescope(interval)  # 设置每次搜索的时间范围，并判断是否已经搜索至结束时间
        if is_finish:
            break
        timescope = sd.get_timescope()
        print(timescope)
        logger.info(timescope)
        url = sd.generate_url()  # 根据指定的微博搜索信息生成url
        cd.download(url)

    print("the end!!!")

    # 结束爬取日志记录
    logger.removeHandler(filehandler)


if __name__ == '__main__':
    username = 'dm15506923661@sina.cn'
    password = 'WYYwyywyy'
    login.WeiboLogin.login(login.WeiboLogin(username, password))
    main()
