import scrapy


class QuotesSpider(scrapy.Spider):
    name = "first"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            #'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #page = response.url.split("/")[-2]
        self.log(response.css('title::text').extract())
        self.log(response.css('title').extract_first())
        self.log(response.css('title').re(r'(\w+) to (\w+)'))
        self.log(response.css('div.quote')[0].extract())
        quote = response.css("div.quote")[0]
        tags = quote.css("div.tags a.tag::text").extract()
        self.log(tags)

        with open('test2.html', 'wb') as f:
            f.write(tags[0])
        self.log('Saved file')
