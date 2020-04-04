# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
from scrapy.exceptions import DropItem


class PttarticlelistPipeline(object):
	def open_spider(self, spider):
		self.conn = sqlite3.connect('./database/beauty.sqlite')
		self.cur = self.conn.cursor()
		# setting column url to be primary key
		self.cur.execute('''create table if not exists beauty_tb(
                            nrec text,
                            title text,
                            author text,
                            date text,
                            url text primary key
                            )''')
                
	def close_spider(self, spider):
		self.conn.commit()
		self.conn.close()

	def process_item(self, item, spider):
		# use upsert method, check if the url is already in the table or not, yes:update column nrec; no:insert data
		self.cur.execute("insert into beauty_tb (nrec, title, author, date, url) values(?,?,?,?,?) on conflict(url) do update set nrec=excluded.nrec",(
					item['nrec'],
					item['title'],
					item['author'],
					item['date'],
					item['url']
					))
		return item



class DropItemPipeline(object):
    def process_item(self, item, spider):
        if item['title']:
            return item
        else:
            raise DropItem('Article was deleted')