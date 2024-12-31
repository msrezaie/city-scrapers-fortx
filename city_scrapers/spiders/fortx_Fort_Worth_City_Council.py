import json
from datetime import datetime

import requests
import scrapy
from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parse as dateparse
from dateutil.relativedelta import relativedelta


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
        fetched from two of its API endpoints. The
        main API endpoint allows fetching meeting
        items for the entirety of one year. The
        spider is set to fetch all meetings 6 months
        in the past and 6 months in the future.
        """
        current_date = datetime.now()
        payloads = self.construct_payloads(current_date)

        for payload in payloads:
            if payload["StartDate"] == payload["EndDate"]:
                continue
            yield scrapy.Request(
                url=self.meetings_url,
                method="POST",
                body=json.dumps(payload),
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

        try:
            details_page = requests.get(meetings_detail_url).text
        except requests.RequestException as e:
            self.logger.error("Failed to retrieve details page: %s", e)
            return

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
            source=meeting_data.get("Link", response.url),
        )

        meeting["status"] = self._parse_status(meeting, meeting_data)
        meeting["id"] = self._get_id(meeting)

        yield meeting

    def _parse_status(self, meeting, item):
        if item["IsCancelled"]:
            return "cancelled"
        return self._get_status(meeting)

    def _parse_location(self, item):
        """
        Some meeting items' Address fields are returned empty.
        In such cases, the meeting is set to the default address.
        """
        location = item["Address"]
        name = location.get("Venue") or location.get("Suburb")
        address = location.get("Formatted").split(", ")
        address.pop(0) if len(address) > 1 else None
        address = ", ".join(address)

        if name == "Fort Worth":
            return {"name": "City Hall", "address": "200 Texas St., Fort Worth, 76102"}
        return {"name": name, "address": address}

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

        if attachment_link is not None:
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

    def construct_payloads(self, current_date):
        """
        The start and end dates parameters for this organization main
        API endpoint requires the dates to be within the same year.
        This means it can't be used to fetch meetings spanning months
        from different years. This method constructs start and end date
        ranges from the current date to 6 months in the past and 6 months
        in the future.
        """
        past = current_date - relativedelta(months=6)
        future = current_date + relativedelta(months=6)

        payloads = []

        if past.year != current_date.year:
            first_payload = self.meetings_url_payload.copy()
            first_payload["StartDate"] = str(past.date())
            first_payload["EndDate"] = str(datetime(past.year, 12, 31).date())
            second_payload = self.meetings_url_payload.copy()
            second_payload["StartDate"] = str(datetime(current_date.year, 1, 1).date())
            second_payload["EndDate"] = str(current_date.date())
            payloads.append(first_payload)
            payloads.append(second_payload)
        else:
            new_payload = self.meetings_url_payload.copy()
            new_payload["StartDate"] = str(past.date())
            new_payload["EndDate"] = str(current_date.date())
            payloads.append(new_payload)

        if future.year != current_date.year:
            first_payload = self.meetings_url_payload.copy()
            first_payload["StartDate"] = str(current_date.date())
            first_payload["EndDate"] = str(datetime(current_date.year, 12, 31).date())
            second_payload = self.meetings_url_payload.copy()
            second_payload["StartDate"] = str(datetime(future.year, 1, 1).date())
            second_payload["EndDate"] = str(future.date())
            payloads.append(second_payload)
            payloads.append(first_payload)
        else:
            new_payload = self.meetings_url_payload.copy()
            new_payload["StartDate"] = str(current_date.date())
            new_payload["EndDate"] = str(future.date())
            payloads.append(new_payload)

        return payloads
