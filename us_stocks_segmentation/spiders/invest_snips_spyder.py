#!/usr/bin/env python

"""
:Date: 4/1/2017
:TL;DR: the scrapy spider crawler implementation
"""

import scrapy
import re
from ..items import Stock


class InvestSnipsSpider(scrapy.Spider):
    name = "invest_snips"

    def start_requests(self):
        """
        :return: request to parse a url
        """
        urls = [
            'http://investsnips.com/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        :param response: scrapy response from url
        :return: requests for next pages
        """
        categories = response.xpath('//a[contains(@href, "list-of")]/text()').extract()
        categories_links = response.xpath('//a[contains(@href, "list-of")]/@href').extract()
        for category, link in zip(categories[:-1], categories_links[:-1]):
            if link is not None:
                next_page = response.urljoin(link)
                yield scrapy.Request(next_page, callback=self.parse_category, meta={'category': category})

    def parse_category(self, response):
        """
        :param response: scrapy response from url
        :return: stocks items (name, symbol, category)
        """
        stocks = response.xpath("//a[contains(text(),'(')]/text()").extract()
        for stock in stocks:
            symbol = ''
            symbol_m = re.search(r"\(([A-Za-z0-9_]+)\)", stock)
            if symbol_m is not None:
                symbol = symbol_m.group(1)
            name = stock.split("(")[0].strip()
            yield Stock(name=name, symbol=symbol, category=response.meta['category'])