from scrapy import Spider


class TaoSecurityBlogSpider(Spider):
    name = "TaoSecurity Blog"
    start_urls = ["https://taosecurity.blogspot.com/"]

    def parse(self, response):
        for card in response.css('article.post-outer-container'):
            title = card.xpath("./div/div/h3/a/text()").get()
            description = card.xpath('./div/div/div[3]/div[2]/div/text()').get()
            photo_url = card.xpath('./div/div/div[3]/div/img/@src').get()

            yield {
                "title": title,
                "description": description.strip(),
                "photo_url": photo_url
            }
