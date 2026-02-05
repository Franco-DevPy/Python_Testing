import server
from server import app


def test_limit_places_competition(reset_data):

    app.config['TESTING'] = True
    client = app.test_client()

    competitions = server.competitions

    for comp in competitions:
        if comp["name"] == "Fall Classic":
            comp["numberOfPlaces"] = "25"
            break

    clubs = server.clubs

    for club in clubs:
        if club["name"] == "Simply Lift":
            club["points"] = "20"
            break

    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Fall Classic',
        'places': '13'
    })

    assert b"Great-booking complete!" not in response.data
    assert b'You cannot book more than 12 places per competition.' in response.data