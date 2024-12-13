from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import COMMISSION
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fortx_Tarrant_County_Commissioners_Court import (
    FortxTarrantCountyCommissionersCourtSpider,
)

archived_meetings = file_response(
    join(
        dirname(__file__),
        "files",
        "fortx_Tarrant_County_Commissioners_Court_archived_meetings.json",
    ),
    url="https://tarrant-agendamanagement-public.techsharetx.gov/publicportal/api/meetings/readArchived",  # noqa
)

upcoming_meetings = file_response(
    join(
        dirname(__file__),
        "files",
        "fortx_Tarrant_County_Commissioners_Court_upcoming_meetings.json",
    ),
    url="https://tarrant-agendamanagement-public.techsharetx.gov/publicportal/api/meetings/readCurrentAndUpcoming",  # noqa
)
spider = FortxTarrantCountyCommissionersCourtSpider()

freezer = freeze_time("2024-11-25")
freezer.start()

archived_items = [item for item in spider.parse(archived_meetings)]
upcoming_items = [item for item in spider.parse(upcoming_meetings)]

parsed_items = archived_items + upcoming_items
freezer.stop()


def test_count():
    assert len(parsed_items) == 11


def test_title():
    assert parsed_items[0]["title"] == "Commissioners Court"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2024, 12, 3, 10, 0)


def test_end():
    assert parsed_items[0]["end"] == datetime(2024, 12, 3, 17, 0)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert (
        parsed_items[0]["id"]
        == "fortx_Tarrant_County_Commissioners_Court/202412031000/x/commissioners_court"
    )


def test_status():
    assert parsed_items[0]["status"] == "tentative"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Tarrant County Administration Building (check the agenda for room location)",  # noqa
        "address": "100 East Weatherford Street, 5th Floor, Fort Worth, Texas 76196",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://www.tarrantcountytx.gov/en/commissioners-court/commissioners-court-agenda-videos.html"  # noqa
    )


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "title": "Agenda",
            "href": "https://tarrant-agendamanagement-public.techsharetx.gov/publicportal/api/meetingattachments/download?id=7f339758-fa4b-4ec7-0189-08dcfda5b8b4",  # noqa
        },
        {
            "title": "Video",
            "href": "https://www.youtube.com/watch?v=BSjaTEIkv1s",
        },
    ]


def test_classification():
    assert parsed_items[0]["classification"] == COMMISSION


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
