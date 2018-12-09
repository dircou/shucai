# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShucaiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    lowest = scrapy.Field()
    REAL = scrapy.Field()
    average = scrapy.Field()
    highest = scrapy.Field()
    unit = scrapy.Field()
    date = scrapy.Field()
