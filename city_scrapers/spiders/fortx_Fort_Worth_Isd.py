from city_scrapers_core.constants import BOARD
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parse


class FortxFortWorthIsdSpider(CityScrapersSpider):
    name = "fortx_Fort_Worth_Isd"
    agency = "Fort Worth ISD Board"
    timezone = "America/Chicago"
    start_urls = ["https://www.fwisd.org/board/board-of-education/board-calendar"]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """

        # loop thru all dates that have events on them
        for day in response.css(".fsStateHasEvents"):
            meeting = Meeting(
                title=day.css(".fsCalendarTitle::text").get(),
                description="",
                classification=BOARD,
                start=self._parse_start(day),
                end=self._parse_end(day),
                all_day=False,
                time_notes="",
                location=self._parse_location(day),
                links=self._parse_links(day),
                source=self._parse_source(response),
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _strip_timezone(self, string):
        """Helper method to strip timezone information."""
        return "-".join(string.split("-")[:-1])

    def _parse_start(self, day):
        """Parse start datetime as a naive datetime object."""
        with_tz = day.css(".fsStartTime::attr(datetime)").get()
        no_tz = self._strip_timezone(with_tz)
        return parse(no_tz)

    def _parse_end(self, day):
        """Parse end datetime as a naive datetime object."""
        with_tz = day.css(".fsEndTime::attr(datetime)").get()
        no_tz = self._strip_timezone(with_tz)
        return parse(no_tz)

    def _parse_location(self, day):
        """Parse or generate location."""
        name = day.css(".fsLocation::text").get()
        return {"name": name, "address": ""}

    def _parse_links(self, day):
        """
        Parse links.
        Agenda link appears after clicking on meeting in calendar.
        It generates a request and returns HTML.
        This request requires more HTML parsing. Skipping for now.
        """
        return []

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
