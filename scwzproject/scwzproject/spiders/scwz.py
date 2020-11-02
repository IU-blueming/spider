import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scwzproject.items import ScwzprojectItem,DetailItem

class ScwzSpider(CrawlSpider):
    name = 'scwz'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://ly.scol.com.cn/welcome/showlist?keystr=wzrd']
    link = LinkExtractor(allow=r'&total=\d+&page=\d+')
    link_detail = LinkExtractor(allow=r'https://ly\.scol\.com\.cn/thread\?tid=\d+')
    """爬取规则选择器：将链接提取器提取到的链接进行指定规则
    LinkExtractor:链接提取器
    callback:回调的数据解析函数
    follow:可以将链接提取器继续作用到 链接提取器 提取到的链接所对应的页面中
    """
    rules = (
        Rule(link, callback='parse_item', follow=False),
        Rule(link_detail, callback='parse_detail',follow=False),
    )
    #解析全站页面的网页内容，提取提问消息的标题，日期，对应url
    def parse_item(self, response):
        a_list = response.xpath('//div[@id="d_1"]/a')
        for a in a_list:
            title = a.xpath('./text()').extract_first()
            url = a.xpath('./@href').extract_first()
            #找当前节点的兄弟节点 following-sibling::span[1]
            #获取当前节点之后的兄弟节点的第一个节点
            date = a.xpath('./following-sibling::span[1]/text()').extract_first()
            # print(title,date,url)
            item = ScwzprojectItem()
            item['title'] = title
            item['date'] = date
            item['url'] = url
            yield item

    def parse_detail(self,response):
        #详细内容
        url = response.request.url
        content = response.xpath('//div[@class="c1"]/p[2]//text()|//div[@class="c1"]/p[3]//text()').extract_first()
        # print(url,content)
        # print(content)
        item = DetailItem()
        item['url'] = url
        item['content'] = content
        yield item

