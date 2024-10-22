from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import COMMITTEE
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fortx_Fort_Worth_Isd_Coc import FortxFortWorthIsdCocSpider

test_response = file_response(
    join(dirname(__file__), "files", "fortx_Fort_Worth_Isd_Coc.html"),
    url="https://www.fwisd.org/departments/operations/capital-improvement-program/2021-citizens-oversight-committee-coc",
)
spider = FortxFortWorthIsdCocSpider()

freezer = freeze_time("2024-10-09")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()

def test_count():
    assert len(parsed_items) == 14


def test_title():
    assert parsed_items[0]["title"] == "2021 Citizens Oversight Committee Meeting"
    assert parsed_items[1]["title"] == "2021 Citizens Oversight Committee - Special Meeting"
    assert parsed_items[3]["title"] == "2021 COC"
    assert parsed_items[13]["title"] == "2021 COC"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2024, 9, 9, 18, 0)
    assert parsed_items[2]["start"] == datetime(2024, 12, 2, 18, 0)
    assert parsed_items[3]["start"] == datetime(2024, 9, 9, 0, 0)
    assert parsed_items[13]["start"] == datetime(2022, 6, 6, 0, 0)

def test_end():
    assert parsed_items[0]["end"] == datetime(2024, 9, 9, 19, 0)
    assert parsed_items[1]["end"] == datetime(2024, 10, 21, 19, 0)
    assert parsed_items[2]["end"] == datetime(2024, 12, 2, 19, 0)
    assert parsed_items[3]["end"] == None
    assert parsed_items[13]["end"] == None


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert parsed_items[0]["id"] == "fortx_Fort_Worth_Isd_Coc/202409091800/x/2021_citizens_oversight_committee_meeting"


def test_status():
    assert parsed_items[0]["status"] == "passed"
    assert parsed_items[1]["status"] == "tentative"
    assert parsed_items[2]["status"] == "tentative"
    assert parsed_items[3]["status"] == "passed"
    assert parsed_items[13]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Fort Worth ISD District Service Center",
        "address": "7060 Camp Bowie Blvd, Fort Worth, TX 76116"
    }
    assert parsed_items[13]["location"] == {
        "name": "Fort Worth ISD District Service Center",
        "address": "7060 Camp Bowie Blvd, Fort Worth, TX 76116"
    }


def test_source():
    assert parsed_items[0]["source"] == "https://www.fwisd.org/departments/operations/capital-improvement-program/2021-citizens-oversight-committee-coc"


def test_links():
    assert parsed_items[0]["links"] == []
    assert parsed_items[3]["links"] == [
        {
            "title": "Agenda",
            "href": "https://drive.google.com/file/d/1Dqk3tdEhQYQ_LIbk30bT1weK2BIF3xu9/view?usp=drive_link"
        },
        {
            "title": "Presentation",
            "href": "https://drive.google.com/file/d/1T442XJTxHLXoLbDWki0hyFSqGjlcROrr/view?usp=drive_link"
        },
    ]
    assert parsed_items[4]["links"] == [
        {
            "title": "Agenda",
            "href": "https://drive.google.com/file/d/1H78SIPHk-qidCxUJAzBX_ubSZr4uPpgW/view?usp=drive_link"
        },
        {
            "title": "Presentation",
            "href": "https://drive.google.com/file/d/1Nl5RkLmOWloPPCYR6kuSMQrb8ml0Xjss/view?usp=drive_link"
        },
        {
            "title": "Minutes",
            "href": "https://drive.google.com/file/d/1gR7xUdtqPplwQo9fUSu3aNMCxG-L68F1/view?usp=drive_link"
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == COMMITTEE


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
