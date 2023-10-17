import requests
import pytest

BASE_URL = "http://localhost:80/api/v3"


def check_if_pet_exists(pet_id):
    # Send a GET request to check if the pet with the given ID exists.
    response = requests.get(f"{BASE_URL}/pet/{pet_id}")

    # Check if the response status code is 200 (Pet exists) or 404 (Pet not found).
    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        # Return None for other status codes (e.g., 400 - Invalid ID supplied).
        return False

pet_data = [
    {"id": 1001, "name": "Pet1", "status": "available"},
    {"id": 1024, "name": "Pet2", "status": "pending"},
    {"id": 300, "name": "Pet3", "status": "sold"},
]
@pytest.mark.parametrize("pet_info", pet_data)
def test_add_new_pet(pet_info):
    # Check if the pet already exists.
    pet_id = pet_info["id"]

    pet_exists = check_if_pet_exists(pet_id)

    # If the pet doesn't exist, add a new pet and verify it returns a 200 status code.
    assert(pet_exists==False)
    if not pet_exists:
        response = requests.post(f"{BASE_URL}/pet", json={
            "id": pet_id,
            "name": "TestPet",
            "status": "available"
        })
        assert response.status_code == 200



@pytest.mark.parametrize("pet_id", [ 1, 10, 300])
def test_delete_pet(pet_id):

    pet_exists = check_if_pet_exists(pet_id)

    assert(pet_exists==True)
    if pet_exists:
        response = requests.delete(f"{BASE_URL}/pet/{pet_id}")
        assert response.status_code == 200
        verify_deleted_response = requests.get(f"{BASE_URL}/pet/{pet_id}")
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


def test_place_order():
    order_statuses = ["placed", "approved", "delivered"]
    
    for order_status in order_statuses:
        order_data = {
            "id": 10,
            "petId": 198772,
            "quantity": 7,
            "shipDate": "2023-10-17T17:49:08.712Z",
            "status": order_status,
            "complete": True
        }

        # Place an order with the current order status
        response = requests.post(f"{BASE_URL}/store/order", json=order_data)

        # Check if the response status code is 200, indicating a successful order placement.
        assert response.status_code == 200

        # Optionally, you can check the response content to further validate.
        response_data = response.json()
        assert response_data["status"] == order_status

        # Ensure the shipDate is slightly different (updated by the server)
        assert response_data["shipDate"] != order_data["shipDate"]






