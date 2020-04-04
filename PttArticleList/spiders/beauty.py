# -*- coding: utf-8 -*-
import scrapy
from ..items import PttarticlelistItem


class BeautySpider(scrapy.Spider):
    name = 'beauty'
    allowed_domains = ['ptt.cc']
    start_urls = ['https://www.ptt.cc/bbs/Beauty/index.html']

    count = 0
    count_max = 3   # max pages to crawl

    def parse(self, response):
        href = 'https://www.ptt.cc/bbs/Beauty/index.html'
        yield scrapy.Request(url=href, cookies={'over18': '1'}, callback=self.parse_list)    # add cookies to pass age verification

    def parse_list(self, response):
        # get list of all articles on current page
        for quote in response.css('div.r-ent'):
            beauty_item = PttarticlelistItem()
            beauty_item['nrec'] = quote.css('div.nrec span::text').get()                                    # number of push
            beauty_item['title'] = quote.css('div.title a::text').get()                                     # title of the article 
            beauty_item['author'] = quote.css('div.meta div.author::text').get()                            # author of the article
            beauty_item['date'] = quote.css('div.meta div.date::text').get()                                # date
            beauty_item['url'] = 'https://www.ptt.cc' + str(quote.css('div.title a::attr(href)').get())     # url of athe article

            yield beauty_item
        
        # get URL of next page
        previous_page = response.xpath('//*[@id="action-bar-container"]/div/div[2]/a[2]/@href').get()
        self.count += 1
        # should keep get URL of next page or not
        if self.count < self.count_max:
            if previous_page is not None:
                previous_page = response.urljoin(previous_page)
                yield scrapy.Request(previous_page, callback=self.parse_list)

