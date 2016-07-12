import requests
from lxml import etree
from pymongo import MongoClient
import sys
import os
import yaml

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class SmzdmC(object):
    # 抓取什么值得买网站海淘专区信息

    def __init__(self):
        """

        :rtype: ready
        """
        self.fname_dir = os.path.dirname(os.path.abspath(__file__))
        fname_conf = os.path.join(self.fname_dir, 'settings.yaml')
        self.config = yaml.load(fname_conf)
        self.session = requests.Session()
        self.headers = self.config['URL']['HOMEPAGE']
        self.url = self.config['URL']
        self.datas = []
        self.response = requests.Response
        self.data = {'item': '', 'price': '', 'info': ''}

    def get_response(self):
        self.response = requests.get(self.url, headers=self.headers)
        print(self.response.status_code)
        return self.response

    def parse_response(self,response):
        """res --chuan ru yi ge requests.response object"""
        cont = etree.HTML(response.content)
        item = cont.xpath('//h3[@class="itemName"]//text()')
        price = [item.pop(n) for n in range(1, 21)]
        info_all = cont.xpath('//div[@class="lrInfo"]//text()')
        info_str = ''.join(info_all)
        info = info_str.split('\n')
        for i in range(len(item)):
            self.data['item'] = item[i]
            self.data['price'] = price[i]
            self.data['info'] = info[i]
            self.datas.append(self.data)
        return self.datas

    def dump_datas(self):
        client = MongoClient()
        db = client['SmzdmDB']
        coll = db['haitao']
        coll.insert_many(self.datas)
        client.close()

if __name__ == '__main__':
    smzdmc = SmzdmC()
    res = smzdmc.get_response()
    smzdmc.parse_response(res)
    smzdmc.dump_datas()
