from unittest import mock
from unittest.mock import patch
import server
from server import app

from tests.mocks.fake_clubs import FAKE_CLUBS
from tests.mocks.fake_competitions import FAKE_COMPETITIONS

@mock.patch("server.saveCompetitions")
@mock.patch("server.saveClubs")
@patch("server.clubs", FAKE_CLUBS)
@patch("server.competitions", FAKE_COMPETITIONS)
def test_update_points_clubs(saveClubs, saveCompetitions):

    app.config["TESTING"] = True
    client = app.test_client()

    response = client.post('/purchasePlaces', data={
        'competition': 'Competition Large Future',
        'club': 'Club High Points',
        'places': "3"
    })

    assert b"Great-booking complete!" in response.data
    assert b"Points available: 17" in response.data
