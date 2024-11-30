import pytest
from backend.database.database import open_or_create_fridge_tables, create, read, read_deleted, read_by_id, update, delete

# tests_db.py

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    open_or_create_fridge_tables()

def test_create():
    item = {"name": "apple", "amount": 5, "expDate": "2024/12/31"}
    result = create(item)
    assert result["name"] == "apple"
    assert result["amount"] == 5
    assert result["expDate"] == "2024/12/31"

def test_read():
    items = read()
    assert isinstance(items, list)
    assert len(items) > 0

def test_read_deleted():
    deleted_items = read_deleted()
    assert isinstance(deleted_items, list)

def test_read_by_id():
    item = {"name": "banana", "amount": 3, "expDate": "2024/11/15"}
    added_item = create(item)
    item_id = added_item["id"]
    fetched_item = read_by_id(item_id)
    assert fetched_item["id"] == item_id
    assert fetched_item["name"] == "banana"

def test_update():
    item = {"name": "carrot", "amount": 2, "expDate": "2024/10/31"}
    added_item = create(item)
    item_id = added_item["id"]
    updated_item = {"id": item_id, "name": "carrot", "amount": 10, "expDate": "2024/10/31"}
    result = update(updated_item)
    assert result["amount"] == 10

def test_delete():
    item = {"name": "milk", "amount": 1, "expDate": "2024/12/01"}
    added_item = create(item)
    item_id = added_item["id"]
    delete(item_id)
    fetched_item = read_by_id(item_id)
    assert fetched_item is None

# def test_get_all_items():
#     items = get_all_items()
#     assert isinstance(items, list)
#     assert len(items) > 0

# def test_get_deleted_items():
#     deleted_items = get_deleted_items()
#     assert isinstance(deleted_items, list)