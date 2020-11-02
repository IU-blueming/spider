# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# class Net163ProjectPipeline:
#     fp = None
#     def open_spider(self,spider):
#         print('开始爬虫......')
#         self.fp = open('./wangyi.txt','w',encoding='utf-8')
#
#     def process_item(self, item, spider):
#         title = item['title']
#         content = item['content']
#         url = item['url']
#         self.fp.write('网址：'+url+'\n'  +'标题：'+title+"\n"  +'内容'+content+'\n\n')
#         return item
#
#     def close_spider(self,spider):
#         print('爬虫结束')
#         self.fp.close()


from pymongo.mongo_client import MongoClient
class MongoDBPipeline(object):
    def open_spider(self, spider):
        self.client = MongoClient("localhost",27017)

    def process_item(self, item, spider):
        title = item['title']
        content = item['content']
        url = item['url']
        dict1 = {
            "url":url,
            "title":title,
            "content":content
        }
        self.client['wangyi']['news'].save(dict1)
        return item

    def close_spider(self, spider):
        self.client.close()


# import pymysql
# class mysqlPileLine(object):
#     def __init__(self):
#         print("mysqlPileLine管道对象初始化...")
#         self.cursor = None
#         self.db = None
#
#     def open_spider(self,spider):
#         self.db = pymysql.Connect(host='127.0.0.1',port=3306,user='root',password='1234',db='qiubai',charset='utf8')
#
#     def process_item(self,item,spider):
#         self.cursor = self.db.cursor()
#
#         try:
#             self.cursor.execute('insert into tb_qiubai(title,content) values("%s","%s")'%(item["title"],item["content"]))
#             self.db.commit()
#         except Exception as e:
#             print(e)
#             self.db.rollback()
#         return item
#
#     def close_spider(self,spider):
#         print("mysqlPileLine管道对象销毁...")
#         self.cursor.close()
#         self.db.close()