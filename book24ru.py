'''
1) Создать пауков по сбору данных о книгах с сайтa book24.ru
2) Паук должен собирать:
* Ссылку на книгу
* Наименование книги
* Автор(ы)
* Основную цену
* Цену со скидкой
* Рейтинг книги
3) Собранная информация должна складываться в базу данных
'''


import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BooksParserItem


class Book24ruSpider(scrapy.Spider):
    name = 'book24ru'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/catalog/fiction-1592/?saleleader=1']
    i = 1

    def parse(self, response: HtmlResponse):
        if response.status != 404:
            next_page = f'https://book24.ru/catalog/fiction-1592/page-{self.i}/?saleleader=1'
            self.i += 1
            yield response.follow(next_page, callback=self.parse)

            links = response.xpath("//a[@class='product-card__name smartLink']/@href").getall()

            for link in links:
                link = f'https://book24.ru{link}'
                yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        author = response.xpath("(//a[@class='product-characteristic-link smartLink'])/text()").get()
        name = response.xpath("(//h1[@itemprop='name'])/text()").get()
        priceold = response.xpath("//span[@class='app-price product-sidebar-price__price-old']/text()").get()
        price = response.xpath("//meta[@itemprop='price']/@content").get()
        rate = response.xpath("//span[@class='rating-widget__main-text']/text()").get()
        link = response.url
        item = BooksParserItem(author=author, name=name, priceold=priceold, price=price, rate=rate, link=link)
        yield item
