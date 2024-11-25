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
            password BLOB NOT NULL,
            CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
        )''',
    "get_all_users": '''SELECT * FROM Users''',
    "get_user_by_id": '''SELECT * FROM Users WHERE uid = ?''',
    "get_user_by_username": '''SELECT * FROM Users WHERE username = ?''',
    "insert_new_user": '''INSERT INTO Users (username, password) VALUES (?, ?)''',
    "delete_user": '''DELETE FROM Users WHERE uid = ?'''
}



def connect_to_db():
    """Connects to the database"""
    conn = sqlite3.connect('Fridge.db')
    return conn

def open_or_create_user_table():
    """Ensures Users table is always created."""
    db = connect_to_db()
    cursor = db.cursor()

    #Create table to store app users
    try:
        cursor.execute(db_commands["create_user_table"])
        db.commit()
    except sqlite3.OperationalError as CreateError:
        raise CreateError("Failed to create Users table")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()



"""Users table CRUD Operation"""

def create_user(user: UserCreate) -> UserResponse | None:
    """Create new user in the database"""
    db = None
    cursor = None
    try:
        open_or_create_user_table()
        db = connect_to_db()
        cursor = db.cursor()

        hashed_password = hash_password(user.password)

        cursor.execute(db_commands["insert_new_user"], (user.username, hashed_password,))

        db.commit()

        cursor.execute(db_commands["get_user_by_id"], (cursor.lastrowid,))

        entity = cursor.fetchone()
        if entity:  # Ensure we got a result (we should though as we know the user is created)
            new_user = UserResponse(
                uid=entity[UID],
                username=entity[USERNAME],
                CreatedAt=entity[CREATED_AT]
            )
        else:
            new_user = None

    except sqlite3.IntegrityError as AlreadyExistsError:
        raise ValueError("Username already exists") from AlreadyExistsError

    except sqlite3.DatabaseError as CreateError:
        raise CreateError(f"Database error: {str(CreateError)}") from CreateError

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


def read_users() -> list[UserResponse]:
    """Get all users in the Users table"""
    users: list[UserResponse] = []
    db = None
    cursor = None
    try:
        open_or_create_user_table()
        db = connect_to_db()
        cursor = db.cursor()

        cursor.execute(db_commands["get_all_users"])
        entities = cursor.fetchall()

        # if not entities:
        #     return users  # Explicit return if no users found

        for entity in entities:
            user = UserResponse(
                        uid=entity[UID], 
                        username=entity[USERNAME], 
                        CreatedAt=entity[CREATED_AT]
                    )
            users.append(user)

    except sqlite3.OperationalError as GetError:
        print(f"Error fetching users: {GetError}")
        raise Exception("Failed to get all users") from GetError

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
        
    return users

def read_user_by_password(user:UserCreate) -> UserResponse | None:
    signed_in_user:UserResponse = None;
    try:
        open_or_create_user_table()
        db = connect_to_db()
        cursor = db.cursor()

        cursor.execute(db_commands["get_user_by_username"], (user.username,))
        entity = cursor.fetchone()
        if entity:
            stored_password:bytes = entity[PASSWORD]
            if(is_correct_password((user.password), stored_password)):
                signed_in_user = UserResponse(
                uid=entity[UID], 
                username=entity[USERNAME], 
                CreatedAt=entity[CREATED_AT]
            )
    except sqlite3.Error as SignInError:
        raise Exception("Failed to sign in") from SignInError
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    return signed_in_user



def read_user_by_id(user_id) -> UserResponse | None:
    """Fetch specfic user from the database"""
    found_user:UserResponse = None
    db = None
    cursor = None
    try:
        open_or_create_user_table()
        db = connect_to_db()
        cursor = db.cursor()

        cursor.execute(db_commands["get_user_by_id"], (user_id,))
        entity = cursor.fetchone()

        if entity:
            found_user = UserResponse(
                uid=entity[UID], 
                username=entity[USERNAME], 
                CreatedAt=entity[CREATED_AT]
            )

    except sqlite3.OperationalError as GetError:
        print(f"Error fetching users: {GetError}")
        raise Exception("Failed to get user") from GetError

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
        
    return found_user


# def update_user(user_id:int, user_password:int) -> UserResponse | None:
#     """Update user's password in the database"""
#     open_or_create_user_table()
#     db = connect_to_db()
#     cursor = db.cursor()

#     change_password_query:str = "UPDATE Users SET password = ? WHERE uid = ?;"

#     cursor.execute(change_password_query, (user_password, user_id))
#     db.commit()

#     cursor.execute("SELECT * FROM Users WHERE uid = ?", (user_id,))

#     entity = cursor.fetchone()
#     if entity is None:
#         return None
#     new_user = UserResponse(uid=entity[UID], username=entity[USERNAME], CreatedAt=entity[CREATED_AT])

#     cursor.close()
#     db.close()

#     return new_user
    

import sqlite3

def delete_user(user_id: int):
    db = None
    cursor = None

    try:
        open_or_create_user_table()
        db = connect_to_db()
        cursor = db.cursor()
        cursor.execute(db_commands["delete_user"], (user_id,))
        db.commit()
        if cursor.rowcount == 0:
            raise ValueError(f"No user found with ID {user_id}")  # Optional: check if a user was deleted
    except sqlite3.OperationalError as DeletionError:
        db.rollback()  # Rollback in case of an error
        print(f"Error occurred when deleting user with ID {user_id}: {DeletionError}")
        raise  DeletionError("Failed to delete user") from DeletionError
    finally:
        cursor.close()
        db.close()


"""Helper methods"""
from bcrypt import hashpw, gensalt, checkpw

def hash_password(password: str) -> bytes:
    """Encrypt user's password"""
    salt = gensalt()  # Generate a salt
    hashed_password = hashpw(password.encode('utf-8'), salt)  # Hash the password with the salt
    return hashed_password  # Return as bytes (bcrypt returns binary data, no need to decode)

def is_correct_password(attempted_password: str, actual_password: bytes) -> bool:
    """Check if the attempted password matches the actual password"""
    return checkpw(attempted_password.encode('utf-8'), actual_password)  # Check using bcrypt's checkpw


# def hash_password(password: str):
#     """Encrypt user's password"""
#     salt = gensalt()
#     hashed_password = hashpw(password.encode('utf-8'), salt)
#     return hashed_password.decode('utf-8')  # Store as a string in the DB
# def is_correct_password(attempted_password:str, actual_password:str) -> bool:
#     return checkpw(attempted_password.encode(), actual_password)
