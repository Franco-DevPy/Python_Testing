from server import app

def test_cannot_purchase_more_places_than_points(reset_data):
    app.config["TESTING"] = True

    client = app.test_client()
    purchasePlaces = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Iron Temple',
        'places': "15"
    })




    assert b"Great-booking complete!" not in purchasePlaces.data
    assert b"You cannot book more places than you have points." in purchasePlaces.data




