# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals

import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class SinaPipeline(object):
    def process_item(self, item, spider):
        sonUrls = item['sonUrls']

        filename = sonUrls[7:-6].replace('/','-')
        filename += 'txt'

        fp = open(item['subFilename'] + '/' + filename,'w')
        fp.write(item['content'])
        fp.close()

        return item
