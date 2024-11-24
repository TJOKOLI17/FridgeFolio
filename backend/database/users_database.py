import sqlite3
from ..api.models.UserModel import UserModel
from bcrypt import hashpw, gensalt, checkpw


def open_or_create_fridge_tables():
    """Ensures Users table is always created."""
    db = sqlite3.connect('Fridge.db')
    cursor = db.cursor()

    #Create table to store app users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userusername TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.close()
    db.commit()
    db.close()


"""Users table CRUD Operation"""
def create(user: UserModel) -> UserModel:
    """Create new user in the database"""
    open_or_create_fridge_tables()
    db = sqlite3.connect('Fridge.db')
    cursor = db.cursor()

    cursor.execute( 
            "INSERT OR IGNORE INTO Users (username, password) VALUES (?, ?, ?)", 
        (user.username, user.password, user.expDate)
    )
    db.commit()

    cursor.execute("SELECT * FROM Users WHERE id = ?", (cursor.lastrowid,))

    entity = cursor.fetchone()
    new_user = UserModel(id=entity[0], username=entity[1], password=entity[2])

    cursor.close(), db.close()

    return new_user


def read() -> list[UserModel]:
    """Fetch all entries in the Users table"""
    open_or_create_fridge_tables()
    db = sqlite3.connect('Fridge.db')
    cursor = db.cursor()
    users: list[UserModel] = []

    cursor.execute('''SELECT * FROM Users ORDER BY expDate''')
    rows = cursor.fetchall()

    if not rows:
        return []

    for row in rows:
        user = UserModel(
                    id=row[0], 
                    username=row[1],
                    password=row[2],     
                    expDate=row[3]
                )
        users.append(user)

    cursor.close()
    db.close()
    return users


def read_by_id(user_id) -> list[UserModel] | None:
    """Fetch specfic entry from the database"""
    open_or_create_fridge_tables()
    db = sqlite3.connect('Fridge.db')
    cursor = db.cursor()
    
    cursor.execute(f"SELECT * FROM Users WHERE id = ?", (user_id,))
    
    entity = cursor.fetchone()
    if(entity is None):
        return None
    found_user = UserModel(id=entity[0], username=entity[1], password=entity[2])

    cursor.close()
    db.close()
    return found_user


def update(user_id:int, user_password:int) -> UserModel | None:
    """Update user's password in the database"""
    open_or_create_fridge_tables()
    db = sqlite3.connect('Fridge.db')
    cursor = db.cursor()

    change_password_query:str = "UPDATE Users SET password = ? WHERE id = ?;"

    cursor.execute(change_password_query, (user_password, user_id))
    db.commit()

    cursor.execute("SELECT * FROM Users WHERE id = ?", (user_id,))

    entity = cursor.fetchone()
    if entity is None:
        return None
    new_user = UserModel(id=entity[0], username=entity[1], password=entity[2])

    cursor.close()
    db.close()

    return new_user
    

def delete(user_id: int):
    open_or_create_fridge_tables()
    db = sqlite3.connect('Fridge.db')
    cursor = db.cursor()

    try:
        cursor.execute(f"DELETE FROM Users WHERE id = ?", (user_id,))
        db.commit()
    except:
        print(f"Error occured when deleting user")
    finally:
        cursor.close()
        db.close()
