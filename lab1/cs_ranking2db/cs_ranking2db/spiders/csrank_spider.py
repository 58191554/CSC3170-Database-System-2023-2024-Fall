from pathlib import Path
import scrapy
import re
from cs_ranking2db.items import CsRanking2DbItem

class CSRankSpider(scrapy.Spider):
    name = 'cs_ranks'
    
    def start_requests(self):
        urls = [
            "https://www.usnews.com/best-graduate-schools/top-science-schools/computer-science-rankings",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = f"cs_rank.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")

        table = response.xpath('//*[@id="search-content"]/div[4]/div[2]/div/div/table')
        for row in table.xpath('.//tr'):
            name_prefix = row.xpath('.//h3/text()').get()
            name_suffix = row.xpath('.//span/text()').get()
            rank_element_str = row.xpath('.//strong').get()
            match = re.search(r'<!-- -->(\d+)<!-- -->', str(rank_element_str))

            if match:
                rank = match.group(1)
            else:
                rank =-1

            location_element = row.xpath('.//p').get()
            matches = re.findall(r'([\w\s]+)<!-- -->,\s<!-- -->([\w\s]+)', str(location_element))

            if matches:
                city, state = matches[0]
            else:
                city, state = None, None

            if name_prefix and name_suffix:
                item = CsRanking2DbItem(name=name_prefix + name_suffix, rank_number=rank, city=city, state=state)
                yield item