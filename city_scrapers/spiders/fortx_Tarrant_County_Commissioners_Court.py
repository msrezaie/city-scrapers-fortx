import json
import scrapy
from city_scrapers_core.constants import COMMISSION
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parse as dateparse


class FortxTarrantCountyCommissionersCourtSpider(CityScrapersSpider):
    name = "fortx_Tarrant_County_Commissioners_Court"
    agency = "Tarrant County Commissioners Court"
    timezone = "America/Chicago"

    """
    The scraper gathers meeting information from two separate endpoints specified in start_urls. One
    endpoint provides archived meetings, and the other provides current and upcoming meetings. This
    approach was chosen to keep the scraper simple and avoid overcomplicating it, especially since
    the CSS of the source webpages was quite messy.
    """
    start_urls = [
        "https://tarrant-agendamanagement-public.techsharetx.gov/publicportal/api/meetings/readArchived",
        "https://tarrant-agendamanagement-public.techsharetx.gov/publicportal/api/meetings/readCurrentAndUpcoming",
    ]
    agenda_base_url = (
        "https://prod-agendamanagement-publicportal.azurewebsites.us/HtmlAgenda/"
    )
    committee_id = "fe6aa5cc-7448-4194-ac6e-08dc95f79ccc"

    location = {
        "address": "100 East Weatherford Street, 5th Floor, Fort Worth, Texas 76196",
        "name": "Tarrant County Administration Building (check the agenda for room location)",
    }

    def start_requests(self):
        payload = {"committeeId": self.committee_id}
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                method="POST",
                body=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                callback=self.parse,
            )

    def parse(self, response):
        data = json.loads(response.text)
        meetings = data.get("data", [])
        for item in meetings:
            if item.get("meetingType") != "Commissioners Court":
                continue
            meeting = Meeting(
                title=item.get("description", "Commissioners Court"),
                description="",
                classification=COMMISSION,
                start=self._parse_datetime(item.get("meetingStartDateTime")),
                end=self._parse_datetime(item.get("meetingEndDateTime")),
                all_day=False,
                time_notes="",
                location=self.location,
                links=self._parse_links(item),
                source=response.url,
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_datetime(self, datetime_str):
        """
        Parse the datetime string into a datetime object.
        """
        if datetime_str:
            return dateparse(datetime_str)
        return None

    def _parse_links(self, item):
        links = []

        if item.get("hasAgenda") and item.get("id"):
            links.append(
                {
                    "title": "Agenda",
                    "href": self.agenda_base_url + item["id"],
                }
            )
        if item.get("videoId"):
            video_url = f"https://www.youtube.com/watch?v={item['videoId']}"
            links.append(
                {
                    "title": "Video",
                    "href": video_url,
                }
            )
        return links
