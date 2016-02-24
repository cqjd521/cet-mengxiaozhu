#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'se4'

import requests
import json
import config


def get_accesstoken(appid,appsecret):
    address = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (appid,appsecret)
    resp = requests.get(address).content.decode('utf-8')
    resp = json.loads(resp)
    return resp['access_token']

def sendtxtmessage(accesstoken,openid,content):
    url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=' + accesstoken
    info = {"touser":"OPENID","msgtype":"text","text":{"content":"HelloWorld"}}
    info['touser'] = openid
    data = json.dumps(info).replace('HelloWorld',content).encode('utf-8') #请主动decode content 到UTF8
    return requests.post(url,data).content.decode('utf-8')

def sendtemplate(accesstoken,openid):
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + accesstoken
    info = {"touser":"OPENID","template_id":"templateid","url":"url00","data":{"first":{"value":"first00","color":"#173177"},"keyword1":{"value":"keyword11","color":"#173177"},"keyword2":{"value":"keyword22","color":"#173177"},"keyword3":{"value":"keyword33","color":"#173177"},"keyword4":{"value":"keyword44","color":"#173177"},"remark":{"value":"remark55","color":"#173177"}}}
    info['touser'] = openid
    info['template_id'] = config.templateid
    info['url'] = config.templateurl
    info['data']['first']['value'] = config.templatefirst
    info['data']['keyword1']['value'] = config.templatekeyword1
    info['data']['keyword2']['value'] = config.templatekeyword2
    info['data']['keyword3']['value'] = config.templatekeyword3
    info['data']['keyword4']['value'] = config.templatekeyword4
    info['data']['remark']['value'] = config.templateremark
    data = json.dumps(info) #请主动decode content 到UTF8
    return requests.post(url,data).content.decode('utf-8')

def debug(resp):
    resp2 = json.loads(resp)
    recode = resp2['errcode']
    if recode == 0 :
        return '客服接口：发送成功'
    elif recode == 45015:
        return '客服接口：发送失败,客户没有在48h内与公众号互动'
    elif recode == 40003:
        return 'json数据组装有误'
    else:
        return '发生了其他的错误'

def get_openidlist(accesstoken):
    address = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s' % accesstoken
    address2 = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=NEXT_OPENID%d'
    resp = requests.get(address).content.decode('utf-8')
    resp = json.loads(resp)
    time = resp['total'] // resp['count']
    resp = resp['data']['openid']
    if time != 1:
        a = 0
        while a < time:
            a = a + 1
            resp2 = requests.get(address2 % (accesstoken,a)).content.decode('utf-8')
            resp2 = resp2['data']['openid']
            resp = list(set(resp).union(set(resp2)))
        return resp
    else:
        return resp

#accesstoken = get_accesstoken(config.appid,config.appsecret)
#resp = sendtxtmessage(accesstoken,'oYAtGw3BJuiBXcwUcJQIDf2iMWpo',u'测试客服接口')
