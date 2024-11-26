import sqlite3
from ..api.models.ItemModel import ItemModel

ID:int = 0
UID:int = 1
NAME:int = 2
AMOUNT:int = 3
EXPDATE:int = 4

db_commands: dict[str, str] = {
    "create_items_table": '''
        CREATE TABLE IF NOT EXISTS Items(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uid INTEGER NOT NULL,
            name TEXT NOT NULL,
            amount INTEGER NOT NULL,
            expDate TEXT NOT NULL,
            FOREIGN KEY (uid) REFERENCES Users(uid) ON DELETE CASCADE ON UPDATE CASCADE
        )
    ''',
    "create_deleted_items_table": 
        '''
            CREATE TABLE IF NOT EXISTS deletedItems(
                id INTEGER NOT NULL,
                uid INTEGER NOT NULL,
                name TEXT NOT NULL,
                amount INTEGER NOT NULL,
                expDate TEXT NOT NULL,
                FOREIGN KEY (uid) REFERENCES Users(uid) ON DELETE CASCADE ON UPDATE CASCADE
            )
        ''',
    "create_item_deletion_validation_trigger": 
        '''
            CREATE TRIGGER item_deletion_validation
                BEFORE DELETE ON Items
                WHEN NOT (OLD.amount = 0 OR DATE(REPLACE(OLD.expDate, '/', '-')) < DATE('now'))
                BEGIN
                    SELECT RAISE(ABORT, 'Item can only be deleted if the quantity is 0 or it is expired');
                END;
        ''',
    "create_item_deletion_trigger": 
        '''
            CREATE TRIGGER item_deletion
            AFTER DELETE ON Items
            BEGIN
                INSERT INTO deletedItems (id, uid,name, amount, expDate) VALUES (OLD.id, OLD.uid, OLD.name, OLD.amount, OLD.expDate);
            END;
        ''',

    "confirm_item_deletion_validation_trigger_exists":'''SELECT name FROM sqlite_master WHERE type='trigger' AND name='item_deletion_validation';''',
    "confirm_item_deletion_trigger_exists":'''SELECT name FROM sqlite_master WHERE type='trigger' AND name='item_deletion';''',
    
    "get_all_items": '''SELECT * FROM Items ORDER BY expDate''',
    "get_all_items_by_uid": '''SELECT * FROM Items WHERE uid = ? ORDER BY expDate''',
    "get_item_by_id_and_uid": '''SELECT * FROM Items WHERE id = ? AND uid = ? ORDER BY expDate''',
    "get_item_by_name_and_uid": '''SELECT * FROM Items WHERE name = ? and uid = ? ORDER BY expDate''',
    
    "get_all_deleted_items": '''SELECT * FROM deletedItems ORDER BY expDate''',
    "get_all_deleted_items_by_uid": '''SELECT * FROM deletedItems WHERE uid = ? ORDER BY expDate''',
    
    "insert_new_item":'''INSERT OR IGNORE INTO Items (uid, name, amount, expDate) VALUES (?, ?, ?, ?)''',
    
    "update_amount_query": "UPDATE Items SET amount = ? WHERE id = ? AND uid = ?;",
    
    "delete_item_and_uid": '''DELETE FROM Items WHERE id = ? and uid = ?'''
}

def connect_to_db():
    """Connects to the database."""
    conn = sqlite3.connect('Fridge.db')
    return conn


def open_or_create_fridge_tables():
    """Ensures Items table is always created."""
    db = connect_to_db()
    cursor = db.cursor()

    # Create table to store fridge items
    cursor.execute(db_commands["create_items_table"])

    # Create table to store deleted items
    cursor.execute(db_commands["create_deleted_items_table"])

    # Confirm item_deletion_validation_trigger exists
    cursor.execute(db_commands["confirm_item_deletion_validation_trigger_exists"])
    trigger_exists_val = cursor.fetchone()

    # Create item_deletion_validation_trigger
    if not trigger_exists_val:
        cursor.execute(db_commands["create_item_deletion_validation_trigger"])

    # Confirm item_deletion_trigger exists
    cursor.execute(db_commands["confirm_item_deletion_trigger_exists"])
    trigger_exists = cursor.fetchone()

    if not trigger_exists:
        # Create item_deletion_trigger to log deletions
        cursor.execute(db_commands["create_item_deletion_trigger"])
    
    cursor.close()
    db.commit()
    db.close()


"""Items table CRUD Operations"""

def create_item(item: ItemModel) -> ItemModel:
    """Create new item in the database"""
    open_or_create_fridge_tables()
    db = connect_to_db()
    cursor = db.cursor()

    cursor.execute(db_commands["insert_new_item"], (item.uid, item.name, item.amount, item.expDate,))
    
    db.commit()

    cursor.execute(db_commands["get_item_by_id_and_uid"], (cursor.lastrowid, item.uid,))


    entity = cursor.fetchone()
    new_item = ItemModel(
                    id=entity[ID], 
                    uid=entity[UID], 
                    name=entity[NAME], 
                    amount=entity[AMOUNT], 
                    expDate=entity[EXPDATE]
                )

    cursor.close(), db.close()

    return new_item

def read_items() -> list[ItemModel]:
    """Fetch all entries from the database"""
    open_or_create_fridge_tables()
    db = connect_to_db()
    cursor = db.cursor()
    items: list[ItemModel] = []

    # cursor.execute('''DROP TRIGGER IF EXISTS item_deletion;''')

    cursor.execute(db_commands["get_all_items"])
    rows = cursor.fetchall()

    if not rows:
        return []

    for row in rows:
        item = ItemModel(
                    id=row[ID], 
                    uid=row[UID],
                    name=row[NAME],
                    amount=row[AMOUNT],     
                    expDate=row[EXPDATE]
                )
        
        items.append(item)

    cursor.close()
    db.close()
    return items


def read_items_by_uid(user_id:int) -> list[ItemModel]:
    """Fetch all user's entries from the database"""
    open_or_create_fridge_tables()
    db = connect_to_db()
    cursor = db.cursor()
    user_items: list[ItemModel] = []

    cursor.execute(db_commands["get_all_items_by_uid"], (user_id,))
    rows = cursor.fetchall()

    if not rows:
        return []

    for row in rows:
        user_item = ItemModel(
                    id=row[ID], 
                    uid=row[UID],
                    name=row[NAME],
                    amount=row[AMOUNT],     
                    expDate=row[EXPDATE]
                )
        
        user_items.append(user_item)

    cursor.close()
    db.close()
    return user_items


def read_deleted_items() -> list[ItemModel]:
    """Fetch all deleted entries from the database"""
    open_or_create_fridge_tables()
    db = connect_to_db()
    cursor = db.cursor()
    user_deleted_items: list[ItemModel] = []

    cursor.execute(db_commands["get_all_deleted_items"])
    rows = cursor.fetchall()
    if not rows:
        return []
    
    for row in rows:
        user_deleted_item = ItemModel(
                    id=row[ID], 
                    uid=row[UID],
                    name=row[NAME],
                    amount=row[AMOUNT],     
                    expDate=row[EXPDATE]
                )
        user_deleted_items.append(user_deleted_item)

    cursor.close()
    db.close()
    return user_deleted_items

def read_deleted_items_by_uid(user_id:int) -> list[ItemModel]:
    """Fetch user's deleted entries from the database"""
    open_or_create_fridge_tables()
    db = connect_to_db()
    cursor = db.cursor()
    items: list[ItemModel] = []

    cursor.execute(db_commands["get_all_deleted_items_by_uid"], (user_id,))
    rows = cursor.fetchall()
    if not rows:
        return []
    
    for row in rows:
        item = ItemModel(
                    id=row[ID], 
                    uid=row[UID],
                    name=row[NAME],
                    amount=row[AMOUNT],     
                    expDate=row[EXPDATE]
                )
        items.append(item)

    cursor.close()
    db.close()
    return items


def read_item_by_id(item_id) -> ItemModel | None:
    """Fetch specfic entry from the database"""
    # open_or_create_fridge_tables()
    # db = connect_to_db()
    # cursor = db.cursor()
    
    # cursor.execute(f"SELECT * FROM Items WHERE id = ? and uid = ?", (item_id,))
    
    # entity = cursor.fetchone()
    # if(entity is None):
    #     return None
    # found_item = ItemModel(
    #                 id=entity[ID], 
    #                 uid=entity[UID], 
    #                 name=entity[NAME], 
    #                 amount=entity[AMOUNT], 
    #                 expDate=entity[EXPDATE]
    #             )

    # cursor.close()
    # db.close()
    # return found_item


def update_item_uid(user_id:int, item_id:int, item_amount:int) -> ItemModel | None:
    """Update a user's item's amount in the database"""
    open_or_create_fridge_tables()
    db = connect_to_db()
    cursor = db.cursor()

    cursor.execute(db_commands["update_amount_query"], (item_amount, item_id, user_id,))
    db.commit()

    cursor.execute(db_commands["get_item_by_id_and_uid"], (item_id, user_id,))

    entity = cursor.fetchone()
    if entity is None:
        return None
    updated_item = ItemModel(
                    id=entity[ID], 
                    uid=entity[UID], 
                    name=entity[NAME], 
                    amount=entity[AMOUNT], 
                    expDate=entity[EXPDATE]
                )

    cursor.close()
    db.close()

    return updated_item
    

def delete_item_by_uid(item_id:int, user_id:int):
    """Delete a user's item"""
    open_or_create_fridge_tables()
    db = connect_to_db()
    cursor = db.cursor()

    try:
        cursor.execute(f"DELETE FROM Items WHERE id = ? and uid = ?", (item_id, user_id,))
        db.commit()
    except sqlite3.IntegrityError as e:
        print(f"Deletion failed: {e}")
    finally:
        cursor.close()
        db.close()