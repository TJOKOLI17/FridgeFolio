import sqlite3
from ..api.models.ItemModel import ItemModel


def open_or_create_fridge_tables():
    """Ensures Items table is always created."""
    db = sqlite3.connect('Fridge.db')
    cursor = db.cursor()

    #Create table to store app users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    #Create table to store fridge items
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Items(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount INTEGER NOT NULL,
            expDate TEXT NOT NULL
        )
    ''')

    #Create table to store deleted items
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deletedItems(
            id INTEGER,
            name TEXT NOT NULL,
            amount INTEGER NOT NULL,
            expDate TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='trigger' AND name='item_deletion_validation';
    ''')
    trigger_exists_val = cursor.fetchone()

    if not trigger_exists_val:
        cursor.execute('''
            CREATE TRIGGER item_deletion_validation
            BEFORE DELETE ON Items
            WHEN NOT (OLD.amount = 0 OR DATE(REPLACE(OLD.expDate, '/', '-')) < DATE('now'))
            BEGIN
                SELECT RAISE(ABORT, 'Item can only be deleted if the quantity is 0 or it is expired');
            END;
        ''')

    cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='trigger' AND name='item_deletion';
    ''')
    trigger_exists = cursor.fetchone()

    if not trigger_exists:
        # Create the trigger to log deletions
        cursor.execute('''
            CREATE TRIGGER item_deletion
            AFTER DELETE ON Items
            BEGIN
                INSERT INTO deletedItems (id, name, amount, expDate) VALUES (OLD.id, OLD.name, OLD.amount, OLD.expDate);
            END;
        ''')
    
    cursor.close()
    db.commit()
    db.close()


"""Items table CRUD Operation"""
def create(item: ItemModel) -> ItemModel:
    """Create new item in the database"""
    open_or_create_fridge_tables()
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
    open_or_create_fridge_tables()
    db = sqlite3.connect('Fridge.db')
    cursor = db.cursor()
    items: list[ItemModel] = []

    cursor.execute('''SELECT * FROM Items ORDER BY expDate''')
    rows = cursor.fetchall()

    if not rows:
        return []

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


def read_deleted() -> list[ItemModel]:
    """Fetch all deleted entries from the database"""
    open_or_create_fridge_tables()
    db = sqlite3.connect('Fridge.db')
    cursor = db.cursor()
    items: list[ItemModel] = []

    cursor.execute('''SELECT * FROM deletedItems ORDER BY expDate''')
    rows = cursor.fetchall()
    if not rows:
        return []
    
    for row in rows:
        item = ItemModel(
            id = row[0],
            name = row[1],
            amount = row[2],
            expDate = row[3]
        )
        items.append(item)

    cursor.close()
    db.close()
    return items


def read_by_id(item_id) -> list[ItemModel] | None:
    """Fetch specfic entry from the database"""
    open_or_create_fridge_tables()
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
    open_or_create_fridge_tables()
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
    

def delete(item_id: int):
    open_or_create_fridge_tables()
    db = sqlite3.connect('Fridge.db')
    cursor = db.cursor()

    try:
        cursor.execute(f"DELETE FROM Items WHERE id = ?", (item_id,))
        db.commit()
    except sqlite3.IntegrityError as e:
        print(f"Deletion failed: {e}")
    finally:
        cursor.close()
        db.close()
