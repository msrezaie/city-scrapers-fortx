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
    The scraper gathers meeting information from two separate endpoints
    specified in start_urls. One endpoint provides archived meetings,
    and the other provides current and upcoming meetings. This approach
    was chosen to keep the scraper simple and avoid overcomplicating it,
    especially since the CSS of the source webpages was quite messy.

    The data from the URLs are taken through a POST request with a payload
    containing the committee ID. The committee ID is the same for both URLs.
    """
    start_urls = [
        "https://tarrant-agendamanagement-public.techsharetx.gov/publicportal/api/meetings/readArchived",  # noqa
        "https://tarrant-agendamanagement-public.techsharetx.gov/publicportal/api/meetings/readCurrentAndUpcoming",  # noqa
    ]
    attachments_url = "https://tarrant-agendamanagement-public.techsharetx.gov/publicportal/api/meetingattachments/download?id="  # noqa
    source_url = "https://www.tarrantcountytx.gov/en/commissioners-court/commissioners-court-agenda-videos.html"  # noqa
    committee_id = "fe6aa5cc-7448-4194-ac6e-08dc95f79ccc"

    location = {
        "address": "100 East Weatherford Street, 5th Floor, Fort Worth, Texas 76196",  # noqa
        "name": "Tarrant County Administration Building (check the agenda for room location)",  # noqa
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
        data = response.json()
        meetings = data.get("data", [])
        for item in meetings:
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
                source=self.source_url,
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

        agenda = item.get("agendaAttachmentId")
        minutes = item.get("minutesAttachmentId")
        video = item.get("videoId")

        if agenda:
            links.append(
                {
                    "title": "Agenda",
                    "href": self.attachments_url + agenda,
                }
            )
        if minutes:
            links.append(
                {
                    "title": "Minutes",
                    "href": self.attachments_url + minutes,
                }
            )
        if video:
            video_url = f"https://www.youtube.com/watch?v={video}"
            links.append(
                {
                    "title": "Video",
                    "href": video_url,
                }
            )

        return links
