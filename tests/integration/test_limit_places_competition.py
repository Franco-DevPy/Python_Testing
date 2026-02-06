from unittest import mock
from server import app

from tests.mocks.fake_clubs import FAKE_CLUBS
from tests.mocks.fake_competitions import FAKE_COMPETITIONS


@mock.patch("server.clubs", FAKE_CLUBS)
@mock.patch("server.competitions", FAKE_COMPETITIONS)
def test_limit_places_competition():

    app.config["TESTING"] = True
    client = app.test_client()

    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Club Medium Points",
            "competition": "Competition Limit Test",
            "places": "13",
        },
    )

    assert b"Great-booking complete!" not in response.data
    assert b"You cannot book more than 12 places per competition." in response.data
