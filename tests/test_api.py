import pytest
import sqlite3
import uuid
from fastapi.testclient import TestClient
from backend.api.main import app
from backend.database.items_database import open_or_create_fridge_tables
from backend.database.users_database import open_or_create_user_table

client = TestClient(app)

# Sample Data for Testing
item_data = {
    "uid": 1,
    "name": "Milk",
    "amount": 3,
    "expDate": "2024-12-31"
}

user_data = {
    "username": "testuser",
    "password": "testpassword123"
}


# Fixture to create and clean up resources after each test
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Fixture to set up the database before running tests."""
    open_or_create_fridge_tables()
    open_or_create_user_table()

    yield

    db = sqlite3.connect('Fridge.db')
    cursor = db.cursor()
    cursor.execute("DELETE FROM Items")
    cursor.execute("DELETE FROM Users")
    cursor.execute("DELETE FROM deletedItems")
    db.commit()
    cursor.close()
    db.close()


### ITEM TESTS ###

def test_create_new_item():
    """Test creating a new item in the fridge."""
    response = client.post("/items/", json=item_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Milk"
    assert response.json()["amount"] == 3

def test_get_all_items():
    """Test fetching all items in the fridge."""
    response = client.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_user_items():
    """Test fetching all items for a specific user."""
    # Create an item first
    client.post("/items/", json=item_data)
    response = client.get("/items/1")  # Assuming user ID is 1
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_item():
    """Test updating an item in the fridge."""
    # Create an item
    create_response = client.post("/items/", json=item_data)
    assert create_response.status_code == 200
    item_id = create_response.json()["id"]
    update_data = {
        "uid": 1,
        "id": item_id,
        "name": "Milk",
        "amount": 5,
        "expDate": "2024-12-31"
    }
    # Update the item
    update_response = client.put("/items/", json=update_data)
    assert update_response.status_code == 200
    assert update_response.json()["amount"] == 5

def test_delete_existing_item():
    """Test deleting an item from the fridge."""
    # Create an item
    create_response = client.post("/items/", json=item_data)
    assert create_response.status_code == 200
    item_id = create_response.json()["id"]
    # Delete the item
    delete_response = client.delete(f"/items/{item_id}/1")  # Assuming user ID is 1
    assert delete_response.status_code == 200

def test_get_deleted_items():
    """Test fetching all deleted items."""
    # Create and delete an item
    create_response = client.post("/items/", json=item_data)
    assert create_response.status_code == 200
    item_id = create_response.json()["id"]
    client.delete(f"/items/{item_id}/1")
    # Get deleted items
    response = client.get("/items/deleted")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


### USER TESTS ###

def test_create_new_user():
    """Test creating a new user with a unique username."""
    unique_username = f"testuser_{uuid.uuid4().hex[:6]}"
    unique_user_data = {
        "username": unique_username,
        "password": "testpassword123"
    }
    response = client.post("/users/", json=unique_user_data)
    assert response.status_code == 200
    assert response.json()["username"] == unique_username

def test_get_all_users():
    """Test fetching all users."""
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_user_by_password():
    """Test signing in using username and password."""
    client.post("/users/", json=user_data)
    response = client.get("/users/login", params={"username": "testuser", "password": "testpassword123"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_get_user_by_id():
    """Test fetching a user by ID."""
    unique_username = f"testuser_{uuid.uuid4().hex[:6]}"
    unique_user_data = {
        "username": unique_username,
        "password": "testpassword123"
    }
    # Create the user
    create_response = client.post("/users/", json=unique_user_data)
    assert create_response.status_code == 200

    # Get the user ID from the response
    user_id = create_response.json()["uid"]

    # Fetch the user by ID
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json()["username"] == unique_username

def test_delete_user():
    """Test deleting a user by ID."""
    unique_username = f"testuser_{uuid.uuid4().hex[:6]}"
    unique_user_data = {
        "username": unique_username,
        "password": "testpassword123"
    }

    # Create the user
    create_response = client.post("/users/", json=unique_user_data)
    assert create_response.status_code == 200, f"Failed to create user, status code: {create_response.status_code}"
    
    # Get the user ID from the response
    user_id = create_response.json()["uid"]

    # Delete the user
    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 200, f"Failed to delete user, status code: {delete_response.status_code}"

### EDGE CASE TESTS ###


def test_update_item_not_found():
    """Test updating an item that does not exist."""
    update_data = {
        "uid": 1,
        "id": 9999,
        "name": "Nonexistent",
        "amount": 10,
        "expDate": "2024-12-31"
    }
    response = client.put("/items/", json=update_data)
    assert response.status_code == 404  # Item not found

def test_get_user_not_found():
    """Test fetching a user that does not exist."""
    response = client.get("/users/9999")
    assert response.status_code == 404  # User not found

def test_delete_user_not_found():
    """Test deleting a user that does not exist."""
    response = client.delete("/users/9999")
    assert response.status_code == 404  # User not found