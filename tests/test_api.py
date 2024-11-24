# test_api.py
import pytest
from fastapi.testclient import TestClient
from backend.api.main import app
from backend.database.database import open_or_create_fridge_tables

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    open_or_create_fridge_tables()


# Test to verify adding an item using POST request
def test_create_item_successfully():
    response = client.post("/", json={
        "name": "apple",
        "amount": 5,
        "expDate": "2024/12/31"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "apple"
    assert data["amount"] == 5
    assert data["expDate"] == "2024/12/31"


# Test to verify fetching all items using GET request
def test_get_all_items_successfully():
    response = client.get("/")
    assert response.status_code == 200
    items = response.json()
    assert len(items) > 0  # Assumes there is at least one item already


# Test to verify fetching a specific item using GET by ID
def test_get_item_by_id_successfully():
    create_response = client.post("/", json={
        "name": "banana",
        "amount": 3,
        "expDate": "2024/11/15"
    })
    assert create_response.status_code == 200
    item_id = create_response.json()["id"]

    response = client.get(f"/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == "banana"


# Test to verify getting an item by ID that does not exist
def test_get_item_by_invalid_id_returns_404():
    response = client.get("/99999")
    assert response.status_code == 404


# Test to verify updating an item successfully using PUT request
def test_update_item_successfully():
    # First, add an item to update
    create_response = client.post("/", json={
        "name": "carrot",
        "amount": 2,
        "expDate": "2024/10/31"
    })
    assert create_response.status_code == 200
    item_id = create_response.json()["id"]

    # Update the item
    updated_response = client.put("/", json={
        "id": item_id,
        "name": "carrot",
        "amount": 10,  # Updating the amount
        "expDate": "2024/10/31"
    })
    assert updated_response.status_code == 200
    updated_item = updated_response.json()
    assert updated_item["amount"] == 10


# Test to verify updating an item that does not exist
def test_update_item_invalid_id_returns_404():
    response = client.put("/", json={
        "id": 99999,  # Assuming 99999 does not exist
        "name": "nonexistent",
        "amount": 1,
        "expDate": "2024/12/31"
    })
    assert response.status_code == 404


# Test to verify deleting an item successfully
def test_delete_item_successfully():
    # First, add an item to delete
    create_response = client.post("/", json={
        "name": "milk",
        "amount": 1,
        "expDate": "2024/12/01"
    })
    assert create_response.status_code == 200
    item_id = create_response.json()["id"]

    # Delete the item
    delete_response = client.delete(f"/{item_id}")
    assert delete_response.status_code == 200

    # Confirm that the item no longer exists
    get_response = client.get(f"/{item_id}")
    assert get_response.status_code == 404


# Test to verify deleting an item that does not exist
def test_delete_item_invalid_id_returns_404():
    response = client.delete("/99999")  # Assuming 99999 does not exist
    assert response.status_code == 404


# Test to verify fetching deleted items from the "trash" using GET request
def test_get_all_deleted_items_successfully():
    response = client.get("/deleted")
    assert response.status_code == 200
    # Expecting an empty list or some items if they were already deleted
    deleted_items = response.json()
    assert isinstance(deleted_items, list)

# Test creating an item with a missing field
def test_create_item_missing_field():
    response = client.post("/", json={
        "name": "apple",
        "expDate": "2024/12/31"  # Missing 'amount'
    })
    assert response.status_code == 422  # Unprocessable Entity

# Test creating an item with invalid data type
def test_create_item_invalid_data_type():
    response = client.post("/", json={
        "name": "apple",
        "amount": "five",  # Invalid data type (should be int)
        "expDate": "2024/12/31"
    })
    assert response.status_code == 422  # Unprocessable Entity

# Test updating an item with invalid data (negative amount)
def test_update_item_with_negative_amount():
    # Add an item first
    create_response = client.post("/", json={
        "name": "carrot",
        "amount": 2,
        "expDate": "2024/10/31"
    })
    assert create_response.status_code == 200
    item_id = create_response.json()["id"]

    # Try to update with a negative amount
    response = client.put("/", json={
        "id": item_id,
        "name": "carrot",
        "amount": -10,  # Invalid value
        "expDate": "2024/10/31"
    })
    assert response.status_code == 422  # Unprocessable Entity or 400 Bad Request

# Test deleting an item that was already deleted
def test_delete_item_twice():
    # Add and then delete the item
    create_response = client.post("/", json={
        "name": "milk",
        "amount": 1,
        "expDate": "2024/12/01"
    })
    assert create_response.status_code == 200
    item_id = create_response.json()["id"]

    delete_response = client.delete(f"/{item_id}")
    assert delete_response.status_code == 200

    # Try to delete the same item again
    second_delete_response = client.delete(f"/{item_id}")
    assert second_delete_response.status_code == 404



