from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fortx_Fort_Worth_Isd_Meetings import FortxFortWorthIsdMeetingsSpider

test_response = file_response(
    join(dirname(__file__), "files", "fortx_Fort_Worth_Isd_Meetings.html"),
    url="https://meetings.boardbook.org/public/organization/733",
)
spider = FortxFortWorthIsdMeetingsSpider()

freezer = freeze_time("2024-10-31")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_count():
    assert len(parsed_items) == 28


def test_title():
    assert parsed_items[0]["title"] == "Regular Board Meeting"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2024, 8, 27, 17, 30)


def test_end():
    assert parsed_items[0]["end"] is None


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert parsed_items[0]["id"] == "fortx_Fort_Worth_Isd_Meetings/202408271730/x/regular_board_meeting"


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Fort Worth ISD District Service Center",
        "address": "7060 Camp Bowie Blvd., Fort Worth, TX 76116"
    }


def test_source():
    assert parsed_items[0]["source"] == "https://meetings.boardbook.org/public/organization/733"


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "title": "Map Link",
            "href": "https://maps.google.com/?q=7060+Camp+Bowie+Blvd.%2c+Fort+Worth%2c+TX+76116"
        },
        {
            "title": "Public Notice",
            "href": "/Public/PublicNotice/733?meeting=646834"
        },
        {
            "title": "Agenda",
            "href": "/Public/Agenda/733?meeting=646834"
        },
    ]


def test_classification():
    assert parsed_items[0]["classification"] == NOT_CLASSIFIED


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
