import re
from datetime import datetime

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
        # Process the meetings presented in the "Commission Meetings" table:
        selector_str = "//h3/following-sibling::table/tbody/tr"
        for item in Selector(text=response).xpath(selector_str):  # for item in response.xpath(selector_str):
            # print(item.extract())
            if '<br>' in item.extract():  # TODO This one needs special treatment, I'll deal with that later!
                continue
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

        # Process the meetings presented in the "Commission Meeting Schedule for ..." list:
        selector_str = "(//h3/following-sibling::ul)[1]/li/text()"
        for item in Selector(text=response).xpath(selector_str):  # for item in response.xpath(selector_str):
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
            meeting_list.append(meeting)  # TODO Don't forget the de-duplication of the results of this loop!

        yield from meeting_list

    def _parse_description(self, item):
        text = self._clean_bad_chars(item.extract())
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
        datetime_obj = self._parse_date(item)
        # return datetime_obj
        return datetime.now()  # TODO Make sure to resolve this of course

    def _parse_date(self, item):
        """
        Parse the meeting date.
        """
        # Borrowed largely from chi_pubhealth.py
        # Future meetings are plain text
        # date_text = item.xpath('//text()').extract_first()
        # print(item)
        date_text = item.xpath('.//text()').extract()
        # date_text = self._clean_bad_chars(item.xpath('.//text()').extract())
        print(f"Length: {len(date_text)}")
        print(date_text)
        # date_text = item.xpath('//td/text()').extract_first()  # This will only work for Comission Meetings section
        # print(date_text)
        #
        # if not date_text:
        #     # Past meetings are links to the agenda
        #     date_text = item.xpath('a/text()').extract_first()

        # Handle typos like "December18"
        # if re.match(r'[a-zA-Z]+\d+', date_text):
        #     date_match = re.search(r'(?P<month>[a-zA-Z]+)(?P<day>\d+)', date_text)
        #     date_text = '{} {}'.format(date_match.group('month'), date_match.group('day'))
        # # Extract date formatted like "January 12"
        # return datetime.strptime(date_text, '%B %d')
        return date_text

    def _parse_links(self, item):
        """Parse or generate links."""
        documents = []
        # Should pretty much just be able to look for item.xpath('a/@href') or similar, see chi_pubhealth.py
        return documents

    def _clean_bad_chars(self, text):
        """ Remove unwanted unicode characters (only one found so far). """
        return text.replace(u'\u200b', '')

    # def _clean_bad_chars(self, item):
    #     pass
    # Now I'm confused because that stopped appearing I think.
    # Need to do something about '\u200b' showing up everywhere
