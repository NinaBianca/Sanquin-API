import os
import sys

# Adjust the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)

# sample data
sample_timeslot = {
    "location_id": 1,
    "start_time": "2021-01-01T00:00:00+00:00",
    "end_time": "2021-01-01T01:00:00+00:00",
    "total_capacity": 10,
    "remaining_capacity": 10,
}
sample_location = {
    "name": "Test Location",
    "address": "Test City",
    "opening_hours": "9:00 AM - 5:00 PM",
    "latitude": "123.456",
    "longitude": "123.456",
    "timeslots": [sample_timeslot],
}
sample_location_response = {
    "id": 1,
    "name": "Test Location",
    "address": "Test City",
    "opening_hours": "9:00 AM - 5:00 PM",
    "latitude": "123.456",
    "longitude": "123.456",
    "timeslots": [sample_timeslot],	
}
sample_donation = {
    "amount": 100.0,
    "user_id": 1,
    "location_id": 1,
    "type": "blood",
    "appointment": "2021-01-01T00:00:00+00:00",
    "status": "pending",
}
sample_update_donation = {
    "id": 1,
    "amount": 200.0,
    "user_id": 1,
    "location_id": 1,
    "type": "blood",
    "appointment": "2021-01-01T00:00:00+00:00",
    "status": "completed",
}


# --- Donation Routes Tests ---
# Test for creating a donation
@patch("routers.donations.create_donation", return_value=sample_donation)
@patch("routers.donations.check_user_exists", return_value=True)
def test_create_donation_route(create_donation, check_user_exists):
    response = client.post("/donations/", json=sample_donation)
    assert response.status_code == 200
    assert response.json()["message"] == "Donation created successfully"

@patch("routers.donations.create_donation", return_value=sample_donation)
@patch("routers.donations.check_user_exists", return_value=False)
def test_create_donation_route_user_not_found(get_donation_by_id, check_user_exists):
    response = client.post("/donations/", json=sample_donation)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found with ID 1"

# Test for getting donations by user ID
@patch("routers.donations.get_donations_by_user_id", return_value=[sample_donation])
@patch("routers.donations.check_user_exists", return_value=True)
def test_get_donations_by_user_id_route(get_donations_by_user_id, check_user_exists):
    response = client.get("/donations/user/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Donations retrieved successfully"

@patch("routers.donations.get_donation_by_id", return_value=sample_donation)
@patch("routers.donations.check_user_exists", return_value=False)
def test_get_donations_by_user_id_route_not_found(get_donation_by_id, check_user_exists):
    response = client.get("/donations/user/2")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found with ID 2"


# Test for deleting a donation
@patch("routers.donations.delete_donation", return_value=True)
@patch("routers.donations.check_donation_exists", return_value=True)
def test_delete_donation_route(delete_donation, check_donation_exists):
    response = client.delete("/donations/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Donation deleted successfully"

@patch("routers.donations.delete_donation", return_value=True)
@patch("routers.donations.check_donation_exists", return_value=False)
def test_delete_donation_route_not_found(delete_donation, check_donation_exists):
    response = client.delete("/donations/2")
    assert response.status_code == 404
    assert response.json()["detail"] == "Donation not found with ID 2"


# Test for updating a donation
@patch("routers.donations.update_donation", return_value=sample_update_donation)
@patch("routers.donations.check_donation_exists", return_value=True)
def test_update_donation_route(update_donation, check_donation_exists):
    response = client.put("/donations/1", json=sample_donation)
    assert response.status_code == 200
    assert response.json()["message"] == "Donation updated successfully"

@patch("routers.donations.update_donation", return_value=sample_update_donation)
@patch("routers.donations.check_donation_exists", return_value=False)
def test_update_donation_route_not_found(update_donation, check_donation_exists):
    response = client.put("/donations/2", json=sample_donation)
    assert response.status_code == 404
    assert response.json()["detail"] == "Donation not found with ID 2"


# Test for getting a donation by ID
@patch("routers.donations.get_donation_by_id", return_value=sample_donation)
@patch("routers.donations.check_donation_exists", return_value=True)
def test_get_donation_route(get_donation_by_id, check_donation_exists):
    response = client.get("/donations/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Donation retrieved successfully"

@patch("routers.donations.check_donation_exists", return_value=False)
def test_get_donation_route_not_found(check_donation_exists):
    response = client.get("/donations/2")
    assert response.status_code == 404
    assert response.json()["detail"] == "Donation not found with ID 2"

# --- Location Routes Tests ---
# Test for getting location info by city
@patch("routers.donations.get_location_info_by_city", return_value=[sample_location])
def test_get_location_info_by_city_route(get_location_info_by_city):
    response = client.get("/donations/location/Test City")
    assert response.status_code == 200
    assert response.json()["message"] == "Location(s) retrieved successfully"

# Test for getting timeslots by location
@patch("routers.donations.get_timeslots_by_location", return_value=[sample_timeslot])
def test_get_timeslots_by_location_route(get_timeslots_by_location):
    response = client.get("/donations/location/Test City/timeslots")
    assert response.status_code == 200
    assert response.json()["message"] == "Timeslots retrieved successfully"

# Test for creating location info
@patch("routers.donations.create_location_info", return_value=sample_location)
def test_create_location_info_route(create_location_info):
    response = client.post("/donations/location", json=sample_location)
    assert response.status_code == 200
    assert response.json()["message"] == "Location created successfully"

# Test for updating location info
@patch("routers.donations.update_location_info", return_value=sample_location)
def test_update_location_info_route(update_location_info):
    response = client.put("/donations/location/1", json=sample_location)
    assert response.status_code == 200
    assert response.json()["message"] == "Location updated successfully"

# Test for deleting location info
@patch("routers.donations.delete_location_info", return_value=True)
def test_delete_location_info_route(delete_location_info):
    response = client.delete("/donations/location/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Location deleted successfully"