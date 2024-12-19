import json
from datetime import datetime

import requests
import scrapy
from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parse as dateparse


class FortxFortWorthCityCouncilSpider(CityScrapersSpider):
    name = "fortx_Fort_Worth_City_Council"
    agency = "Fort Worth City Council"
    timezone = "America/Chicago"

    custom_settings = {
        "ROBOTSTXT_OBEY": False,
    }

    main_url = "https://www.fortworthtexas.gov/"

    meetings_url = "https://www.fortworthtexas.gov/ocapi/calendars/getcalendaritems"

    meetings_url_payload = {
        "LanguageCode": "en-US",
        "Ids": ["8a8add9a-3fd0-4b39-9a3e-d58e98e27acc"],
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
        fetched from a few of its API endpoints. The
        main API endpoint allows fetching meeting
        items for the entirety of the year. The
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

        meetings_detail_url = meeting_data["Link"]

        details_page = requests.get(meetings_detail_url).text

        meeting = Meeting(
            title=meeting_data["Title"],
            description=meeting_data["Description"],
            classification=CITY_COUNCIL,
            start=dateparse(item["DateTime"]),
            end=None,
            all_day=False,
            time_notes="Please check the meeting description for details on the start time",  # noqa
            location=self._parse_location(meeting_data),
            links=self._parse_links(details_page),
            source=response.url,
        )

        meeting["status"] = self._get_status(meeting)
        meeting["id"] = self._get_id(meeting)

        yield meeting

    def _parse_location(self, item):
        """Meetings which are cancelled do not return the full address"""
        address = item["Address"]
        if item["IsCancelled"]:
            return {"name": address["Suburb"], "address": address["Formatted"].strip()}
        return {"name": address["Venue"], "address": address["Formatted"].strip()}

    def _parse_links(self, response):
        selector = scrapy.Selector(text=response)
        links = []
        attachment_div = selector.css(".side-box.consultation-snapshot")
        attachment_hint = (
            attachment_div.css(".side-box-title::text").get(default="").strip()
        )
        attachment_link = attachment_div.css(
            ".side-box-section.body-content a::attr(href)"
        ).get()

        if attachment_hint:
            if "agenda" in attachment_hint.lower():
                links.append(
                    {"href": self.main_url + attachment_link, "title": "Agenda"}
                )
            if "minutes" in attachment_hint.lower():
                links.append(
                    {"href": self.main_url + attachment_link, "title": "Minutes"}
                )
            if "notice" in attachment_hint.lower():
                links.append(
                    {"href": self.main_url + attachment_link, "title": "Public Notice"}
                )

        return links
