import json
from datetime import datetime

import scrapy
from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parse as dateparse


class FortxFortWorthPublicMeetingsSpider(CityScrapersSpider):
    name = "fortx_Fort_Worth_Public_Meetings"
    agency = "Fort Worth Public Meetings"
    timezone = "America/Chicago"
    custom_settings = {
        "ROBOTSTXT_OBEY": False,
    }

    main_url = "https://www.fortworthtexas.gov/"

    meetings_url = "https://www.fortworthtexas.gov/ocapi/calendars/getcalendaritems"

    meetings_url_payload = {
        "LanguageCode": "en-US",
        "Ids": ["8efac0b6-9ea3-402e-b7d9-e9e71a2a34a0"],
        "StartDate": "",
        "EndDate": "",
    }

    meeting_detail_url = (
        "https://www.fortworthtexas.gov/ocapi/get/contentinfo"
        "?calendarId={calendarId}&contentId={contentId}&language=en-US"
        "&currentDateTime={currentDateTime}&mainContentId={mainContentId}"
    )

    def start_requests(self):
        """
        The meeting items for this organization are
        fetched from two of its API endpoints. The
        main API endpoint allows fetching meeting
        items for the entirety of one year. The
        spider is set to fetch all meetings for the
        current year.
        """
        current_date = datetime.now().date()

        start_of_year = datetime(current_date.year, 1, 1).date()
        end_of_year = datetime(current_date.year, 12, 31).date()

        self.meetings_url_payload["StartDate"] = str(start_of_year)
        self.meetings_url_payload["EndDate"] = str(end_of_year)

        yield scrapy.Request(
            url=self.meetings_url,
            method="POST",
            body=json.dumps(self.meetings_url_payload),
            headers={"Content-Type": "application/json"},
            callback=self.parse,
        )

    def parse(self, response):
        data = response.json()

        items = []
        for meeting in data["data"]:
            items.extend(meeting["Items"])

        for item in items:
            date_obj = datetime.strptime(item["DateTime"], "%d/%m/%Y %I:%M:%S %p")
            currentDateTime = date_obj.strftime("%d/%m/%Y%%20%I:%M:%S%%20%p")

            meeting_detail_url = self.meeting_detail_url.format(
                calendarId=item["CalendarId"],
                contentId=item["Id"],
                currentDateTime=currentDateTime,
                mainContentId=item["MainContentId"],
            )

            yield scrapy.Request(
                url=meeting_detail_url,
                method="GET",
                callback=self.parse_meeting,
                cb_kwargs={"item": item},
            )

    def parse_meeting(self, response, item):
        data = response.json()
        meeting_data = data["data"]

        meeting = Meeting(
            title=meeting_data["Title"],
            description=self._parse_description(meeting_data),
            classification=CITY_COUNCIL,
            start=dateparse(item["DateTime"]),
            end=None,
            all_day=False,
            time_notes="Please check the meeting description for details on the start time",  # noqa
            location=self._parse_location(meeting_data),
            links=[],
            source=meeting_data.get("Link", response.url),
        )

        meeting["status"] = self._parse_status(meeting, meeting_data)
        meeting["id"] = self._get_id(meeting)

        yield meeting

    def _parse_status(self, meeting, item):
        if item["IsCancelled"]:
            return "cancelled"
        return self._get_status(meeting)

    def _parse_description(self, item):
        description = item["Description"]
        description = description.replace("\r", "").replace("\n", "")
        return description

    def _parse_location(self, item):
        """
        Some meeting items' Address fields are returned empty.
        In such cases, the meeting is held via WebEx.
        """
        location = item["Address"]
        name = location.get("Venue") or location.get("Suburb")
        address = location.get("Formatted").split(", ")
        address.pop(0) if len(address) > 1 else None
        address = ", ".join(address)

        if not name and not address:
            return {"name": "WebEx", "address": "WebEx"}
        return {"name": name, "address": address}
