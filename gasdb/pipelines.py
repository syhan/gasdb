# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import requests
import json

class CoordinatePipeline(object):
    BAIDU_AK = 'YkORmXGyF7U2ySjRGLh5lVq3UpycNRIH'
    #BAIDU_MAP_URL = 'http://api.map.baidu.com/geocoder/v2/?output=json&ak=YkORmXGyF7U2ySjRGLh5lVq3UpycNRIH&address={}'
    BAIDU_MAP_URL = 'http://api.map.baidu.com/cloudgc/v1?output=json&ak={}&address={}'

    def process_item(self, item, spider):
        resp = requests.get(self.BAIDU_MAP_URL.format(self.BAIDU_AK, item['address']))

        if resp.ok:
            j = json.loads(resp.text)
            result = j['result']

            if not result:
                item['coordinate'] = result['location']
                item['address_components'] = result['address_components']


        return item

class JsonWritterPipeline(object):
    def open_spider(self, spider):
        self.file = open(spider.name + '.json', 'wb')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False).encode('utf8') + b"\n"
        self.file.write(line)
        return item