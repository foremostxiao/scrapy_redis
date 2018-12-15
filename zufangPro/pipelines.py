# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ZufangproPipeline(object):
    def __init__(self):
        self.fp = None

    def open_spider(self, spider):
        print('开始爬虫')
        self.fp = open('./data.txt', 'w',encoding='utf-8')

    def process_item(self, item, spider):
        title = item['title']
        room = item['room']
        zone = item['zone']
        address = item['address']
        money = item['money']
        type = item['type']
        detail = title+'\n'+room+'\n'+zone+'\n'+address+'\n'+money+'\n'+type+'\n'
        print(detail)
        # 将爬虫文件提交的item写入文件进行持久化存储
        self.fp.write(detail)
        return item

    def close_spider(self, spider):
        print('结束爬虫')
        self.fp.close()
