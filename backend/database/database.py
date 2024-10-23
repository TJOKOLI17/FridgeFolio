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
    open_or_create_Items_table()
    db = sqlite3.connect('Fridge.db')
    cursor = db.cursor()
    items: list[ItemModel] = []
    """Fetch all entries from the database"""
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
        

    
# def update_item():
    
def delete(item_id:int):
    open_or_create_Items_table()
    db = sqlite3.connect('Fridge.db')
    cursor = db.cursor()

    cursor.execute( f"DELETE FROM Items WHERE id = ?", (item_id,))
    db.commit()