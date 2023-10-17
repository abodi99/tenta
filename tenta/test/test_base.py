import requests
import pytest

BASE_URL = "http://localhost:80/api/v3"

@pytest.fixture
def pet_id():
    response = requests.post(f"{BASE_URL}/pet", json={
        "id": 123,
        "name": "TestPet",
        "status": "available"
    })
    return response.json()['id']

def test_add_new_pet():
    response = requests.post(f"{BASE_URL}/pet", json={
        "id": 123,
        "name": "TestPet",
        "status": "available"
    })
    assert response.status_code == 200


def test_delete_pet():

    test_add_new_pet()
    # Delete the pet with the given petId
    response = requests.delete(f"{BASE_URL}/pet/123")

    # Check if the response status code is 200, indicating a successful delete request.
    assert response.status_code == 200

    # Optionally, you can check if the pet has been deleted by trying to retrieve it.
    verify_deleted_response = requests.get(f"{BASE_URL}/pet/123")
    assert verify_deleted_response.status_code == 404


@pytest.mark.parametrize("status", ["available", "pending", "sold"])
def test_find_pets_by_status(status):
    response = requests.get(f"{BASE_URL}/pet/findByStatus?status={status}")

    # Check if the response status code is 200, indicating a successful request.
    assert response.status_code == 200

    # Verify that the response contains pets with the expected status.
    pets = response.json()
    for pet in pets:
        assert pet["status"] == status

