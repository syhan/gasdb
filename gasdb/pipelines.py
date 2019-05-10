# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import requests
import json
import pymongo

class CoordinatePipeline(object):
    
    BAIDU_CLOUDGC_URL = 'http://api.map.baidu.com/cloudgc/v1?output=json&ak={}&address={}'
    BAIDU_GENCODER_URL = 'http://api.map.baidu.com/geocoder/v2/?output=json&ak={}&address={}'

    def __init__(self, baidu_ak):
        self.baidu_ak = baidu_ak

    @classmethod
    def from_crawler(cls, crawler):
        return cls(baidu_ak = crawler.settings.get('BAIDU_AK'))

    def process_item(self, item, spider):
        resp = requests.get(self.BAIDU_CLOUDGC_URL.format(self.baidu_ak, item['address']))
        result = {}

        if resp.ok:
            j = json.loads(resp.text)

            if j.status == 302: # exceed quota
                # try gencoder
                resp = requests.get(self.BAIDU_GENCODER_URL.format(self.baidu_ak, item['address']))
                if resp.ok:
                    j = json.loads(resp.text)
                    result = j['result']
                    item['coordinate'] = result['location']
            else:
                result = j['result'][0]
            
                item['coordinate'] = result['location']
                item['address_components'] = result['address_components']

        return item


class JsonWritterPipeline(object):
    def open_spider(self, spider):
        self.file = open(spider.name + '.jl', 'wb')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False).encode('utf8') + b'\n'
        self.file.write(line)
        return item


class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DATABASE', 'gas')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[spider.name].insert_one(dict(item))
        return item