#import pandas as pd
import sqlite3

def create_connection():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    try:
        command = "CREATE TABLE table_users (user_id INT NOT NULL PRIMARY KEY, user_name TEXT NOT NULL, user_pass TEXT NOT NULL);"
        cursor.execute(command)
        connection.commit()
        cursor.close()
        connection.close()
        print("Database created")
    except Exception as e:
        print("Database creation failed")
        print("Error: " + str(e))
        cursor.close()
        connection.close()

def create_user(user_data):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    if user_exists(user_data["username"]) is False:
        try:
            cursor.execute("SELECT user_id FROM table_users")
            fetch = cursor.fetchall()
            if len(fetch) >= 1:
                new_id = int(fetch[-1][0]) + 1
            else:
                new_id = 0
            cursor.execute("INSERT INTO table_users VALUES(?, ?, ?)", (new_id, user_data["username"], user_data["password"],))
            connection.commit()
            print("New user added successfully")
        except Exception as e:
            print("New user failed to be added")
            print("Error: " + str(e))
    else:
        print("New user failed to be added, username exists")
    cursor.close()
    connection.close()

def user_exists(username):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM table_users WHERE user_name = ?", (username,))
    if len(cursor.fetchall()) >= 1:
        cursor.close()
        connection.close()
        return True #The user exists
    else:
        cursor.close()
        connection.close()
        return False #The user does not exist
    
def user_getID(username):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM table_users WHERE user_name = ?", (username,))
    fetch = cursor.fetchall()
    if len(fetch) >= 1:
        user_id = fetch[0][0]
    else:
        user_id = None
    cursor.close()
    connection.close()
    return user_id
    
def user_check_confirmation(user_id):
    user_info = {}
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM table_users WHERE user_id = ?", (user_id,))
    for item in cursor.fetchall():
        user_info["id"] = item[0]
        user_info["username"] = item[1]
    cursor.close()
    connection.close()
    return user_info

def user_delete(username):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM table_users WHERE user_name = ?", (username,))
    connection.commit()
    cursor.close()
    connection.close()