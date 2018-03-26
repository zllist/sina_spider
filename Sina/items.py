# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #大类的标题跟URL
    parentTitle = scrapy.Field()
    parentUrls  = scrapy.Field()

    #小类的标题 跟 url

    subTitle    = scrapy.Field()
    subUrls     = scrapy.Field()

    #小类目录储存路径
    subFilename = scrapy.Field()
    subUrls     = scrapy.Field()

    #小类下的自链接
    sonUrls = scrapy.Field()
    content = scrapy.Field()
    head    = scrapy.Field()



