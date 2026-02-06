from unittest import mock
from server import app

from tests.mocks.fake_clubs import FAKE_CLUBS


@mock.patch("server.clubs", FAKE_CLUBS)
def test_points_display_board():

    app.config["TESTING"] = True
    client = app.test_client()

    response = client.get("/displayBoard")

    assert response.status_code == 200
    assert b"Club Points Board" in response.data
