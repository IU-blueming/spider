import scrapy

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from net163project.items import Net163ProjectItem
class NewsSpider(scrapy.Spider):
    def __init__(self):
        self.module_urls = []  #用于存放的网易新闻5大板块相应的url
        #实例化一个无头浏览器，且规避检测
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        #规避检测
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.browse = webdriver.Chrome(executable_path='chromedriver.exe',options=chrome_options)
    name = 'news'
    start_urls = ['https://news.163.com/']

    def parse(self, response):
        # print(response.text)
        module_indexes=[3,4,6,7,8]   #索引
        li_list = response.xpath('//*[@id="index2016_wrap"]/div[1]/div[2]/div[2]/div[2]/div[2]/div/ul/li')
        for index in module_indexes:
            module_url = li_list[index].xpath('./a/@href').extract_first()
            self.module_urls.append(module_url)
        # print(self.module_urls)
        #依次对每一个模块对应的页面发起请求
        for url in self.module_urls:
            yield scrapy.Request(url,callback=self.parse_module,dont_filter=True)

    def parse_module(self,response):
        div_list = response.xpath('//div[@class="ndi_main"]/div')
        for div in div_list:
            #新闻标题
            title = div.xpath('./div/div[1]/h3/a/text()').extract_first()
            #某条新闻的详细的url
            content_url = div.xpath('./div/div[1]/h3/a/@href').extract_first()

            item = Net163ProjectItem()
            item['title'] = title
            if title is not None:
                yield scrapy.Request(url=content_url,callback=self.parse_detail,meta={"item":item})

    #解析新闻详情页面的函数
    def parse_detail(self,response):
        content = response.xpath('//*[@id="content"]//text()').extract() or response.xpath('//*[@id="endText"]//text()').extract()
        content = ''.join(content)

        item = response.meta['item']
        item['content'] = content

        url = response.request.url
        item['url'] = url

        # print(f"url:{response.request.url}, title:{item['title']},  content:{item['content']},'\n\n'")

        #把item数据持久化
        yield item