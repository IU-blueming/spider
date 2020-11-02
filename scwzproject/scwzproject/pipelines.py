# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymysql
from scwzproject.items import ScwzprojectItem,DetailItem
class ScwzprojectPipeline:
    def open_spider(self,spider):
        print("开启爬虫时执行...")
        #创建连接对象
        self.conn = pymysql.Connect(host='127.0.0.1', port=3306, database='wz_db', user='root', password='1234',charset='utf8')
        # 通过连接对象创建游标
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if isinstance(item,ScwzprojectItem):
            try:
                #插入操作
                sql_str = 'insert into tb_wz(title,url,date) values("%s","%s","%s")' % (item['title'], item['url'], item['date'])
                self.cursor.execute(sql_str)
                self.conn.commit() #提交事务
            except Exception as e:
                print(e)
                self.conn.rollback() #回滚事务
            return item
        if isinstance(item,DetailItem):
            try:
                #更新操作
                sql_str = 'update tb_wz set content="%s" where url="%s"' % (item['content'], item['url'])
                self.cursor.execute(sql_str)
                self.conn.commit()  # 提交事务
            except Exception as e:
                print(e)
                self.conn.rollback()  # 回滚事务
            return item
        return item

    # def close_spider(self):
    #     print("关闭爬虫时执行...")
    #     self.cursor.close()
    #     self.conn.close()