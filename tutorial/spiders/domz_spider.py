import scrapy

from tutorial.items import DmozItem

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/",
    ]

    def parse(self, response):
        for sel in response.xpath("//div[@id='subcategories-div']/section[@class='children']"):
            for href in sel.xpath("div/div/a/@href"):
                url = response.urljoin(href.extract())
                yield scrapy.Request(url, callback=self.parse_dir_content)

    def parse_dir_content(self, response):
        for sel in response.xpath("//div[@id='site-list-content']/div/div[@class='title-and-desc']"):
            item = DmozItem()
            item['title'] = sel.xpath('a/div//text()').extract()[0].rstrip('\r\n\t')
            item['link'] = sel.xpath('a/@href').extract()
            description = sel.xpath('normalize-space(div[normalize-space(@class)="site-descr"]//text())')[0].extract()
            description = description.replace("\r", '')
            description = description.replace("\n", '')
            description = description.replace("\t", '')
            item['desc'] = description;
            yield item
