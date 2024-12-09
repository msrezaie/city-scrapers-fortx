from datetime import datetime
from os.path import dirname, join
from unittest.mock import MagicMock, patch

import pytest
from city_scrapers_core.constants import COMMISSION
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fortx_Fort_Worth_Boards import FortxFortWorthBoardsSpider

test_response = file_response(
    join(dirname(__file__), "files", "fortx_Fort_Worth_Boards.json"),
    url="https://www.fortworthtexas.gov/ocapi/calendars/getcalendaritems?Ids=788ffb59-05d1-457d-b9dd-423d4b95a06e&LanguageCode=en-US",  # noqa
)
spider = FortxFortWorthBoardsSpider()

freezer = freeze_time("2024-10-04")
freezer.start()

parsed_item_data = [
    {
        "data": {
            "Title": "Notice of Public Comment for Brownsfields Program",
            "Description": "Notice of Public Comment for Analysis of Brownfields Cleanup Alternatives (ABCA) document prepared by the Brownsfields Program",  # noqa
            "Link": "https://www.fortworthtexas.gov/departments/citysecretary/events/2024-Public-Notice-Public-Comment",  # noqa
            "Image": None,
            "AltText": None,
            "Address": {
                "Venue": "",
                "Street": "",
                "Suburb": "Fort Worth",
                "PostCode": "",
                "Formatted": " Fort Worth",
            },
            "AdditionalInfo": [],
            "IsCancelled": False,
        },
        "success": True,
    },
    {
        "data": {
            "Title": "blank",
            "Description": "DFW International Airport Board Operations Committee",
            "Link": "https://www.fortworthtexas.gov/departments/citysecretary/events/blank-4.0",  # noqa
            "Image": None,
            "AltText": None,
            "Address": {
                "Venue": "Board Room – DFW Headquarters Building",
                "Street": "2400 Aviation Dr.",
                "Suburb": "DFW Airport",
                "PostCode": "75261",
                "Formatted": "",
            },
            "AdditionalInfo": [],
            "IsCancelled": False,
        },
        "success": True,
    },
    {
        "data": {
            "Title": "Blank",
            "Description": "for future use",
            "Link": "https://www.fortworthtexas.gov/departments/citysecretary/events/blank-3.5",  # noqa
            "Image": None,
            "AltText": None,
            "Address": {
                "Venue": "",
                "Street": "",
                "Suburb": "",
                "PostCode": "",
                "Formatted": "",
            },
            "AdditionalInfo": [],
            "IsCancelled": False,
        },
        "success": True,
    },
    {
        "data": {
            "Title": "blank",
            "Description": "For future use",
            "Link": "https://www.fortworthtexas.gov/departments/citysecretary/events/blank-3.0",  # noqa
            "Image": None,
            "AltText": None,
            "Address": {
                "Venue": "",
                "Street": "",
                "Suburb": "",
                "PostCode": "",
                "Formatted": "",
            },
            "AdditionalInfo": [],
            "IsCancelled": False,
        },
        "success": True,
    },
    {
        "data": {
            "Title": "Notice of Public Comment for Brownsfields Program",
            "Description": "Notice of Public Comment for Analysis of Brownfields Cleanup Alternatives (ABCA) document prepared by the Brownsfields Program",  # noqa
            "Link": "https://www.fortworthtexas.gov/departments/citysecretary/events/2024-Public-Notice-Public-Comment",  # noqa
            "Image": None,
            "AltText": None,
            "Address": {
                "Venue": "",
                "Street": "",
                "Suburb": "Fort Worth",
                "PostCode": "",
                "Formatted": " Fort Worth",
            },
            "AdditionalInfo": [],
            "IsCancelled": False,
        },
        "success": True,
    },
    {
        "data": {
            "Title": "Tax Increment Reinvestment Zone No. 8 (Lancaster Corridor TIF)",  # noqa
            "Description": "Tax Increment Reinvestment Zone No. 8 (Lancaster Corridor TIF)",  # noqa
            "Link": "https://www.fortworthtexas.gov/departments/citysecretary/events/tif-number-8-lancaster-corridor-2024",  # noqa
            "Image": None,
            "AltText": None,
            "Address": {
                "Venue": "City Hall",
                "Street": "200 Texas St",
                "Suburb": "Fort Worth",
                "PostCode": "76102",
                "Formatted": "City Hall, 200 Texas St, Fort Worth, 76102",
            },
            "AdditionalInfo": [],
            "IsCancelled": False,
        },
        "success": True,
    },
    {
        "data": {
            "Title": "Notice of Public Comment for Brownsfields Program",
            "Description": "Notice of Public Comment for Analysis of Brownfields Cleanup Alternatives (ABCA) document prepared by the Brownsfields Program",  # noqa
            "Link": "https://www.fortworthtexas.gov/departments/citysecretary/events/2024-Public-Notice-Public-Comment",  # noqa
            "Image": None,
            "AltText": None,
            "Address": {
                "Venue": "",
                "Street": "",
                "Suburb": "Fort Worth",
                "PostCode": "",
                "Formatted": " Fort Worth",
            },
            "AdditionalInfo": [],
            "IsCancelled": False,
        },
        "success": True,
    },
    {
        "data": {
            "Title": "DFW International Airport Board and Committee Meetings",
            "Description": "DFW International Airport Board and Committee Meetings",
            "Link": "https://www.fortworthtexas.gov/departments/citysecretary/events/dfw-airport-board-and-committees",  # noqa
            "Image": None,
            "AltText": None,
            "Address": {
                "Venue": "Board Room - DFW Headquarters Building",
                "Street": "2400 Aviation Dr., DFW Airport",
                "Suburb": "",
                "PostCode": "75261",
                "Formatted": "Board Room - DFW Headquarters Building, 2400 Aviation Dr., DFW Airport, 75261",  # noqa
            },
            "AdditionalInfo": [],
            "IsCancelled": False,
        },
        "success": True,
    },
    {
        "data": {
            "Title": "Downtown Design Review Board (DDRB)",
            "Description": "Enforce the Downtown Urban Design Standards (DDRB) for new construction and renovations by hearing and deciding applications for certificates of appropriateness in accordance with Section 4.1200; and Propose amendments to the Downtown Urban Design Standards to the City Zoning Commission and City Council from time to time. View agenda and meeting details.",  # noqa
            "Link": "https://www.fortworthtexas.gov/departments/citysecretary/events/downtown-design-review-board-2024",  # noqa
            "Image": None,
            "AltText": None,
            "Address": {
                "Venue": "City Hall",
                "Street": "200 Texas St",
                "Suburb": "Fort Worth",
                "PostCode": "76102",
                "Formatted": "City Hall, 200 Texas St, Fort Worth, 76102",
            },
            "AdditionalInfo": [],
            "IsCancelled": False,
        },
        "success": True,
    },
    {
        "data": {
            "Title": "Library Advisory Board Meeting (LAB)",
            "Description": "LAB recommends to the City Manager and the City Council plans for the development of Library facilities and services to meet the needs of the City. It reviews and comments on the annual operating budget and capital improvement requests. View agenda and meeting details.",  # noqa
            "Link": "https://www.fortworthtexas.gov/departments/citysecretary/events/library-advisory-board-2024",  # noqa
            "Image": None,
            "AltText": None,
            "Address": {
                "Venue": "Southwest Regional Branch Library",
                "Street": "4001 Library Lane",
                "Suburb": "Fort Worth",
                "PostCode": "76109",
                "Formatted": "Southwest Regional Branch Library, 4001 Library Lane, Fort Worth, 76109",  # noqa
            },
            "AdditionalInfo": [],
            "IsCancelled": False,
        },
        "success": True,
    },
    {
        "data": {
            "Title": "Notice of Public Comment for Brownsfields Program",
            "Description": "Notice of Public Comment for Analysis of Brownfields Cleanup Alternatives (ABCA) document prepared by the Brownsfields Program",  # noqa
            "Link": "https://www.fortworthtexas.gov/departments/citysecretary/events/2024-Public-Notice-Public-Comment",  # noqa
            "Image": None,
            "AltText": None,
            "Address": {
                "Venue": "",
                "Street": "",
                "Suburb": "Fort Worth",
                "PostCode": "",
                "Formatted": " Fort Worth",
            },
            "AdditionalInfo": [],
            "IsCancelled": False,
        },
        "success": True,
    },
    {
        "data": {
            "Title": "Business Equity Advisory Board",
            "Description": "Business Equity Advisory Board formerly the Minority and Women Business Enterprise (MWBE)",  # noqa
            "Link": "https://www.fortworthtexas.gov/departments/citysecretary/events/business-equity-advisory-board-mwbe-2024",  # noqa
            "Image": None,
            "AltText": None,
            "Address": {
                "Venue": "New City Hall, 7th Floor Training Rooms 0734 & 0735",
                "Street": "100 Fort Worth Trail",
                "Suburb": "Fort Worth",
                "PostCode": "76104",
                "Formatted": "New City Hall, 7th Floor Training Rooms 0734 & 0735, 100 Fort Worth Trail, Fort Worth, 76104",  # noqa
            },
            "AdditionalInfo": [],
            "IsCancelled": False,
        },
        "success": True,
    },
    {
        "data": {
            "Title": "Zoning Commission",
            "Description": "Advisory board to the City Council in regard to zoning matters within the City of Fort Worth.  View agenda and meeting details.",  # noqa
            "Link": "https://www.fortworthtexas.gov/departments/citysecretary/events/zoning-commission-agenda-2024",  # noqa
            "Image": None,
            "AltText": None,
            "Address": {
                "Venue": "Old City Hall",
                "Street": "200 Texas St",
                "Suburb": "Fort Worth",
                "PostCode": "76102",
                "Formatted": "Old City Hall, 200 Texas St, Fort Worth, 76102",
            },
            "AdditionalInfo": [],
            "IsCancelled": False,
        },
        "success": True,
    },
    {
        "data": {
            "Title": "Collective Bargaining",
            "Description": "Fort Worth Professional Fire Fighters Association,\r\nalso known as the International Association of Fire Fighters,\r\nLocal Union 440, as the exclusive bargaining agent on behalf of all\r\nFire Fighters of the City of Fort Worth Fire Department,\r\npursuant to the Collective Bargaining Process",  # noqa
            "Link": "https://www.fortworthtexas.gov/departments/citysecretary/events/collective-bargaining-fire-2024",  # noqa
            "Image": None,
            "AltText": None,
            "Address": {
                "Venue": "IAFF Local 440 Office",
                "Street": "3855 Tulsa Way",
                "Suburb": "Fort Worth",
                "PostCode": "76107",
                "Formatted": "IAFF Local 440 Office, 3855 Tulsa Way, Fort Worth, 76107",
            },
            "AdditionalInfo": [],
            "IsCancelled": False,
        },
        "success": True,
    },
    {
        "data": {
            "Title": "Tax Increment Reinvestment Zone No. 3 (Downtown TIF)",
            "Description": "Tax Increment Reinvestment Zone No. 3 (Downtown TIF)",
            "Link": "https://www.fortworthtexas.gov/departments/citysecretary/events/tif-number-3-downtown",  # noqa
            "Image": None,
            "AltText": None,
            "Address": {
                "Venue": "Old City Hall, Council Conference Room 2020",
                "Street": "200 Texas Street, Fort Worth Texas 76102",
                "Suburb": "Fort Worth",
                "PostCode": "76102",
                "Formatted": "Old City Hall, Council Conference Room 2020, 200 Texas Street, Fort Worth Texas 76102, Fort Worth, 76102",  # noqa
            },
            "AdditionalInfo": [],
            "IsCancelled": False,
        },
        "success": True,
    },
    {
        "data": {
            "Title": "Community Development Council",
            "Description": "The Community Development Council was established for the purpose of assisting the City Council in setting priorities for projects to be initiated with Federal funding and complying with Federal grant requirements and limitations of the United States Department of Housing and Urban Development. View agendas and details on meetings.",  # noqa
            "Link": "https://www.fortworthtexas.gov/departments/citysecretary/events/community-development-council-2024",  # noqa
            "Image": None,
            "AltText": None,
            "Address": {
                "Venue": "New City Hall",
                "Street": "100 Fort Worth Trail",
                "Suburb": "Fort Worth",
                "PostCode": "76102",
                "Formatted": "New City Hall, 100 Fort Worth Trail, Fort Worth, 76102",
            },
            "AdditionalInfo": [],
            "IsCancelled": False,
        },
        "success": True,
    },
    {
        "data": {
            "Title": "Mayor's Committee on Persons with Disabilities (MCPD)",
            "Description": "Mayor's Committee on Persons with Disabilities (MCPD) is an organization of citizen volunteers working together with the Fort Worth Human Relations Commission to increase public awareness of the abilities of persons with disabilities and promote employment opportunities and housing accessibility. View agenda and meeting details.",  # noqa
            "Link": "https://www.fortworthtexas.gov/departments/citysecretary/events/mayors-committee-person-disabilities-human-relations-2024",  # noqa
            "Image": None,
            "AltText": None,
            "Address": {
                "Venue": "Hazel Harvey Peace Center for Neighborhoods Lucille B. Smith Training Room",  # noqa
                "Street": "818 Missouri Avenue",
                "Suburb": "Fort Worth",
                "PostCode": "76104",
                "Formatted": "Hazel Harvey Peace Center for Neighborhoods Lucille B. Smith Training Room, 818 Missouri Avenue, Fort Worth, 76104",  # noqa
            },
            "AdditionalInfo": [],
            "IsCancelled": False,
        },
        "success": True,
    },
    {
        "data": {
            "Title": "Fort Worth After School Coordinating Board Meeting",
            "Description": "Fort Worth After School Coordinating Board Meeting",
            "Link": "https://www.fortworthtexas.gov/departments/citysecretary/events/2024-fort-worth-after-school",  # noqa
            "Image": None,
            "AltText": None,
            "Address": {
                "Venue": "Como Community Center",
                "Street": "4660 Horne Street",
                "Suburb": "Fort Worth",
                "PostCode": "76107",
                "Formatted": "Como Community Center, 4660 Horne Street, Fort Worth, 76107",  # noqa
            },
            "AdditionalInfo": [],
            "IsCancelled": False,
        },
        "success": True,
    },
]
with patch("requests.get") as mock_get:
    mocks = []
    for data in parsed_item_data:
        mock = MagicMock()
        mock.json.return_value = data
        mocks.append(mock)

    mock_get.side_effect = mocks
    parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_count():
    assert len(parsed_items) == 18


def test_title():
    assert (
        parsed_items[0]["title"] == "Notice of Public Comment for Brownsfields Program"
    )
    assert (
        parsed_items[1]["title"]
        == "DFW International Airport Board Operations Committee"
    )


def test_description():
    assert (
        parsed_items[0]["description"]
        == "Notice of Public Comment for Analysis of Brownfields Cleanup Alternatives (ABCA) document prepared by the Brownsfields Program"  # noqa
    )
    assert (
        parsed_items[1]["description"]
        == "DFW International Airport Board Operations Committee"
    )


def test_start():
    assert parsed_items[0]["start"] == datetime(2024, 10, 1, 0, 0)
    assert parsed_items[1]["start"] == datetime(2024, 10, 1, 12, 30)


def test_end():
    assert parsed_items[0]["end"] is None


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert (
        parsed_items[0]["id"]
        == "fortx_Fort_Worth_Boards/202410010000/x/notice_of_public_comment_for_brownsfields_program"  # noqa
    )


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {"name": "", "address": "Fort Worth, TX"}
    assert parsed_items[1]["location"] == {
        "name": "Board Room – DFW Headquarters Building",
        "address": "2400 Aviation Dr., DFW Airport, 75261, TX",
    }
    assert parsed_items[5]["location"] == {
        "name": "City Hall",
        "address": "200 Texas St, Fort Worth, 76102, TX",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://www.fortworthtexas.gov/calendar/boards-commission"
    )


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "title": "Link",
            "href": "https://www.fortworthtexas.gov/departments/citysecretary/events/2024-Public-Notice-Public-Comment",  # noqa
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == COMMISSION


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
