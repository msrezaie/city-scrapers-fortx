from city_scrapers_core.constants import COMMITTEE
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parse


class FortxFortWorthIsdCocSpider(CityScrapersSpider):
    name = "fortx_Fort_Worth_Isd_Coc"
    agency = "Fort Worth ISD Citizens' Oversight Committee"
    timezone = "America/Chicago"
    start_urls = [
        "https://www.fwisd.org/departments/operations/capital-improvement-program/2021-citizens-oversight-committee-coc"  # noqa
    ]

    def parse(self, response):
        """
        Parse 2021 Citizens' Oversight Committee page.
        There is a Calendar section with upcoming meetings.
        There is also a Meeting Documents section with a table of past meetings.
        Scrape both.
        """

        location = {
            "name": "Fort Worth ISD District Service Center",
            "address": "7060 Camp Bowie Blvd, Fort Worth, TX 76116",
        }

        # keep track of scraped dates to prevent duplicates
        scraped_dates = set()

        # the first table has the old events
        # if there are duplicates on the page, we are potentially missing data
        # scrape data from table first bc it has more data (links) than next section
        for item in response.css("table")[0].css("tr"):
            start = self._parse_past_start(item)
            scraped_dates.add(start.date())
            meeting = Meeting(
                title="2021 Citizens' Oversight Committee Meeting",
                description="",
                classification=COMMITTEE,
                start=start,
                end=None,
                all_day=False,
                time_notes="",
                location=location,
                links=self._parse_past_links(item),
                source=self._parse_source(response),
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

        # go over the new events
        for item in response.css(".fsDayContainer"):
            start = self._parse_upcoming_start(item)
            if start and start.date() not in scraped_dates:
                meeting = Meeting(
                    title=self._parse_upcoming_title(item),
                    description="",
                    classification=COMMITTEE,
                    start=start,
                    end=self._parse_upcoming_end(item),
                    all_day=False,
                    time_notes="",
                    location=location,
                    links=[],
                    source=self._parse_source(response),
                )

                meeting["status"] = self._get_status(meeting)
                meeting["id"] = self._get_id(meeting)

                yield meeting

    def _parse_upcoming_title(self, item):
        """Parse or generate meeting title."""
        return item.css(".fsTitle a::text").get()

    def _strip_timezone(self, string):
        """Helper method to strip timezone information."""
        if not string:
            return None
        dt_naive = parse(string, ignoretz=True)
        return dt_naive

    def _parse_upcoming_start(self, item):
        """Parse upcoming start datetime as a naive datetime object."""
        datetime = item.css(".fsStartTime::attr(datetime)").get()
        return self._strip_timezone(datetime)

    def _parse_past_start(self, item):
        """
        Parse past start date as a naive datetime object.
        All meeting appear to happen at 6PM. 6PM is the default.
        """
        date = item.css("td::text").get()
        return parse(f"{date} 6:00PM")

    def _parse_upcoming_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        datetime = item.css(".fsEndTime::attr(datetime)").get()
        return self._strip_timezone(datetime)

    def _parse_past_links(self, item):
        """Parse or generate links."""
        links = []
        cells = item.css("td")
        # loop thru each cell
        for cell in cells:
            # check if there is a link present
            if cell.css("a"):
                # if so, add link to links array
                title = cell.css("a::text").get()
                href = cell.css("a::attr(href)").get()
                links.append({"title": title, "href": href})

        return links

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
