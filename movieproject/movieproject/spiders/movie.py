import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from pymongo.mongo_client import MongoClient
from movieproject.items import MovieprojectItem

class MovieSpider(CrawlSpider):
    #初始化爬虫对象是调用该方法
    def __init__(self):
        #调用父类的方法
        super().__init__(self)
        #访问数据库，创建客户端对象
        self.client = MongoClient('localhost',27017)
        self.url_connection = self.client['moviedb']['urls']
    #销毁爬虫对象时，回调该方法
    def __del__(self):
        self.client.close()

    name = 'movie'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['http://www.4567kan.com/frim/index1.html']
    link_1 = LinkExtractor(allow=r'http://www\.4567kan\.com/frim/index1\.html')
    link = LinkExtractor(allow=r'http://www\.4567kan\.com/frim/index1-\d+\.html')

    rules = (
        Rule(link_1, callback='parse_item', follow=False),
        Rule(link, callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        # print(response.request.url)
        li_list = response.xpath('/html/body/div[1]/div/div/div/div[2]/ul/li')
        for li in li_list:
            self.detail_url = "http://www.4567kan.com"+li.xpath('./div/a/@href').extract_first()
            self.title = li.xpath('./div/a/@title').extract_first()
            # print('影名：'+self.title,'网址链接：'+self.detail_url)

            cursor = self.url_connection.find({'url':self.detail_url})
            if cursor.count() == 0:
                print('该%s没有被访问，可以进行数据的爬取...'%self.detail_url)
                self.url_connection.insert_one({"url":self.detail_url})
                #发起一个新的请求，访问该url的电影详情页面
                yield scrapy.Request(url=self.detail_url, callback=self.parse_detail)
            else:
                print("当前的%s已经访问过，无需访问"%self.detail_url)
    def parse_detail(self, response):
        item = MovieprojectItem()
        item['name'] = response.xpath('/html/body/div[1]/div/div/div/div[2]/h1/text()').extract_first()
        item['desc'] = response.xpath('/html/body/div[1]/div/div/div/div[2]/p[5]/span[2]//text()').extract()
        item['desc'] = ''.join(item['desc'])
        yield item