from scrapy.selector import Selector

from city_scrapers_core.constants import COMMISSION
from city_scrapers_core.items import Meeting


class PsuedoSpider:
    name = "chi_midway_noise"
    agency = "Chicago Midway Noise Compatibility Commission"
    timezone = "America/Chicago"
    allowed_domains = ["www.flychicago.com"]
    start_urls = ["https://www.flychicago.com"]
    title = "Midway Noise Compatibility Commission Meeting"
    location = {
        "name": "The Mayfield",
        "address": "6072 S. Archer Ave., Chicago, IL 60638",
    }
    source = "https://www.flychicago.com/community/MDWnoise/AdditionalResources/pages/default.aspx"

    def parse(self, response):
        meeting_list = []
        selector_str = "//div/div/div/h3/following-sibling::table/tbody/tr"
        for item in Selector(text=response).xpath(selector_str):  # for item in response.xpath(selector_str):
            print(item.extract())
            meeting = Meeting(
                title=self.title,
                description=self._parse_description(item),
                classification=COMMISSION,
                start=self._parse_start(item),
                end=None,
                all_day=False,
                time_notes="Start times are not explicitly stated, but all observed past meetings occurred at 6:30PM",
                location=self.location,
                links=self._parse_links(item),
                source=self.source,
            )
            meeting_list.append(meeting)

        yield from meeting_list

    def _parse_description(self, item):
        text = item.extract()
        desc = ''
        if 'Regular' in text:
            desc = 'Regular Meeting'
        elif 'Special' in text:
            desc = 'Special Meeting'
        elif 'Committee' in text:
            desc = 'Committee Meeting'
            if 'Executive' in text:
                desc = f"Executive {desc}"
            elif 'Residential' in text:
                desc = f"Residential {desc}"
        return desc

    def _parse_start(self, item):
        pass

    def _parse_links(self, item):
        """Parse or generate links."""
        documents = []
        # Should pretty much just be able to look for item.xpath('a/@href') or similar, see chi_pubhealth.py
        return documents
