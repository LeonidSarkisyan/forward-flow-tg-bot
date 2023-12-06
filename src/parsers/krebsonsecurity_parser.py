from scrapy import Spider


class KrebsonSecuritySpider(Spider):
    name = "KrebsonSecurity"
    start_urls = ["https://krebsonsecurity.com/"]

    def parse(self, response):
        for card in response.xpath('/html/body/div/div[4]/div[1]/div/article'):
            title = card.xpath("./header[@class='entry-header']/h2/a/text()").get()
            yield {
                "title": title
            }

