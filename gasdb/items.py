# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose


class Gas(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    chargeable = scrapy.Field()
    phone = scrapy.Field()
    coordinate = scrapy.Field()
    province = scrapy.Field()
    address_components = scrapy.Field()

class GasLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(lambda x: x.strip())
    chargeable_in = MapCompose(lambda x: True if x.strip() == '是' else False)