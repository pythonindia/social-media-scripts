# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import signals


class CrawlerSpider(scrapy.Spider):
    name = 'crawler'
    allowed_domains = ['in.pycon.org']
    url = "https://in.pycon.org"
    proposals = []
    file = open("proposals.json", "w")
    def start_requests(self):
        yield scrapy.Request(self.url + "/cfp/2018/proposals", callback = self.parse)

    def parse(self, response):
        proposal_links = response.xpath("//h3[@class='proposal--title']/a/@href").extract()
        for link in proposal_links:
            yield scrapy.Request(self.url + link, callback = self.parseProposal)
        
        
        
    def parseProposal(self, response):
        title = response.xpath("//h1[@class='proposal-title']/text()").extract()[0].strip()
        author = response.xpath("//p[@class='text-muted']/small/b/text()").extract()[0].strip()
        created_on = response.xpath("//p[@class='text-muted']/small/b/time/text()").extract()[0].strip()

        section = response.xpath("//section[@class='col-sm-8 proposal-writeup']/div")
        proposal = {}
        for div in section:
            heading = div.xpath(".//h4[@class='heading']/b/text()").extract()[0]
            data = self.format_data(div.xpath(".//text()").extract(), heading)
            data = data[2:-2]
            proposal[heading[:-1]] = data
        
        table_rows = response.xpath("//table/tr")
        for row in table_rows:
            extra_info_heading = row.xpath(".//td/small/text()").extract()[0].strip()
            extra_info_content = row.xpath(".//td/text()").extract()[0].strip()
            proposal[extra_info_heading[:-1]] = extra_info_content
        
        proposal["title"] = title
        proposal["link_to_proposal"] = response.request.url
        proposal["author"] = author
        proposal["created_on"] = created_on
        proposal["Last Updated"] = response.xpath("//time/text()").extract()[0]

        self.proposals.append(proposal)
                
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
        self.file.close()
        
        
  
