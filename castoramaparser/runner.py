from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from castoramaparser import settings
from castoramaparser.spiders.castorama import CastoramaSpider

if __name__ == '__main__':
    crawler_setting = Settings()
    crawler_setting.setmodule(settings)

    process = CrawlerProcess(settings=crawler_setting)

    process.crawl(CastoramaSpider)

    process.start()
