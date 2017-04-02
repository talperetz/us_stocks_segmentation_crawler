# -*- coding: utf-8 -*-

"""
Date: 4/1/2017
TL;DR: scrapy's pipeline implementation
"""

from . import constants
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter


class CsvWriterPipeline(object):
    """
    saves items as a csv file (in constants.OUTPUT_FILE_PATH)
    """

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.file = open(constants.OUTPUT_FILE_PATH, 'wb')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
