# -*- coding: utf-8 -*-
import scrapy
from gasdb.items import Gas, GasLoader

class SinopecSpider(scrapy.Spider):
    name = 'sinopec'
    allowed_domains = ['www.sinopecsales.com']
    current_page = 1
    query_url = 'http://www.sinopecsales.com/website/gasStationAction_queryGasStationByCondition.action'
    formdata = {'stationCharge': '2', 'page.pageNo': str(current_page)}
    provinces = iter([11, 91, 12, 13, 41, 14, 15, 21, 22, 23, 31, 32, 33, 34, 35, 36, 37, 42, 43, 44, 45, 46, 50, 51, 52, 53, 54, 61, 62, 63, 64, 65])

    def start_requests(self):
        self.formdata['province'] = str(next(self.provinces))
        yield scrapy.FormRequest(url=self.query_url, formdata=self.formdata, callback=self.parse)

    def parse(self, response):
        rows = response.xpath('//tr[@height="35px"]')

        for row in rows:
            l = GasLoader(item=Gas(), selector=row)

            l.add_xpath('id', 'td[1]/text()')
            l.add_xpath('name', 'td[2]/text()')
            l.add_xpath('address', 'td[3]/text()')
            l.add_xpath('chargeable', 'td[4]/text()')
            l.add_xpath('phone',  'td[5]/text()')
            l.add_value('province', self.formdata['province'])
            
            yield l.load_item()

        next_page =  response.xpath('//td[a="下一页"]').get()
        if next_page is not None:
            self.current_page = self.current_page + 1
            self.formdata['page.pageNo'] = str(self.current_page)

            yield scrapy.FormRequest(url=self.query_url, formdata=self.formdata, callback=self.parse)
        else:
            next_province = next(self.provinces, None)

            if next_province is not None:
                self.current_page = 1
                self.formdata['page.pageNo'] = str(self.current_page)
                self.formdata['province'] = str(next_province)

                yield scrapy.FormRequest(url=self.query_url, formdata=self.formdata, callback=self.parse)
            


