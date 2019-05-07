# -*- coding: utf-8 -*-
import scrapy


class SinopecSpider(scrapy.Spider):
    name = 'sinopec'
    allowed_domains = ['www.sinopecsales.com']
    start_urls = ['http://www.sinopecsales.com/website/gasStationAction_queryGasStationByCondition.action?province=31&stationCharge=2&page.pageNo=1',
    'http://www.sinopecsales.com/website/gasStationAction_queryGasStationByCondition.action?province=31&stationCharge=2&page.pageNo=2',
    'http://www.sinopecsales.com/website/gasStationAction_queryGasStationByCondition.action?province=31&stationCharge=2&page.pageNo=3',
    'http://www.sinopecsales.com/website/gasStationAction_queryGasStationByCondition.action?province=31&stationCharge=2&page.pageNo=4',
    'http://www.sinopecsales.com/website/gasStationAction_queryGasStationByCondition.action?province=31&stationCharge=2&page.pageNo=5',
    'http://www.sinopecsales.com/website/gasStationAction_queryGasStationByCondition.action?province=31&stationCharge=2&page.pageNo=6',
    'http://www.sinopecsales.com/website/gasStationAction_queryGasStationByCondition.action?province=31&stationCharge=2&page.pageNo=7',
    'http://www.sinopecsales.com/website/gasStationAction_queryGasStationByCondition.action?province=31&stationCharge=2&page.pageNo=8',
    'http://www.sinopecsales.com/website/gasStationAction_queryGasStationByCondition.action?province=31&stationCharge=2&page.pageNo=9',
    'http://www.sinopecsales.com/website/gasStationAction_queryGasStationByCondition.action?province=31&stationCharge=2&page.pageNo=10',
    'http://www.sinopecsales.com/website/gasStationAction_queryGasStationByCondition.action?province=31&stationCharge=2&page.pageNo=11',
    'http://www.sinopecsales.com/website/gasStationAction_queryGasStationByCondition.action?province=31&stationCharge=2&page.pageNo=12']

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
        # TODO: how to follow the link instead of put all pages ahead


