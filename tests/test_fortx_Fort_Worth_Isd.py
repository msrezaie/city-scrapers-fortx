from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fortx_Fort_Worth_Isd import FortxFortWorthIsdSpider

test_response = file_response(
    join(dirname(__file__), "files", "fortx_Fort_Worth_Isd.html"),
    url="https://www.fwisd.org/board/board-of-education/board-calendar",
)
spider = FortxFortWorthIsdSpider()

freezer = freeze_time("2024-10-09")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_count():
    assert len(parsed_items) == 2

def test_title():
    assert parsed_items[0]["title"] == "Special School Board Meeting"
    assert parsed_items[1]["title"] == "Regular School Board Meeting"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2024, 10, 8, 17, 30)


def test_end():
    assert parsed_items[0]["end"] == datetime(2024, 10, 8, 18, 30)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert parsed_items[0]["id"] == "fortx_Fort_Worth_Isd/202410081730/x/special_school_board_meeting"


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Fort Worth ISD District Service Center",
        "address": ""
    }


def test_source():
    assert parsed_items[0]["source"] == "https://www.fwisd.org/board/board-of-education/board-calendar"


def test_links():
    assert parsed_items[0]["links"] == []


def test_classification():
    assert parsed_items[0]["classification"] == BOARD


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
