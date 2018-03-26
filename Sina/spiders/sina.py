#-*- coding:utf-8 -*-

from Sina.items import SinaItem
import scrapy
import os
import sys

#重载模块 为了设置当前的编码格式
reload(sys)
sys.setdefaultencoding("utf-8")

class SinaSpider(scrapy.Spider):
    name = "sina"
    allow_domains = ["sina.com.cn"]
    start_urls = [
        "http://news.sina.com.cn/guide/",
    ]

    def parse(self,response):
        items = []
        
        #所有大类的url 跟 标题
        parentUrls = response.xpath('//div[@id=\"tab01\"]/div/h3/a/@href').extract()
        parentTitle  = response.xpath("//div[@id=\"tab01\"]/div/h3/a/text()").extract()

        #所有小类的url 和 标题
        subUrls  = response.xpath('//div[@id=\"tab01\"]/div/ul/li/a/@href').extract()
        subTitle = response.xpath('//div[@id=\"tab01\"]/div/ul/li/a/text()').extract()

        for i in range(0,len(parentTitle)):
            parentFilename = "./Data/" + parentTitle[i]

            #创建大类的目录 
            if(not os.path.exists(parentFilename)):
                os.makedirs(parentFilename)

            for j in range(0, len(subUrls)):
                item = SinaItem()

                item['parentTitle'] = parentTitle[i]
                item['parentUrls']  = parentUrls[i]

                #检测小类的url 是否属于大类
                if_belong = subUrls[j].startswith(item['parentUrls'])

                if(if_belong):
                    subFilename = parentFilename + '/' + subTitle[j]

                    if(not os.path.exists(subFilename)):
                        os.makedirs(subFilename)

                    item['subUrls'] = subUrls[j]
                    item['subTitle'] =subTitle[j]
                    item['subFilename'] = subFilename

                    items.append(item)

        for item in items:
            yield scrapy.Request( url = item['subUrls'], meta={'meta_1':item}, callback=self.second_parse)




    def second_parse(self, response):
        #提取每次 response中的meta的数据
        meta_1 = response.meta['meta_1']

        # 取出小类里所有子连接
        sonUrls = response.xpath('//a/@href').extract()

        items = []
        for i in range(0, len(sonUrls)):
            if_belong = sonUrls[i].endswith('.shtml') and sonUrls[i].startswith(meta_1['parentUrls'])

            if(if_belong):
                item = SinaItem()
                item['parentTitle'] = meta_1['parentTitle']
                item['parentUrls'] =meta_1['parentUrls']
                item['subUrls'] = meta_1['subUrls']
                item['subTitle'] = meta_1['subTitle']
                item['subFilename'] = meta_1['subFilename']
                item['sonUrls'] = sonUrls[i]
                items.append(item)

        for item in items:
            yield scrapy.Request(url=item['sonUrls'], meta={'meta_2':item}, callback = self.detail_parse)

    def detail_parse(self,response):
        item = response.meta['meta_2']
        content = ""
        head    = response.xpath('//h1[@id=\"main_title\"]/text()').extract()
        content_list = response.xpath('//div[@id=\"artibody\"]/p/text()').extract()

        for content_one in content_list:
            content += content_one

        item['head'] = head
        item['content'] = content

        yield item
































































