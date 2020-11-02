# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class ImgsproPipeline(object):
#     def process_item(self, item, spider):
#         return item


from scrapy.pipelines.images import ImagesPipeline
import scrapy

#定义一个基于ImagesPipeline的一个管道类，专门用于处理图片请求
class imgsPileLine(ImagesPipeline):
    #返回图片的Request请求
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['src'])

    #返回图片文件名
    def file_path(self, request, response=None, info=None, *, item=None):
        # imgName = request.url.split('/')[-1]
        return item['name']+'.jpg'

    #当item处理完毕后，返回给下一个即将被执行的管道类
    def item_completed(self, results, item, info):
        return item




