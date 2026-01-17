import copy
import pytest
import server 

@pytest.fixture
def reset_data():
    
    original_clubs = copy.deepcopy(server.clubs)
    original_competitions = copy.deepcopy(server.competitions)

    yield  

   
    server.clubs = original_clubs
    server.competitions = original_competitions
