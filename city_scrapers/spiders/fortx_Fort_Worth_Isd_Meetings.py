from urllib.parse import urljoin

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
        Parse meetings from table.
        """
        for item in response.css("table tbody tr"):
            meeting = Meeting(
                title=self._parse_title(item),
                description="",
                classification=NOT_CLASSIFIED,
                start=self._parse_start(item),
                end=None,
                all_day=False,
                time_notes="",
                location=self._parse_location(item),
                links=self._parse_links(item),
                source=self._parse_source(response),
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_title(self, item):
        """Parse meeting title."""
        str = item.css("td")[0].css("div::text").get()
        title = str.split("-")[1].strip()
        return title

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        str = item.css("td")[0].css("div::text").get()
        date, time = str.split("at")
        time = time.split("-")[0]
        return parse(f"{date} {time}")

    def _parse_location(self, item):
        """Parse location from 2nd field."""
        lines = item.css("td")[1].css("span::text")
        name = lines[0].get()
        line1 = lines[1].get()
        line2 = lines[2].get()
        return {
            "name": name,
            "address": f"{line1}, {line2}",
        }

    def _parse_links(self, item):
        """Parse links from table row."""
        base_url = "https://meetings.boardbook.org/"
        output = []
        links = item.css("a")
        for link in links:
            title = link.css("::text").get()
            if title == " map it":
                title = "Map Link"
            href = link.css("::attr(href)").get()
            # prepend base URL if necessary
            # enables usability on other websites
            href = urljoin(base_url, href)
            output.append({"title": title, "href": href})
        return output

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
