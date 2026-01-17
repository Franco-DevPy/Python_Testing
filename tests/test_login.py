from server import app

def test_login_email_not_valid():

    app.config['TESTING'] = True

    email = "noexiste@test.com"
    client = app.test_client()
    response = client.post('/showSummary', data={'email': email}, follow_redirects=True)

    assert response.status_code == 200
    assert b"Email not found." in response.data




