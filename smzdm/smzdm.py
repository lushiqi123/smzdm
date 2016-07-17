# -*- coding = utf-8 -*-

import os
import sys
import datetime
import random

import requests
from lxml import etree
import pymongo
import yaml

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def get_config(path):
    """导入yaml配置文件"""
    with open(path, 'r') as fp:
        f = yaml.load(fp)
    return f


class Smzdm(object):
    def __init__(self):
        self.dir_root = os.path.dirname(os.path.abspath(__file__))
        conf_path = os.path.join(self.dir_root, 'conf.yaml')
        self.conf = get_config(conf_path)
        self.url = self.conf['URL']
        self.headers = self.conf['HEADERS']
        self.session = requests.Session()
        self.page_mark = str()
        self.use_agent_list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 '
            '(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
            'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 '
            '(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 '
            '(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 '
            '(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 '
            '(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 '
            '(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5']

    def creat_headers(self, refer):
        # 获取多页内容时的请求头
        headers = {'Refer': str(refer), 'User-Agent': str(random.choice(self.use_agent_list))}
        return headers

    def login(self):
        pass

    def get_response(self):
        res = requests.get(self.url, headers=self.headers)
        if res.status_code == requests.codes.ok:
            return res
        else:
            print('get response false')

    def parse(self, response):
        # 解析网页
        html = etree.HTML(response.content)
        item_list = html.xpath('//h3[@class="itemName"]//text()')
        title_list = [item_list[i] for i in range(0, 40, 2)]
        price_list = [item_list[i] for i in range(1, 40, 2)]
        info_list = ''.join(html.xpath('//div[@class="lrInfo"]//text()')).split('\n')
        timesort_list = html.xpath('//@timesort')
        self.page_mark = timesort_list[-1]
        datas = []
        for i in range(20):
            data = {'_id': str(timesort_list[i]),
                    'creattime': str(datetime.datetime.now()),
                    'item': {'title': title_list[i],
                             'price': price_list[i],
                             'info': info_list[i]
                             }
                    }
            datas.append(data)
        return datas

    def save_datas(self, datas):
        try:
            client = pymongo.MongoClient()
            coll = client['SmzdmDB']['haitao']

        except Exception as e:
            print(e)

        else:
            for data in datas:
                coll.insert_one(data)
            client.close()

    def data_more(self, headers):
        # 分页是动态加载到,需要抓包,响应是json格式的数据
        url = self.url + '/?json_more?timesort=' + self.page_mark
        print(url)
        json_more = requests.get(url, headers=headers)
        item_list = json_more.json()
        datas = []
        for item in item_list:
            data = {'id': item['article_timesort'],
                    'creattime': str(datetime.datetime.now()),
                    'item': {'title': item['article_title'],
                             'price': item['article_price'],
                             'indo': item['article_content']
                             }
                    }
            datas.append(data)
        return datas

if __name__ == '__main__':
    smzdm = Smzdm()
    r = smzdm.get_response()
    smzdm.save_datas(smzdm.parse(r))
