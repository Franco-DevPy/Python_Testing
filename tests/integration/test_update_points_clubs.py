import server
from server import app



def test_update_points_clubs(): 
    app.config["TESTING"] = True

    client = app.test_client()

    clubs = server.clubs
    competitions = server.competitions

    for club in clubs:
        if club["name"] == "Iron Temple":
            club["points"] = "10"

    for comp in competitions:
        if comp["name"] == "Winter Cup":
            comp["numberOfPlaces"] = "5"
            break

    response = client.post('/purchasePlaces', data={
        'competition': 'Winter Cup',
        'club': 'Iron Temple',
        'places': "3"
    })

    assert b"Great-booking complete!" in response.data
    assert b"Points available: 7" in response.data

