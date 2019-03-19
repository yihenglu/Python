#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#功能：通过框架，从移动端网址爬取特定公众号（如“987路况”）所发表的文章
#Request URL:https://m.weibo.cn/api/container/getIndex?containerid=2304132171172280_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page=2
#对应视频教程：https://www.bilibili.com/video/av40538761?from=search&seid=8881669598828363105
import time

import requests
import pprint
import json
from urllib.parse import urlencode
from pyquery import PyQuery  #获取一段符号（如整个网页的源码）中的中文
base_url = 'https://m.weibo.cn/api/container/getIndex?'  #网址的固定前缀

#根据页数获取数据
def get_page(page,containerid):  #containerid是字符串的形式，如'2304132171172280'
        parames = {
            'containerid':containerid,
            'page_type':'03',
            'page':page
        }
        # print(base_url + urlencode(parames))  #完整网址
        reponse = requests.get(base_url + urlencode(parames))  #获取请求的返回结果
        if reponse.status_code == 200 :  #若返回的状态码不是200，如为418，则返回None
            # print(reponse)
            # pprint.pprint(reponse.json())  #网页html格式源码
            return reponse.json()
        else:
            print("跳过 ",reponse.status_code)
            return None


#解析数据
def parse_data(res_json):
    for item in res_json['data']['cards']:
        try:  #此处也可以更改为if条件语句，如if item['mblog']['raw_text'] :
            # print(item)
            result = dict()  #还可以增加更多的信息
            result['text'] = PyQuery(item['mblog']['text']).text()  #某一条微博的文本内容
            # result['created_at'] = item['mblog']['created_at']  #某一条微博的创建时间
            # print(result['created_at'],result['raw_text'])
            with open('weibo_traffic_987lukuang_info.txt','a+',encoding='utf-8') as f:  #以追加的方式写文件，不会覆盖原来的
                # f.write(result['created_at'] + ' ' + result['raw_text'] + '\n')
                f.write(result['text'] + '\n')
                # f.write(json.dumps(result))  #将结果写成json格式，也可以选择保存为json
        except:
            None

    return

def main():
    get_num = 0
    total_page = 200  #需要爬取的微博页数
    containerid = '2304132171172280'  #用户id，根据请求的网址可以观察出来，该id为“987路况信息”
    for page in range(0,total_page):
        res_json = get_page(page,containerid)
        if res_json != None:
            parse_data(res_json)
            get_num += 1
        else:
            time.sleep(30)
    print('共爬取' + str(get_num) + '页微博')
    return

if __name__ == '__main__':
    main()

