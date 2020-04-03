# -*- coding: utf-8 -*-
import scrapy
from ..items import PttarticlelistItem


class BeautySpider(scrapy.Spider):
    name = 'beauty'
    allowed_domains = ['ptt.cc']
    start_urls = ['https://www.ptt.cc/bbs/Beauty/index.html']

    count = 0
    count_max = 5   # 調整要爬幾頁

    def parse(self, response):
        href = 'https://www.ptt.cc/bbs/Beauty/index.html'
        yield scrapy.Request(url=href, cookies={'over18': '1'}, callback=self.parse_list)    # 加入cookie，以通過年齡驗證

    def parse_list(self, response):
        # 獲取本頁所有文章的清單
        for quote in response.css('div.r-ent'):
            beauty_item = PttarticlelistItem()
            beauty_item['nrec'] = quote.css('div.nrec span::text').get()                                    # 推噓數
            beauty_item['title'] = quote.css('div.title a::text').get()                                     # 文章標題 
            beauty_item['author'] = quote.css('div.meta div.author::text').get()                            # 作者
            beauty_item['day'] = quote.css('div.meta div.date::text').get()                                 # 發文日期
            beauty_item['href'] = 'https://www.ptt.cc' + str(quote.css('div.title a::attr(href)').get())    # 頁面連結

            yield beauty_item
        
        # 獲取下一頁的URL
        previous_page = response.xpath('//*[@id="action-bar-container"]/div/div[2]/a[2]/@href').get()
        self.count += 1
        # 用來判斷是否爬完指定的頁數
        if self.count < self.count_max:
            if previous_page is not None:
                previous_page = response.urljoin(previous_page)
                yield scrapy.Request(previous_page, callback=self.parse_list)

