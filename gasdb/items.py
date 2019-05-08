# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Gas(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    chargeable = scrapy.Field()
    phone = scrapy.Field()
