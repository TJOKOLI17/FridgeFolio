import sqlite3
# from fastapi import Depends
from ..api.model import ItemModel
db = sqlite3.connect('Fridge.db')
# session = Depends(db)
cursor = db.cursor()


def open_or_create_Items_table():
    """Ensures Items table is always created."""
    db = sqlite3.connect('Fridge.db')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Items(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount INTEGER NOT NULL,
            expDate TEXT NOT NULL
        )
    ''')
    
    cursor.close(), db.commit(), db.close()

def create(item: ItemModel) -> ItemModel:
    """Create new item in the database"""
    open_or_create_Items_table()
    db = sqlite3.connect('Fridge.db')
    cursor = db.cursor()

    cursor.execute( 
            "INSERT OR IGNORE INTO Items (name, amount, expDate) VALUES (?, ?, ?)", 
        (item.name, item.amount, item.expDate)
    )
    db.commit()

    cursor.execute("SELECT * FROM Items WHERE id = ?", (cursor.lastrowid,))

    entity = cursor.fetchone()
    new_item = ItemModel(id=entity[0], name=entity[1], amount=entity[2], expDate=entity[3])

    cursor.close(), db.close()

    return new_item

def read() -> list[ItemModel]:
    """Fetch all entries from the database"""
    open_or_create_Items_table()
    db = sqlite3.connect('Fridge.db')
    cursor = db.cursor()
    items: list[ItemModel] = []

    cursor.execute('''
        SELECT * FROM Items ORDER BY expDate ASC
    ''')
    rows = cursor.fetchall()

    for row in rows:
        item = ItemModel(
                    id=row[0], 
                    name=row[1],
                    amount=row[2],     
                    expDate=row[3]
                )
        items.append(item)

    cursor.close()
    db.close()
    return items

def read_by_id(item_id) -> list[ItemModel] | None:
    """Fetch specfic entry from the database"""
    open_or_create_Items_table()
    db = sqlite3.connect('Fridge.db')
    cursor = db.cursor()
    
    cursor.execute(f"SELECT * FROM Items WHERE id = ?", (item_id,))
    
    entity = cursor.fetchone()
    if(entity is None):
        return None
    found_item = ItemModel(id=entity[0], name=entity[1], amount=entity[2], expDate=entity[3])

    cursor.close()
    db.close()
    return found_item
          
def update(item_id:int, item_amount:int) -> ItemModel | None:
    """Update item's amount in the database"""
    open_or_create_Items_table()
    db = sqlite3.connect('Fridge.db')
    cursor = db.cursor()

    change_amount_query:str = "UPDATE Items SET amount = ? WHERE id = ?;"

    cursor.execute(change_amount_query, (item_amount, item_id))
    db.commit()

    cursor.execute("SELECT * FROM Items WHERE id = ?", (item_id,))

    entity = cursor.fetchone()
    if entity is None:
        return None
    new_item = ItemModel(id=entity[0], name=entity[1], amount=entity[2], expDate=entity[3])

    cursor.close()
    db.close()

    return new_item
    
def delete(item_id:int):
    open_or_create_Items_table()
    db = sqlite3.connect('Fridge.db')
    cursor = db.cursor()

    cursor.execute( f"DELETE FROM Items WHERE id = ?", (item_id,))
    db.commit()
    cursor.close(), db.close()