# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse


class Net163ProjectDownloaderMiddleware:


    def process_request(self, request, spider):

        return None

    #拦截 响应对象，该方法拦截的是5大板块的响应对象，进行篡改
    def process_response(self, request, response, spider):
        #挑选出指定的响应对象进行篡改
        if request.url in spider.module_urls:
            # print("该url拦截:",request.url)
            #使用selenium重新发起请求，获取动态加载的数据，浏览器
            #取得爬虫文件创建的无头浏览器对象
            browse = spider.browse
            #向五大板块的url发起请求，获取包含动态加载数据
            browse.get(request.url)
            page_text = browse.page_source
            new_response = HtmlResponse(url=request.url,body=page_text,
                                        encoding='utf-8',request=request)
            return new_response
        else:
            # print("该url不拦截:",request.url)
            return response

    def process_exception(self, request, exception, spider):

        pass


