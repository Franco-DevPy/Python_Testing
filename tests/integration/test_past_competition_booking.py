from unittest.mock import patch
import server
from server import app

from tests.mocks.fake_clubs import FAKE_CLUBS
from tests.mocks.fake_competitions import FAKE_COMPETITIONS


@patch("server.clubs", FAKE_CLUBS)
@patch("server.competitions", FAKE_COMPETITIONS)
def test_cannot_book_past_competition():

    app.config['TESTING'] = True
    client = app.test_client()

    response = client.get("/book/Competition%20Past/Club%20High%20Points")

    assert b"How many places?" not in response.data
    assert b"You cannot book places for past competitions." in response.data
