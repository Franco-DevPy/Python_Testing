from unittest import mock
import server
from server import app
from tests.mocks.fake_competitions import FAKE_COMPETITIONS
from tests.mocks.fake_clubs import FAKE_CLUBS
    


@mock.patch('server.competitions', FAKE_COMPETITIONS)
@mock.patch('server.clubs', FAKE_CLUBS)
def test_cannot_purchase_more_places_than_competition_allows():

    app.config["TESTING"] = True

    client = app.test_client()

    
    purchasePlaces = client.post('/purchasePlaces', data={
        'competition': 'Competition One Place',
        'club': 'Club Medium Points',
        'places': "2"
    })

    assert b"Great-booking complete!" not in purchasePlaces.data
    assert b"Not enough places available in the competition." in purchasePlaces.data