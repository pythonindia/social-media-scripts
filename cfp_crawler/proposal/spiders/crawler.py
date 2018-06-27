# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import signals

class CrawlerSpider(scrapy.Spider):
    name = 'crawler'
    allowed_domains = ['in.pycon.org']
    url = "https://in.pycon.org"
    proposals = {}
    file = open("proposals.json", "w")
    def start_requests(self):
        yield scrapy.Request(self.url + "/cfp/2018/proposals", callback = self.parse)

    def parse(self, response):
        proposal_links = response.xpath("//h3[@class='proposal--title']/a/@href").extract()
        index = 1
        for link in proposal_links:
            yield scrapy.Request(self.url + link, callback = self.parseProposal, meta = {"number" : index})
            index += 1
        
        
    def parseProposal(self, response):
        index = response.meta.get("number")

        title = response.xpath("//h1[@class='proposal-title']/text()").extract()[0].strip()
        author = response.xpath("//p[@class='text-muted']/small/b/text()").extract()[0].strip()
        created_on = response.xpath("//p[@class='text-muted']/small/b/time/text()").extract()[0].strip()

        section = response.xpath("//section[@class='col-sm-8 proposal-writeup']/div")
        some_dic = {}
        for div in section:
            heading = div.xpath(".//h4[@class='heading']/b/text()").extract()[0]
            data = self.format_data(div.xpath(".//text()").extract(), heading)
            data = data[2:-2]
            some_dic[heading[:-1]] = data
        
        table = response.xpath("//table/tr")
        for col in table:
            heading = col.xpath(".//td/small/text()").extract()[0].strip()
            data = col.xpath(".//td/text()").extract()[0].strip()
            some_dic[heading[:-1]] = data
        
        some_dic["title"] = title
        some_dic["link_to_proposal"] = response.request.url
        some_dic["author"] = author
        some_dic["created_on"] = created_on
        some_dic["Last Updated"] = response.xpath("//time/text()").extract()[0]

        self.proposals[index] = some_dic
                
    def format_data(self, data, head):
        return " ".join([d.strip() for d in data if d != "" and d!=head ])
    
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(CrawlerSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print("Closing spider")
        json.dump(self.proposals, self.file, indent = 2, sort_keys = True)
        
        
  