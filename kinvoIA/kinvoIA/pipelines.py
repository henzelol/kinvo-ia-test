# -*- coding: utf-8 -*-
import json


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class KinvoiaPipeline(object):
    def process_item(self, item, spider):       
        if item['titulo'] == None or item['titulo'] == 'null':
            return item
        if item['noticiadata'] == None or item['noticiadata'] == 'null':
            return item
        linha =  json.dumps(dict(item), ensure_ascii=False, indent=4)
        self.file.write(linha)
        return item

    def open_spider(self, spider):
        self.file = open('noticias.txt', 'w')

    def close_spider(self, spider):
        self.file.close()
