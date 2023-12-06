from scrapy import Spider


class BankSecuritySpider(Spider):
    name = "GitHub"
    start_urls = ["https://www.bankinfosecurity.co.uk/"]

    def parse(self, response):
        for card in response.css('article.excerpt'):
            title = card.xpath("./div[1]/div[2]/h2/a/text()").get()

            if title:
                yield {
                    "title": title,
                    "description": card.xpath("./div[1]/div[2]/p[2]/text()").get(),
                    "photo_url": card.xpath("./div[1]/div[1]/a/img/@src").get()
                }



