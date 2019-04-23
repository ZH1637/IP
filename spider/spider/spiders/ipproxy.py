# -*- coding: utf-8 -*-
import scrapy
from ..items import IpItem


class IpproxySpider(scrapy.Spider):
    name = 'ipproxy'
    allowed_domains = ['www.xicidaili.com']

    def start_requests(self):
        baseurl = 'https://www.xicidaili.com/'
        Type = {
            # '高匿': 'nn/',
            # '普通': 'nt/',
            'HTTPS': 'wn/',
            # 'HTTP': 'wt/'
        }
        # 追加四类基本url
        for d in Type:
            url = baseurl + Type[d]
            yield scrapy.Request(url, meta={'url_first': url}, callback=self.parse_add_page)

    def parse_add_page(self, response):
        # 追加不同页数的url
        pages = response.xpath('//div[@class="pagination"]//a')
        pagesize = int(pages[-2].xpath('./text()').extract()[0])
        for x in range(1, pagesize + 1, 1):
            url = response.meta['url_first'] + str(x)
            yield scrapy.Request(url, callback=self.parse_ip)

    def parse_ip(self, response):
        # 解析ip
        item = IpItem()
        ip_list = response.xpath('//tr')
        ip_list.pop(0)
        for ip in ip_list:
            ip = ip.xpath('./td//text()').extract()
            if len(ip) == 19:
                item['ip'] = ip[0]
                item['port'] = ip[1]
                item['address'] = ip[3]
                item['type'] = ip[6]
                yield item
