import pytest
import os
import sqlite3

from rich import _console
from backend.api.models import ItemModel, UserModels
from backend.database.items_database import *
from backend.database.users_database import *

item_data1 = ItemModel(uid=1, name="Pizza", amount=5, expDate="2024-12-31")

item_data2 = ItemModel(uid=1, name="Bread", amount=2, expDate="2024-12-31")

item_data3 = ItemModel(uid=2, name="Milk", amount=3, expDate="2024-12-31")

user_data1 = UserCreate(username="testuser1", password="pw1")

user_data2 = UserCreate(username="testuser2", password="pw2")


# Fixture to create and clean up resources after each test
@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Fixture to set up the database before running tests."""
    
    open_or_create_fridge_tables()
    open_or_create_user_table()

    yield

    os.remove('Fridge.db')

### ITEM TESTS ###

def test_create_item():
    """Test adding an item to the fridge."""
    item = create_item(item_data1)
    assert item.id == 1
    assert item.uid == 1
    assert item.name == "Pizza"
    assert item.amount == 5
    assert item.expDate == "2024-12-31"

def test_read_items():
    """Test fetching all items in the fridge."""
    create_item(item_data1)
    create_item(item_data2)
    items = read_items()
    assert len(items) == 2
    assert items[0].name == "Pizza"
    assert items[1].name == "Bread"

def test_read_items_by_uid():
    """Test fetching items by user ID."""
    create_item(item_data1)
    create_item(item_data2)
    create_item(item_data3)
    items = read_items_by_uid(1)
    assert len(items) == 2
    assert items[0].name == "Pizza"
    assert items[1].name == "Bread"

# comment noted triggers in 'open_or_create_fridge_tables()' in items_database.py
def test_delete_item_by_uid_1():
    """Test deleting an item by user ID."""
    create_item(item_data1)
    create_item(item_data2)
    delete_item_by_uid(2, 1)
    items = read_items_by_uid(1)
    assert len(items) == 1

def test_delete_item_by_uid_2():
    """Test deleting an item by user ID for two users."""
    create_item(item_data1)
    create_item(item_data2)
    create_item(item_data3)
    delete_item_by_uid(2, 1)
    delete_item_by_uid(3, 2)
    items1 = read_items_by_uid(1)
    items2 = read_items_by_uid(2)
    assert len(items1) == 1
    assert len(items2) == 0

def test_read_deleted_items():
    """Test fetching all deleted items."""
    create_item(item_data1)
    create_item(item_data2)
    delete_item_by_uid(2, 1)
    items = read_deleted_items()
    assert len(items) == 1
    assert items[0].name == "Bread"

def test_read_deleted_items_by_uid():
    """Test fetching deleted items by user ID."""
    create_item(item_data1)
    create_item(item_data2)
    create_item(item_data3)
    delete_item_by_uid(2, 1)
    delete_item_by_uid(3, 2)
    items = read_deleted_items_by_uid(2)
    assert len(items) == 1
    assert items[0].name == "Milk"

### USER TESTS ###

def test_create_user_1():
    """Test adding a user to the database."""
    user = create_user(user_data1)
    assert user.uid == 1
    assert user.username == "testuser1"

def test_create_user_2():
    """Test adding a user to the database with a dictionary."""
    user1 = create_user(user_data1)
    user2 = create_user(user_data2)
    assert user2.uid == 2
    assert user2.username == "testuser2"

def test_create_user_3():
    """Test adding a user to the database with a dictionary."""
    user1 = create_user(user_data1)
    with pytest.raises(ValueError):
        create_user(user_data1)
    
def test_read_users():
    """Test fetching all users from the database."""
    create_user(user_data1)
    create_user(user_data2)
    users = read_users()
    assert len(users) == 2
    assert users[0].username == "testuser1"
    assert users[1].username == "testuser2"
    
def test_read_user_by_password():
    """Test fetching a user by password."""
    create_user(user_data1)
    user = read_user_by_password(UserCreate(username="testuser1", password="pw1"))
    assert user.uid == 1

def test_read_user_by_id_1():
    """Test fetching a user by ID."""
    create_user(user_data1)
    user = read_user_by_id(1)
    assert user.uid == 1
    assert user.username == "testuser1"

def test_read_user_by_id_2():
    """Test fetching a user by ID."""
    create_user(user_data1)
    create_user(user_data2)
    user = read_user_by_id(2)
    assert user.uid == 2
    assert user.username == "testuser2"

def test_delete_user():
    """Test deleting a user from the database."""
    create_user(user_data1)
    assert read_user_by_id(1)

    delete_user(1)
    users = read_users()
    assert len(users) == 0
    assert not read_user_by_id(1)

