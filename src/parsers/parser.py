from scrapy import Spider


class GITSpider(Spider):
    name = "GitHub"
    start_urls = ["https://www.bankinfosecurity.co.uk/"]

    def parse(self, response):
        for title in response.css('.title'):
            yield {
                "title": title.xpath("./a/text()").get()
            }
