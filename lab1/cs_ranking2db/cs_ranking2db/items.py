'''
Author: Zhen Tong 120090694@link.cuhk.edu.cn
'''


# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CsRanking2DbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    rank_number = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    pass
