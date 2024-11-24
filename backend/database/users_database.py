import sqlite3
from ..api.models.UserModels import *
from bcrypt import hashpw, gensalt, checkpw

UID:int = 0
USERNAME:int = 1
PASSWORD:int = 2
CREATED_AT:int = 3

db_commands: dict[str, str] = {
    "create_user_table": '''CREATE TABLE IF NOT EXISTS Users(
            uid INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
        )''',
    "get_all_users": '''SELECT * FROM Users''',
    "get_user": '''SELECT * FROM Users WHERE uid = ?''',
    "insert_new_user": '''INSERT INTO Users (username, password) VALUES (?, ?)''',
}


def connect_to_db():
    conn = sqlite3.connect('Fridge.db')
    return conn

def open_or_create_user_table():
    """Ensures Users table is always created."""
    db = connect_to_db()
    cursor = db.cursor()

    #Create table to store app users
    try:
        cursor.execute(db_commands["create_user_table"])
    except sqlite3.OperationalError as CreateError:
        raise CreateError("Failed to create Users table")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    db.commit()


"""Users table CRUD Operation"""

def create(user: UserCreate) -> UserResponse | None:
    """Create new user in the database"""
    try:
        open_or_create_user_table()
        db = connect_to_db()
        cursor = db.cursor()

        hashed_password = hash_password(user.password)

        cursor.execute(db_commands["insert_new_user"], (user.username, hashed_password,))

        db.commit()

        cursor.execute(db_commands["get_user"], (cursor.lastrowid,))

        entity = cursor.fetchone()
        if entity:  # Ensure we got a result
            new_user = UserResponse(
                uid=entity[UID],
                username=entity[USERNAME],
                CreatedAt=entity[CREATED_AT]
            )
        else:
            new_user = None

    except sqlite3.IntegrityError as AlreadyExistsError:
        raise ValueError("Username already exists") from AlreadyExistsError

    except sqlite3.DatabaseError as db_error:
        raise db_error(f"Database error: {str(db_error)}") from db_error

    except Exception as e:
        # Log or raise unexpected errors
        print(f"Unexpected error: {str(e)}")
        raise e   
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    return new_user


def read() -> list[UserResponse]:
    """Fetch all entries in the Users table"""
    users: list[UserResponse] = []
    try:
        open_or_create_user_table()
        db = connect_to_db()
        cursor = db.cursor()

        cursor.execute(db_commands["get_all_users"])
        entities = cursor.fetchall()

        if not entities:
            return []  # Explicit return if no users found

        for entity in entities:
            user = UserResponse(
                        uid=entity[UID], 
                        username=entity[USERNAME], 
                        CreatedAt=entity[CREATED_AT]
                    )
            users.append(user)

    except sqlite3.OperationalError as GetError:
        # Log the error and raise a custom message
        print(f"Error fetching users: {GetError}")
        raise Exception("Failed to get all users") from GetError

    finally:
        # Ensure cursor and db are closed in the finally block
        if cursor:
            cursor.close()
        if db:
            db.close()
        
    return users



def read_by_id(user_id) -> UserResponse | None:
    """Fetch specfic entry from the database"""
    open_or_create_user_table()
    db = connect_to_db()
    cursor = db.cursor()
    
    cursor.execute(db_commands["get_user"], (user_id,))
    
    entity = cursor.fetchone()
    if(entity is None):
        return None
    found_user = UserResponse(uid=entity[UID], username=entity[USERNAME], CreatedAt=entity[CREATED_AT])

    cursor.close()
    db.close()
    return found_user


def update(user_id:int, user_password:int) -> UserResponse | None:
    """Update user's password in the database"""
    open_or_create_user_table()
    db = connect_to_db()
    cursor = db.cursor()

    change_password_query:str = "UPDATE Users SET password = ? WHERE uid = ?;"

    cursor.execute(change_password_query, (user_password, user_id))
    db.commit()

    cursor.execute("SELECT * FROM Users WHERE uid = ?", (user_id,))

    entity = cursor.fetchone()
    if entity is None:
        return None
    new_user = UserResponse(uid=entity[UID], username=entity[USERNAME], CreatedAt=entity[CREATED_AT])

    cursor.close()
    db.close()

    return new_user
    

def delete(user_id: int):
    open_or_create_user_table()
    db = connect_to_db()
    cursor = db.cursor()

    try:
        cursor.execute(f"DELETE FROM Users WHERE uid = ?", (user_id,))
        db.commit()
    except:
        print(f"Error occured when deleting user")
    finally:
        cursor.close()
        db.close()

"""Helper methods"""
def hash_password(password: str):
    """Encrypt user's password"""
    salt = gensalt()
    hashed_password = hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')  # Store as a string in the DB
