# -*- coding: utf-8 -*-

import scrapy


class Stock(scrapy.Item):
    """
    the basic entity that represents each row in the final dataframe
    """
    name = scrapy.Field()
    symbol = scrapy.Field()
    category = scrapy.Field()
