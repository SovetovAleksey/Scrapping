import scrapy
from scrapy.http import HtmlResponse
from castoramaparser.items import CastoramaparserItem
from scrapy.loader import ItemLoader

class CastoramaSpider(scrapy.Spider):
    name = 'castorama'
    allowed_domains = ['castorama.ru']
    i = 1


    def __init__(self):
        super().__init__()
        self.start_urls = ["https://www.castorama.ru/decoration/wallpaper"]

    def parse(self, response: HtmlResponse):
        if response.status != 404:
            next_page = f'https://www.castorama.ru/decoration/wallpaper?p={self.i}'
            self.i += 1
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@class='product-card__img-link']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)


    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=CastoramaparserItem(), response=response)
        loader.add_xpath('name', '//h1[@itemprop="name"]/text()')
        loader.add_xpath('price', "//span[@class='price']//text()")
        loader.add_xpath('photos', "//li[contains(@class,'thumb-slide')]/img/@src")
        loader.add_value('url', response.url)
        yield loader.load_item()
