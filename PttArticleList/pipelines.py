# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
from scrapy.exceptions import DropItem


# 將資料存入資料庫
class PttarticlelistPipeline(object):
	def open_spider(self, spider):
		self.conn = sqlite3.connect('./database/beauty.sqlite')
		self.cur = self.conn.cursor()
		self.cur.execute('''create table if not exists beauty_tb(
                            nrec varchar(100),
                            title varchar(100),
                            author varchar(100),
                            day varchar(100),
                            href varchar(500)
                            )''')
                
	def close_spider(self, spider):
		self.conn.commit()
		self.conn.close()

	def process_item(self, item, spider):
		col = ','.join(item.keys())
		placeholder = ','.join(len(item) * '?')
		sql = 'insert into beauty_tb({}) values({})'
		self.cur.execute("insert into beauty_tb values(?,?,?,?,?)",(
							item['nrec'],
							item['title'],
							item['author'],
							item['day'],
							item['href']
		))
		return item



# 移除已被刪除的文章
class DropItemPipeline(object):
    def process_item(self, item, spider):
        if item['title']:
            return item
        else:
            raise DropItem('Article was deleted')