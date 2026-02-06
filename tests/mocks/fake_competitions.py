FAKE_COMPETITIONS = [

    # TEST: valid booking
    {
        "name": "Competition Large Future",
        "date": "2030-01-01 10:00:00",
        "numberOfPlaces": "30"
    },

    # TEST: not enough places
    {
        "name": "Competition One Place",
        "date": "2030-01-01 10:00:00",
        "numberOfPlaces": "1"
    },

    #  TEST: past competition
    {
        "name": "Competition Past",
        "date": "2020-01-01 10:00:00",
        "numberOfPlaces": "30"
    },

    # TEST: limit 12 places
    {
        "name": "Competition Limit Test",
        "date": "2030-01-01 10:00:00",
        "numberOfPlaces": "50"
    }

]
