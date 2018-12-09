# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from datetime import datetime
from ShuCai.items import ShucaiItem

class ScHqSpider(scrapy.Spider):
    name = 'sc_hq'
    # allowed_domains = ['www.xinfadi.com.cn']
    # start_urls = ['http://www.xinfadi.com.cn/marketanalysis/1/list/1.shtml',]
    # 批量采集用！
    start_urls = []
    for i in range(4163, 0, -1):
        start_urls.append('http://www.xinfadi.com.cn/marketanalysis/1/list/{}.shtml'.format(i))

    def parse(self, response):
        age = True
        item = ShucaiItem()
        tem = response.xpath('//table[@class="hq_table"]/tr')
        for i in range(1, len(tem)):
            tem2 = tem[i].xpath('.//td/text()').extract()
            item['name'] = tem2[0].strip()
            item['lowest'] = tem2[1].strip()
            item['average'] = tem2[2].strip()
            item['highest'] = tem2[3].strip()
            item['unit'] = tem2[5].strip()
            item['date'] = tem2[6].strip()
            yield item
            # 获取日期格式为2018-12-3
            # OldDate = datetime.strptime(tem2[6].strip(),'%Y-%m-%d').date()
            # NowDate = datetime.now().date()
            # if NowDate == OldDate:
            #     yield scrapy.Request(page,callback=self.get_page)
            # date = tem2[6].strip()
            # print(age,date)
            # if date != '2018-12-04':
            #     age = False
            # else:
            #     yield item
        # page = response.xpath('//div[@class="manu"]/a[@title="下一页"]/@href').extract_first()
        # if page is not []:
        #     # 网址拼接三种方法　下面两种及第三种yield　后面的response.follow(page)
        #     # page = parse.urljoin(response.url, page)
        #     page = response.urljoin(page)
        #     print(date, page,age)
        #     # 获取当前物品时间
        #     if age:
        #         yield response.follow(page)

    def get_page(self,response):
        pass
        # item = ShucaiItem()
        # tem = response.xpath('//table[@class="hq_table"]/tr')
        # for i in range(1,len(tem)):
        #     tem2 = tem[i].xpath('.//td/text()').extract()
        #     item['name'] = tem2[0].strip()
        #     item['lowest'] = tem2[1].strip()
        #     item['average'] = tem2[2].strip()
        #     item['highest'] = tem2[3].strip()
        #     item['unit'] = tem2[5].strip()
        #     item['date'] = tem2[6].strip()
        #     yield item
