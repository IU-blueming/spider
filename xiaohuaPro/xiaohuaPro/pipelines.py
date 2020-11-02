# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class XiaohuaproPipeline:
    fp = None
    # 重写父类的一个方法：该方法只在开始爬虫的时候被调用一次
    def open_spider(self,spider):
        print('开始爬虫......')
        self.fp = open('./tu','w',encoding='utf-8')

    #专门用来处理item类型对象的
    #该方法可以接收爬虫文件传过来的item对象
    #该方法每接收一个item就会被调用一次
    def process_item(self, item, spider):
        src = item['src']
        self.fp.write(src)
        return item

    def close_spider(self,spider):
        print('结束爬虫！')
        self.fp.close()
