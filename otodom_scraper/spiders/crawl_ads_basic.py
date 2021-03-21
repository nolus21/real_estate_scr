# -*- coding: utf-8 -*-
import unicodedata
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from otodom_scraper.items import AdItem


def remove_diacritics(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str.replace('ł', 'l'))
    return u''.join([c for c in nfkd_form if not unicodedata.combining(c)])
# remove_diacritics('zażółć gęślą jaźń')


class CrawlAdsBasicSpider(CrawlSpider):
    name = 'crawl_ads_basic'
    allowed_domains = ['otodom.pl']

    def __init__(self,
                 locations=None,
                 page=None,
                 *args, **kwargs):

        if locations:
            self.locations = remove_diacritics(locations).replace(' ', '-').split(';')
            self.locations = [x + '/' for x in self.locations]
        else:
            self.locations = ['']

        if page == 1 or page == str(1):
            url_parts = ['/sprzedaz/mieszkanie/' + x for x in self.locations]
            self.start_urls = ['https://www.otodom.pl' + x + 
            '?nrAdsPerPage=72' for x in url_parts] #for EVERY each otodom + location ADD page number
    #this seems to be the url - how to make it parse through the pages?
    #&page=2
        else:
            url_parts = ['/sprzedaz/mieszkanie/' + x for x in self.locations]
            self.start_urls = ['https://www.otodom.pl' + x + 
            '?nrAdsPerPage=72' + '&page=' + page for x in url_parts] #for EVERY each otodom + location ADD page number
    #this seems to be the url - how to make it parse through the pages?
    #&page=2

        self.rules = (
            Rule(LinkExtractor(allow=[x + '\\?nrAdsPerPage=72$' for x in url_parts]),
                 callback='parse_item', follow=True),
            Rule(LinkExtractor(allow=[x + '.*page=[0-9]+$' for x in url_parts]), #rule for pages - but does it iterrate? parse through 
                 callback='parse_item', follow=True),
        )

        super(CrawlAdsBasicSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        for ad in response.css('.col-md-content article'):
            item = ItemLoader(item=AdItem(), selector=ad)

            item.add_css('item_id', '::attr("data-item-id")')
            item.add_css('tracking_id', '::attr("data-tracking-id")')
            item.add_css('url', '::attr("data-url")')
            item.add_css('featured_name', '::attr("data-featured-name")')
            item.add_css('title', '.offer-item-title ::text')
            item.add_css('subtitle', '.offer-item-header p ::text')
            item.add_css('rooms', '.offer-item-rooms ::text')
            item.add_css('price', '.offer-item-price ::text')
            item.add_css('price_per_m', '.offer-item-price-per-m ::text')
            item.add_css('area', '.offer-item-area ::text')
            item.add_css('longitude', '.offer-item-longitude ::text')
            item.add_css('latitude', '.offer-item-latitude ::text')
            item.add_css('others', '.params-small li ::text')

            yield item.load_item()

import pandas as pd