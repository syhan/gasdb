# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import requests
import json

class CoordinatePipeline(object):
    BAIDU_MAP_URL = 'http://api.map.baidu.com/geocoder/v2/?output=json&ak=YkORmXGyF7U2ySjRGLh5lVq3UpycNRIH&address={}'

    def process_item(self, item, spider):
        resp = requests.get(self.BAIDU_MAP_URL.format(item['address']))

        if resp.ok:
            j = json.loads(resp.text)
            item['coordinate'] = j['result']['location']


        return item
