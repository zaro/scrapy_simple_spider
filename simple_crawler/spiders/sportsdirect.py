# -*- coding: utf-8 -*-
import scrapy
from ..items import ProductItem


class SportsdirectSpider(scrapy.Spider):
    name = 'sportsdirect'
    allowed_domains = ['sportsdirect.com']
    start_urls = [
    'http://www.sportsdirect.com/mens/mens-rugby-boots',
    #'http://www.sportsdirect.com/mens/mens-shirts'
    ]

    def parse(self, response):
        products = response.css('.s-productthumbbox')
        for p in products:
            brand = p.css('.productdescriptionbrand::text').extract_first()
            productName = p.css('.productdescriptionname::text').extract_first()
            price = p.css('.curprice::text').extract_first()
            productUrl = p.css('a::attr(href)').extract_first()
            item = ProductItem()
            item['brand'] = brand
            item['name'] = productName
            item['price'] = price
            item['url'] = response.urljoin(productUrl)
            r = scrapy.Request(url=response.urljoin(productUrl), callback=self.parseProduct)
            r.meta['item'] = item
            yield r
        nextPageLinkSelector = response.css('.NextLink::attr("href")')
        if nextPageLinkSelector:
            nextPageLink = nextPageLinkSelector[0].extract()
            yield scrapy.Request(url=response.urljoin(nextPageLink))

    def parseProduct(self, response):
        item = response.meta['item']
        imageUrls = response.css('a::attr(srczoom)').extract()
        item['image_urls'] = imageUrls
        yield item
