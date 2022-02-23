import mysql.connector

import encryption

database = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="admin",
    database="chatroom"
)

# print(mydb)

cursor = database.cursor()


# check if username already registered
def check_username(username):
    sql = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(sql)
    result = cursor.fetchone()
    return result


# validates login password
def check_password(username, password):
    result = check_username(username)
    if result is None:
        return False
    else:
        if encryption.decrypt_password(result[2], password):
            return True
        else:
            return False


# register a new user
def register_user(username, password, user_type):
    if check_username(username) is None:
        password = encryption.encrypt_password(password)
        sql = "INSERT into users (username, password, user_type) VALUES (%s, %s, %s)"
        val = (username, password, user_type)
        cursor.execute(sql, val)
        database.commit()
        if cursor.rowcount > 0:
            return True
        else:
            print("something happened")
    else:
        return False


# storing public chat messages using encryption in the DB
def store_public_chat(username, message):
    message = encryption.encrypt_message(message)
    sql = "INSERT into chat_history (username, message) VALUES (%s, %s)"
    val = (username, message)
    cursor.execute(sql, val)
    database.commit()
    if cursor.rowcount > 0:
        pass
    else:
        print("Unable to store public chats")


# storing banned username and IP in the DB
def ban_user(username, ip_address):
    sql = "INSERT into ban_list (username, ip_address) VALUES (%s, %s)"
    val = (username, ip_address)
    cursor.execute(sql, val)
    database.commit()
    if cursor.rowcount > 0:
        pass
    else:
        print("Unable to ban user")


# checks if username already exists in the ban_list table
def check_username_banned(username):
    sql = "SELECT * FROM ban_list WHERE username = '" + username + "'"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result is None:
        return False
    else:
        return True


# checks if IP already exists in the ban_list table
def check_ip_banned(ip_address):
    sql = "SELECT * FROM ban_list WHERE ip_address = '" + ip_address + "'"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result is None:
        return False
    else:
        return True

# print(check_username("admin"))
# register_user("Suwadith", "wdp3YttyyX/LSQ==*vrQ7f2+vY6pWnj8+h1RRmA==*Bx+z56v6FL+BZD5SVZcU0g==*5GKS7GBWeTkrZbLisz7UZg==", "user")
# store_public_chat("Suwadith", "chat storage check 2")

# print(check_password("admin", "admin"))
