import scrapy


# class MeinvSpider(scrapy.Spider):
#     name = 'xiaohua'
#     # allowed_domains = ['www.abc.com']
#     start_urls = ['http://www.521609.com/meinvxiaohua/']
#
#     # 基本url的模板
#     base_url = "http://www.521609.com/meinvxiaohua/list12%d.html"
#     page_num = 2
#
#     name_list = []
#     def parse(self, response):
#         # 数据解析
#         li_list = response.xpath('//div[@id="content"]/div[2]/div[2]/ul/li')
#         for li in li_list:
#             img_name = li.xpath('./a[2]//text()').extract_first()
#             self.name_list.append(img_name)
#         if self.page_num <= 11:
#             new_url = format(self.base_url % self.page_num)
#             self.page_num += 1
#             yield scrapy.Request(url=new_url, callback=self.parse, method='GET')
#
#         print(self.name_list)
#         print(len(self.name_list))

from xiaohuaPro.items import XiaohuaproItem

class MeinvSpider(scrapy.Spider):
    name = 'xiaohua'
    # allowed_domains = ['www.abc.com']
    start_urls = ['http://sc.chinaz.com/tupian/']

    def parse(self, response):
        div_list = response.xpath('//div[@id="container"]/div')
        for div in div_list:
            #注意：使用伪属性
            src = div.xpath('./div/a/img/@src2').extract_first()
            # print(src)
            item = XiaohuaproItem()
            item['src'] = src

            yield item