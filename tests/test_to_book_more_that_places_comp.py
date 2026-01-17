import server
from server import app, loadCompetitions



def test_cannot_purchase_more_places_than_competition_allows(reset_data):

    app.config["TESTING"] = True

    client = app.test_client()

    competitions = server.competitions

    for comp in competitions:
        if comp["name"] == "Spring Festival":
            comp["numberOfPlaces"] = "1"


    purchasePlaces = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Iron Temple',
        'places': "2"
    })

    assert b"Great-booking complete!" not in purchasePlaces.data
    assert b"Not enough places available in the competition." in purchasePlaces.data