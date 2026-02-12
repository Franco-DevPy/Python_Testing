from unittest import mock
from server import app
import server
from tests.mocks.fake_clubs import FAKE_CLUBS
from tests.mocks.fake_competitions import FAKE_COMPETITIONS

@mock.patch("server.saveCompetitions")
@mock.patch("server.saveClubs")
@mock.patch("server.clubs", FAKE_CLUBS)
@mock.patch("server.competitions", FAKE_COMPETITIONS)
def test_cannot_purchase_more_places_than_points(   saveClubs, saveCompetitions):

    app.config["TESTING"] = True
    client = app.test_client()

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "Competition Large Future",
            "club": "Club Low Points",
            "places": "10"
        },
    )

    assert b"Great-booking complete!" not in response.data
    assert b"You cannot book more places than you have points." in response.data
