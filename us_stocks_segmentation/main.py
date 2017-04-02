#!/usr/bin/env python

"""
Date: 4/1/2017
TL;DR: this module's goal is to create a stocks segmentation excel sheet
Abstract: got an assignment on one of my interviews as CTO
Problem: create us stocks segmentation according to http://investsnips.com/
Proposed Solution: use scrapy for web scraping and pandas to edit the csv
"""

import pandas as pd
from us_stocks_segmentation import constants
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

__author__ = "Tal Peretz"
__copyright__ = "Copyright 2017"
__credits__ = ["Tal Peretz"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Tal Peretz"
__email__ = "talperetz24@gmail.com"
__status__ = "Development"


def get_first_arg(*args):
    return args[0]


if __name__ == "__main__":
    # run crawler
    process = CrawlerProcess(get_project_settings())
    process.crawl('invest_snips')
    process.start()

    # fix csv
    df = pd.read_csv(constants.OUTPUT_FILE_PATH, skip_blank_lines=True)

    # group by name
    df_by_name = df.groupby(by='name').agg({'symbol': lambda ser: ser.iloc[0],
                                            'category': lambda ser: ' ,'.join(list(set(ser)))})[['symbol', 'category']]
    # group by category
    df_by_cat = df.groupby(by='category').agg({'symbol': lambda ser: ' ,'.join(list(set(ser.astype(str)))),
                                               'name': lambda ser: ' ,'.join(list(set(ser.astype(str))))})[
        ['symbol', 'name']]

    # override csv
    df_by_name.to_csv(constants.BY_NAME_OUTPUT_FILE_PATH)
    df_by_cat.to_csv(constants.BY_CATS_OUTPUT_FILE_PATH)
