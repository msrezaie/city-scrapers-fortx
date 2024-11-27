from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import COMMISSION
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fortx_Tarrant_County_Commissioners_Court import (
    FortxTarrantCountyCommissionersCourtSpider,
)

test_response = file_response(
    join(dirname(__file__), "files", "fortx_Tarrant_County_Commissioners_Court.json"),
    url="https://tarrant-agendamanagement-public.techsharetx.gov/publicportal/api/meetings/readArchived",  # noqa
)
spider = FortxTarrantCountyCommissionersCourtSpider()

freezer = freeze_time("2024-11-25")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_count():
    assert len(parsed_items) == 7


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
        == "https://tarrant-agendamanagement-public.techsharetx.gov/publicportal/api/meetings/readArchived"  # noqa
    )


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "title": "Agenda",
            "href": "https://prod-agendamanagement-publicportal.azurewebsites.us/HtmlAgenda/94a0118f-4bf9-4be3-c33a-08dcfdc9934d",  # noqa
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == COMMISSION


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
