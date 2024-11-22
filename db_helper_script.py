import argparse
import sqlite3

def get_all_items():
    """Fetch all items from the Items table."""
    db = sqlite3.connect('Fridge.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Items")
    items = cursor.fetchall()
    cursor.close()
    db.close()
    return items

def print_items_from_db():
    """Print all items from the Items table."""
    items = get_all_items()

    if items:
        print("Items in the database:")
        for item in items:
            print(f"ID: {item[0]}, Name: {item[1]}, Amount: {item[2]}, Expiration Date: {item[3]}")
    else:
        print("No items in the database.")

def get_all_deleted_items():
    """Fetch all deleted items from the deletedItems table."""
    db = sqlite3.connect('Fridge.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM deletedItems")
    deleted_items = cursor.fetchall()
    cursor.close()
    db.close()
    return deleted_items

def print_deleted_items():
    """Print all deleted items from the deletedItems table."""
    deleted_items = get_all_deleted_items()

    if deleted_items:
        print("Deleted items in the database:")
        for item in deleted_items:
            print(f"ID: {item[0]}, Name: {item[1]}, Amount: {item[2]}, Expiration Date: {item[3]}")
    else:
        print("No deleted items in the database.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Database Helper Script")
    parser.add_argument("--print_items", action="store_true", help="Print all items in the database")
    parser.add_argument("--print_deleted_items", action="store_true", help="Print all deleted items in the database")

    args = parser.parse_args()

    if args.print_items:
        print_items_from_db()

    if args.print_deleted_items:
        print_deleted_items()
