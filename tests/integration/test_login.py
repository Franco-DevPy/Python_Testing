from unittest import mock
from server import app

from tests.mocks.fake_clubs import FAKE_CLUBS


@mock.patch("server.clubs", FAKE_CLUBS)
def test_login_email_not_valid():

    app.config["TESTING"] = True
    client = app.test_client()

    email = "noexiste@test.com"

    response = client.post(
        "/showSummary",
        data={"email": email},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Email not found." in response.data
