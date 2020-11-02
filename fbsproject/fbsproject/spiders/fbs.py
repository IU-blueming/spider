import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from fbsproject.items import FbsprojectItem
from scrapy_redis.spiders import RedisCrawlSpider


class FbsSpider(RedisCrawlSpider):
    name = 'fbs'
    # allowed_domains = ['www.xxx.com']
    # 分布式爬虫 起始的url要注释掉
    #start_urls = ['http://www.4567kan.com/movie/index40429.html']
    # 定义一个可以被共享的调度器队列的名称
    redis_key = 'movie'
    # 链接提取器
    # http://www.4567kan.com/movie/index40429.html
    link = LinkExtractor(allow=r'http://www\.4567kan\.com/movie/index\d+\.html')
    # 规则解析器
    rules = (
        Rule(link, callback='parse_item', follow=False),
    )
    def parse_item(self, response):
        # 电影名称
        name = response.xpath('/html/body/div[1]/div/div/div/div[2]/h1/text()').extract_first()
        # 电影描述，简介
        desc = response.xpath('/html/body/div[1]/div/div/div/div[2]/p[5]/span[2]//text()').extract()
        desc = ''.join(desc)
        # 把数据封装到item
        item = FbsprojectItem()
        item['name'] = name
        item['desc'] = desc
        print(item)
        yield item
