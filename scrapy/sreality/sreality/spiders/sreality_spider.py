from typing import Iterable

import scrapy
from scrapy_playwright.page import PageMethod
from ..items import SrealityItem


class SrealitySpider(scrapy.Spider):
    name = "sreality_spider"
    allowed_domains = ["www.sreality.cz"]
    start_urls = ["https://www.sreality.cz/hledani/prodej/byty"]
    item_count = 0

    def start_requests(self):
        url = "https://www.sreality.cz/hledani/prodej/byty"
        yield scrapy.Request(url, meta={
            'playwright': True,
            'playwright_include_page': True,
            'playwright_page_methods': [
                PageMethod('wait_for_selector', 'div.dir-property-list div.property')
            ],
            'errback': self.errback
        })

    async def parse(self, response):
        page = response.meta['playwright_page']
        await page.close()

        for prop_title in response.css('div.dir-property-list div.property'):
            if self.item_count >= 500:
                break
            title = prop_title.css('div.text-wrap h2 span::text').get()
            img_url = prop_title.css('preact div div a:nth-child(1) img::attr(src)').extract_first()

            title = str(title).replace("\xa0", "")
            self.item_count += 1

            item = SrealityItem()
            item["title"] = title
            item["img"] = img_url
            yield item

        # print(response.css('ul.paging-full li.paging-item:last-child a::attr(href)').get())
        next_page = response.css('ul.paging-full li.paging-item:last-child a::attr(href)').get()
        print(next_page)
        if self.item_count < 500 and next_page is not None:
            next_page_url = 'https://www.sreality.cz' + next_page

            yield scrapy.Request(next_page_url, meta={
                'playwright': True,
                'playwright_include_page': True,
                'playwright_page_methods': [
                    PageMethod('wait_for_selector', 'div.dir-property-list div.property')
                ],
                'errback': self.errback
            })

    async def errback(self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()

