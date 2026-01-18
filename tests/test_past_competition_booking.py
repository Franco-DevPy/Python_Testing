import server
from server import app

def test_cannot_book_past_competition(reset_data):
    app.config['TESTING'] = True
    client = app.test_client()
    competition = [comp for comp in server.competitions if comp["name"] == "Fall Classic"][0]
    competition["date"] = "2022-01-01 10:00:00" 
    
    response = client.get("/book/Fall%20Classic/Simply%20Lift")


    assert b"How many places?" not in response.data
    assert b"You cannot book places for past competitions." in response.data
