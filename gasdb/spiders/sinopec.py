# -*- coding: utf-8 -*-
import scrapy


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
        table = response.xpath('//*[@id="form"]/div[2]/div[1]/table/tbody')
        rows = table.xpath('//tr')[2:-1] # remove the header and footer 

        for row in rows:
            yield {
                'id': row.xpath('td//text()')[0].get().strip(),
                'name': row.xpath('td//text()')[1].get().strip(),
                'address': row.xpath('td//text()')[2].get().strip(),
                'chargeable': row.xpath('td//text()')[3].get().strip(),
                'phone': row.xpath('td//text()')[4].get().strip()
            }

        next_page = response.xpath('//*[@id="form"]/div[2]/div[2]/table/tbody/tr/td[3]/a[1]').get()
        if next_page is not None:
            self.current_page = self.current_page + 1
            self.formdata['page.pageNo'] = str(self.current_page)

            yield scrapy.FormRequest(url=self.query_url, formdata=self.formdata, callback=self.parse)


