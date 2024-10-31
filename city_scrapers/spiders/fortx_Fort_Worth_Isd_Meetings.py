from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parse


class FortxFortWorthIsdMeetingsSpider(CityScrapersSpider):
    name = "fortx_Fort_Worth_Isd_Meetings"
    agency = "Fort Worth ISD Meetings"
    timezone = "America/Chicago"
    start_urls = ["https://meetings.boardbook.org/public/organization/733"]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for item in response.css("table tbody tr"):
            meeting = Meeting(
                title=self._parse_title(item),
                description=self._parse_description(item),
                classification=self._parse_classification(item),
                start=self._parse_start(item),
                end=self._parse_end(item),
                all_day=self._parse_all_day(item),
                time_notes=self._parse_time_notes(item),
                location=self._parse_location(item),
                links=self._parse_links(item),
                source=self._parse_source(response),
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_title(self, item):
        """Parse or generate meeting title."""
        str = item.css('td')[0].css('div::text').get()
        title = str.split('-')[1].strip()
        return title

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return NOT_CLASSIFIED

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        str = item.css('td')[0].css('div::text').get()
        date, time = str.split('at')
        time = time.split('-')[0]
        return parse(f"{date} {time}")

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return None

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        return ""

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, item):
        """Parse or generate location."""
        lines = item.css('td')[1].css('span::text')
        name = lines[0].get()
        line1 = lines[1].get()
        line2 = lines[2].get()
        return {
            "name": name,
            "address": f"{line1}, {line2}",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        # import pdb; pdb.set_trace()
        output = []
        links = item.css('a')
        for link in links:
            title = link.css('::text').get()
            if title == ' map it':
                title = 'Map Link'
            href = link.css('::attr(href)').get()
            output.append({ "title": title, "href": href })
        return output

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
