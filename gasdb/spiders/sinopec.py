# -*- coding: utf-8 -*-
import scrapy
from gasdb.items import Gas, GasLoader

class SinopecSpider(scrapy.Spider):
    name = 'sinopec'
    allowed_domains = ['www.sinopecsales.com']

    def __init__(self):
        self.current_page = 1
        self.query_url = 'http://www.sinopecsales.com/website/gasStationAction_queryGasStationByCondition.action'
        self.formdata = {'province': '31', 'stationCharge': '2', 'page.pageNo': str(self.current_page)}

    def start_requests(self):
        yield scrapy.FormRequest(url=self.query_url, formdata=self.formdata, callback=self.parse, dont_filter=True)

    def parse(self, response):
        rows = response.xpath('//tr[@height="35px"]')

        for row in rows:
            l = GasLoader(item=Gas(), selector=row)

            l.add_xpath('id', 'td[1]/text()')
            l.add_xpath('name', 'td[2]/text()')
            l.add_xpath('address', 'td[3]/text()')
            l.add_xpath('chargeable', 'td[4]/text()')
            l.add_xpath('phone',  'td[5]/text()')
            
            yield l.load_item()

        next_page = response.xpath('//*[@id="form"]/div[2]/div[2]/table/tbody/tr/td[3]/a[1]').get()
        if next_page is not None:
            self.current_page = self.current_page + 1
            self.formdata['page.pageNo'] = str(self.current_page)

            yield scrapy.FormRequest(url=self.query_url, formdata=self.formdata, callback=self.parse)


