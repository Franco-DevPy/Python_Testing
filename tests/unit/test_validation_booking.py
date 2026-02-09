from server import validate_booking


def test_negative_places():
    result = validate_booking(
        placesRequired=-1,
        club_points=10,
        competition_places=10,
        competition_date="2026-12-31 10:00:00"
    )
    assert result == "NEGATIVE_PLACES"


def test_total_booking_limit_exceeded():

    fake_competition = {
        "name": "Competition Max Places",
        "date": "2030-01-01 10:00:00",
        "numberOfPlaces": "50",
        "bookings": [
            {"club_id": 1, "places": 8}
        ]
    }

    result = validate_booking(
        placesRequired=8,
        club_points=20,
        competition_places=20,
        competition_date="2026-12-31 10:00:00",
        club_id=1,
        competition=fake_competition
    )

    assert result == "TOTAL_BOOKING_LIMIT_EXCEEDED"


def test_past_competition():
    result = validate_booking(
        placesRequired=1,
        club_points=10,
        competition_places=10,
        competition_date="2020-01-01 10:00:00"
    )
    assert result == "PAST_COMPETITION"


def test_too_many_places():
    result = validate_booking(
        placesRequired=13,
        club_points=20,
        competition_places=20,
        competition_date="2026-12-31 10:00:00"
    )
    assert result == "TOO_MANY_PLACES"


def test_not_enough_places():
    result = validate_booking(
        placesRequired=5,
        club_points=10,
        competition_places=3,
        competition_date="2026-12-31 10:00:00"
    )
    assert result == "NOT_ENOUGH_PLACES"


def test_not_enough_points():
    result = validate_booking(
        placesRequired=5,
        club_points=3,
        competition_places=10,
        competition_date="2026-12-31 10:00:00"
    )
    assert result == "NOT_ENOUGH_POINTS"


def test_valid_booking():
    result = validate_booking(
        placesRequired=5,
        club_points=10,
        competition_places=10,
        competition_date="2026-12-31 10:00:00"
    )
    assert result == "OK"
