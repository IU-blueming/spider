# -*- coding: utf-8 -*-
import scrapy
from imgsPro.items import ImgsproItem

class ImgSpider(scrapy.Spider):

    name = 'img'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['http://sc.chinaz.com/tupian/']

    def parse(self, response):
        #显示请求头信息
        print(response.request.headers)

        div_list = response.xpath('//div[@id="container"]/div')
        for div in div_list:
            #注意：使用伪属性
            src = div.xpath('./div/a/img/@src2').extract_first()
            name = div.xpath('./div/a/img/@alt').extract_first()

            item = ImgsproItem()
            item['src'] = src
            item['name'] = name

            yield item
