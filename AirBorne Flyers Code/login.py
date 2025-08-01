import subprocess
import sqlite3
from appJar import gui


# Connect to SQLite database
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

# Create users table if it doesn't exist
# User table defined with pk, username, password, gold column which is default = 0
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, gold INTEGER DEFAULT 0)''')
conn.commit()
# Connect to SQLite database
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

def register(username, password):
    try:
        # Insert new user data into the database
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return True  # Registration successful
    except sqlite3.IntegrityError:
        return False  # Username already exists


def login(username, password):
    # Check if the username and password match any user in the database
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    row = cursor.fetchone()
    if row:
        return True  # Login successful
    else:
        return False  # Login failed


def pressLogin(button):
    if button == "Login":
        username = app.getEntry("Username:")
        password = app.getEntry("Password:")
       
        success = login(username, password)  # Check if login is successful
        if success:
            app.infoBox("Success", "Login successful")
            app.stop()  # Stop the login GUI
            # this is now creating a file to store usernaem which can be accessed in other files.
            userRetrieve = open("uName.txt", "w")
            userRetrieve.write(username)
            userRetrieve.close()
            subprocess.run(["python", "MAINMENU.py"])
        else:
            app.errorBox("Error", "Invalid username or password")


def pressRegister(button):
    if button == "Register":
        app.clearEntry("Username:")
        app.clearEntry("Password:")
        app.clearEntry("New Username:")
        app.clearEntry("New Password:")
        app.showSubWindow("Register")
        app.setBgImage("plx-2.png")

def pressSubmit():
    username = app.getEntry("New Username:")
    password = app.getEntry("New Password:")
    if not username or not password:
        app.errorBox("Error", "Username and password cannot be empty")
    if register(username, password):
        app.infoBox("Success", "Registration successful")
        app.hideSubWindow("Register")
    else:
        app.errorBox("Error", "Username already exists")


# Create main login window
app = gui("Login", "600x400")
app.addLabelEntry("Username:")
app.addLabelSecretEntry("Password:")
app.addButton("Login", pressLogin)
app.addButton("Register", pressRegister)


# Create registration window (hidden by default)
app.startSubWindow("Register", modal=True)
app.addLabelEntry("New Username:")
app.addLabelSecretEntry("New Password:")
app.addButton("Submit", pressSubmit)
app.stopSubWindow()
app.setBgImage("plx-2.png")
app.go()
