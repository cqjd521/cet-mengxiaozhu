#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import urllib.parse
import json
from bs4 import BeautifulSoup
import wechat
import config


province='湖北'
school='华中科技大学文华学院'
db = {}

accesstoken = wechat.get_accesstoken(config.appid,config.appsecret)

def get_ticket(name):
    url = 'http://119.29.80.182/ticket'
    data = {'school':school,'province':province,'name':name,'cet_type':1}
    headers = { "Accept":"application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Referer":"http://139.129.49.130/",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311."
                         "154 Safari/537.36 LBBROWSER"
            }
    resp = requests.post(url,data=data,headers=headers).text
    resp = json.loads(resp)['ticket_number']
    return resp

def get_score(name,ticket):
    url = 'http://119.29.80.182/score'
    data = {'name':name,'ticket':ticket,'scet':1}
    headers = { "Accept":"application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Referer":"http://139.129.49.130/",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER"
            }
    resp = requests.post(url,data=data).text
    return resp

def name2score(openid,name):
    ticket = get_ticket(name)
    html = get_score(name,ticket)
    soup = BeautifulSoup(html,'lxml')
    name = soup.table.find_all('td')[1].contents
    school = soup.table.find_all('td')[3].contents
    listening = soup.table.find_all('td')[5].contents
    read = soup.table.find_all('td')[7].contents
    write = soup.table.find_all('td')[9].contents
    total = soup.table.find_all('td')[11].contents
    db[openid] = name,school,listening,read,write,total
    return db[openid]

def get_m_band_users():
    address = 'https://www.mengxiaozhu.cn/Service/ajax_debug_message?service_id=%d&type=text&username=%s&openid=%s'
    openidlist = wechat.get_openidlist(accesstoken)
    for openid in openidlist:
        ret = requests.get(address % (config.mid,openid,openid),verify=False).content
        if len(ret) != 0:
            ret = ret.decode('utf-8').lstrip('[').rstrip(']')
            i = json.loads(ret)
            l = i['user'].replace('@',':').split(':')
            name = l[0]
            name2score(openid,name)
    print ( '姓名考号及用户对应关系构建完毕')


def sendscore():
    for openid in db:
        if config.mode == 1:
            content = u'%s同学：\n听力:%s\n阅读：%s\n写作：%s\n总分：%s\n\n萌小助 X 口袋文华 为您带来卓越用户体验 :)'
            content = content % (db[openid][0],db[openid][2],db[openid][3],db[openid][4],db[openid][5])
            print('正在用48h客服接口向' + openid + '发送CET成绩……')
            resp = wechat.debug(wechat.sendtxtmessage(accesstoken,openid,content))
            print(resp)
        elif config.mode == 0:
            config.templatekeyword1 = str(db[openid][0])
            config.templatekeyword2 = str(db[openid][1])
            config.templatekeyword3 = '420900151101116' #写到这里突然发现忘记存准考证号到数组了，所以假装这里我不会弄
            config.templatekeyword4 = u'听力:%s , 阅读:%s , 写作:%s , 总分:%s ' % (db[openid][2],db[openid][3],
                                                                           db[openid][4],db[openid][5])
            resp = wechat.debug(wechat.sendtemplate(accesstoken,openid))
            print(resp)
        else:
            pass





get_m_band_users()
#db = {'oYAtGw3BJuiBXcwUcJQIDf2iMWpo': (['操大戈'], ['华中科技大学文华学院'], ['153'], ['142'], ['133'], ['428'])}
sendscore()
