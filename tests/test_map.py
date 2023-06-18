import pytest

# Import the distance function from your module
from app.app import distance, unbound, MAP_SIZE

# Test cases

def test_distance_valid_coordinates():
    # Test case 1: Testing distance at the center of the map
    assert distance((16, 16),(16,16)) == 0
    assert distance((16, 16),(17,16)) == 1
    assert distance((17, 16),(16,16)) == 1
    assert distance((16, 17),(16,16)) == 1
    assert distance((16, 16),(16,17)) == 1
    assert distance((0, 0),(16,16)) == 24
    assert distance((0, 0),(0,16)) == 16
    assert distance((16, 16),(16,0)) == 16
    assert distance((16, 16),(17,17)) == 1.5
    

def test_distance_invalid_coordinates():
    with pytest.raises(ValueError):
        distance((-1, 0),(0,0))  # Invalid negative coordinate
    with pytest.raises(ValueError):
        distance((MAP_SIZE + 1, MAP_SIZE),(0,0))  # Invalid coordinate exceeding the maximum
    with pytest.raises(ValueError):
        distance((MAP_SIZE/2, -1),(0,0))  # Invalid negative coordinate
    with pytest.raises(ValueError):
        distance((MAP_SIZE/2, MAP_SIZE + 1),(0,0))  # Invalid coordinate exceeding the maximum

    with pytest.raises(ValueError):
        distance((0, 0),(-1,0))  # Invalid negative coordinate
    with pytest.raises(ValueError):
        distance((0,0),(MAP_SIZE + 1, MAP_SIZE))  # Invalid coordinate exceeding the maximum
    with pytest.raises(ValueError):
        distance((0,0),(MAP_SIZE/2, -1))  # Invalid negative coordinate
    with pytest.raises(ValueError):
        distance((0,0),(MAP_SIZE/2, MAP_SIZE + 1))  # Invalid coordinate exceeding the maximum

def test_unbound():
    assert unbound((-1, 0))  # Invalid negative coordinate
    assert unbound((0, -1))  # Invalid negative coordinate
    assert unbound((MAP_SIZE + 1, 0))  # Invalid negative coordinate
    assert unbound((0, MAP_SIZE + 1))  # Invalid negative coordinate


# Run the tests
pytest.main()
