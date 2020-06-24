# -*- coding: utf-8 -*-

import urllib
import urllib2
import cookielib
import base64
import re
import rsa
import binascii


# post登录请求所需数据
postdata = {
    'entry': 'weibo',
    'gateway': '1',
    'from': '',
    'savestate': '7',
    'userticket': '1',
    'ssosimplelogin': '1',
    'vsnf': '1',
    'vsnval': '',
    'su': '',
    'service': 'miniblog',
    'servertime': '',
    'nonce': '',
    'pwencode': 'rsa2',  # 加密算法
    'sp': '',
    'encoding': 'UTF-8',
    'prelt': '401',
    'rsakv': '',
    'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
    'returntype': 'META'
    }

# 为网页下载器安装httpCookie写入功能和httpURL打开功能
cj = cookielib.LWPCookieJar()  # python中管理cookie的工具
cookie_support = urllib2.HTTPCookieProcessor(cj)  # 登录成功后自动绑定Cookies，并且在每次访问后携带该信息
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  # 设置HTTPHandler用于处理http的URL的打开
urllib2.install_opener(opener)


class WeiboLogin:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __get_spwd(self):
        rsa_public_key = int(self.pubkey, 16)
        key = rsa.PublicKey(rsa_public_key, 65537)  # 创建公钥
        message = self.servertime + '\t' + self.nonce + '\n' + self.password  # 拼接字段用于加密，前两者通过GET请求得到
        password = rsa.encrypt(message, key)  # 使用公钥加密密码信息
        password = binascii.b2a_hex(password)  # 将加密信息转换为16进制
        return password

    def __get_suser(self):
        username = urllib.quote(self.username)  # 对与URL格式冲突的字符进行编码
        username = base64.encodestring(username)[:-1]  # 使用base64编码微博账号，保证非ASCII字符的完整性
        return username

    def __prelogin(self):
        prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&client=ssologin.js(v1.4.4)' % self.username
        response = urllib2.urlopen(prelogin_url)  # 返回的数据是一个json字符串
        data = eval(re.findall(r'[^()]+', response.read())[1])  # 将字符串str当成有效的表达式来求值
        self.pubkey = str(data['pubkey'])
        self.servertime = str(data['servertime'])  # 这些为随机字段
        self.nonce = str(data['nonce'])
        self.rsakv = str(data['rsakv'])

    def login(self):
        url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'

        try:
            self.__prelogin()  # 预登录
        except:
            print('Prelogin Error!')
            return

        # 创建并完善post请求所需的数据
        global postdata
        postdata['servertime'] = self.servertime
        postdata['nonce'] = self.nonce
        postdata['su'] = self.__get_suser()
        postdata['sp'] = self.__get_spwd()
        postdata['rsakv'] = self.rsakv
        postdata = urllib.urlencode(postdata)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:37.0) Gecko/20100101 Firefox/37.0'}

        req = urllib2.Request(
                  url=url,
                  data=postdata,
                  headers=headers)

        result = urllib2.urlopen(req)
        text = result.read()
        data = re.search(r'location\.replace(.*)', text).group()  # 寻找location.replace及其后面的所有字符

        try:
            login_url = re.findall(r'[^\']+', data)[1]  # 寻找不包含'的字符串，此操作可取出''内的字符串
            urllib2.urlopen(login_url)
            print('Login Succeed!')
        except:
            print('Login Error!')
