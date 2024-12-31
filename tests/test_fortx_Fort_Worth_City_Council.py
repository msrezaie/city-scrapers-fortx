from datetime import datetime
from os.path import dirname, join

import pytest
import scrapy
from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fortx_Fort_Worth_City_Council import (
    FortxFortWorthCityCouncilSpider,
)

meetings_items = file_response(
    join(
        dirname(__file__), "files", "fortx_Fort_Worth_City_Council_meeting_items.json"
    ),
    url="https://www.fortworthtexas.gov/ocapi/calendars/getcalendaritems",
)

meetings_detail = file_response(
    join(
        dirname(__file__), "files", "fortx_Fort_Worth_City_Council_meeting_details.json"
    ),
    url=(
        "https://www.fortworthtexas.gov/ocapi/get/contentinfo?calendarId=8a8add9a-3fd0-4b39-9a3e-d58e98e27acc"  # noqa
        "&contentId=07d0abc1-462c-4b0a-94b9-d1e7aee72eec&language=en-US&currentDateTime=09/01/2024%2012:00:00%20PM"  # noqa
        "&mainContentId=07d0abc1-462c-4b0a-94b9-d1e7aee72eec"
    ),
)

spider = FortxFortWorthCityCouncilSpider()

freezer = freeze_time("2024-12-19")
freezer.start()

parsed_items = []

for req in spider.parse(meetings_items):
    if isinstance(req, scrapy.Request):
        meeting_detail_item = spider.parse_meeting(
            meetings_detail, req.cb_kwargs["item"]
        )
        parsed_items.extend(meeting_detail_item)

freezer.stop()

"""
The spider for this site is set to fetch meeting items for the entire year.
To make the test less time consuming, the number of meetings to be tested is
limited to 17 items.
"""


def test_count():
    assert len(parsed_items) == 17


def test_title():
    assert parsed_items[0]["title"] == "City Council Executive Session"


def test_description():
    assert parsed_items[0]["description"] == "City Council Executive Session"


def test_start():
    assert parsed_items[0]["start"] == datetime(2024, 9, 1, 12, 0)


def test_end():
    assert parsed_items[0]["end"] is None


def test_time_notes():
    assert (
        parsed_items[0]["time_notes"]
        == "Please check the meeting description for details on the start time"
    )


def test_id():
    assert (
        parsed_items[0]["id"]
        == "fortx_Fort_Worth_City_Council/202409011200/x/city_council_executive_session"
    )


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Old City Hall",
        "address": "200 Texas St., Fort Worth, 76102",
    }


def test_source():
    assert parsed_items[0]["source"] == (
        "https://www.fortworthtexas.gov/departments/citysecretary/"
        "events/2024-city-council-executive-session-meetings"
    )


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "href": "https://www.fortworthtexas.gov//files/assets/public/v/2/city-secretary/documents/calendar/2024-agendas/city-council/executive-session/11-05-2024-executive-session.pdf",  # noqa
            "title": "Agenda",
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == CITY_COUNCIL


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
