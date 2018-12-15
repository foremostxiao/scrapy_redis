# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from zufangPro.items import ZufangproItem
#CrawlSpider
class ZufangSpider(RedisCrawlSpider):
    name = 'zufang'
    #allowed_domains = ['https://www.bj.58.com']
    #start_urls = ['https://bj.58.com/chuzu/pn1']
    # 调度器队列的名称
    redis_key = 'zufang'  # 表示跟start_urls含义是一样

    #('https://bj.58.com/chuzu/pn2/')
    rules = (
        Rule(LinkExtractor(allow=r'https://bj.58.com/chuzu/pn\d+'), callback='parse_item', follow=True),
    )


    def parse_item(self, response):
        print(response)

        li_list = response.xpath('//ul[@class="listUl"]/li')
        for li in li_list:
            def all_detail(li, type):
                title = li.xpath('./div[@class="des"]/h2/a/text()').extract_first()
                room = li.xpath('./div[@class="des"]/p[@class="room"]/text()').extract_first()
                address = li.xpath('./div[@class="des"]/p[@class="add"]//text()').extract()
                address = ''.join(address)
                money = li.xpath('.//div[@class="money"]/b/text()').extract_first() + '元/月'
                item = ZufangproItem()
                item['title'] = title
                item['room'] = room
                item['address'] = address
                item['money'] = money
                item['type'] = type
                yield item

            if li.xpath('./div[@class="des"]/p[@class="gongyu"]'):
                print('公寓类型')
                type = li.xpath('./div[@class="des"]/p[@class="gongyu"]//text()').extract()
                type = ''.join(type)
                all_detail(li, type)

            if li.xpath('./div[@class="des"]/p[@class="geren"]'):
                print('个人房源')
                type = li.xpath('./div[@class="des"]/p[@class="green"]//text()').extract()
                type = ''.join(type)
                all_detail(li, type)

            if li.xpath('./div[@class="des"]/div[@class="jjr"]'):
                print('经纪人/安选房源')
                type = li.xpath('./div[@class="des"]/div[@class="jjr"]//text()').extract()
                type = ''.join(type)
                all_detail(li,type)


