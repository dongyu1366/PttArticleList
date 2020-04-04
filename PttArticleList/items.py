# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PttarticlelistItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nrec = scrapy.Field()   # 推噓數
    title = scrapy.Field()
    author = scrapy.Field()
    day = scrapy.Field()
    url = scrapy.Field()
