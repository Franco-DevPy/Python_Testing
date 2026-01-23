import server
from server import app

def test_points_display_board(reset_data):
    app.config["TESTING"] = True
    client = app.test_client()

    response = client.get("/displayBoard")

    assert response.status_code == 200
    assert b"Club Points Board" in response.data
