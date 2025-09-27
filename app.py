import mysql.connector
import sys
from getpass import getpass


def launch():
    """Get user info with prompts {hostname, port, username, password}"""
    credentials = {
    "hostname": None,
    "port": None,
    "username": None,
    "password": None,
    }

    for key in credentials:
        prompt = (f"Enter {key} >> ")

        if key == "password":
            credentials[key] = getpass(prompt) # just hides the passwd

        else:
            credentials[key] = input(prompt)

    return credentials


def login_db(credentials):
    """Log into MySQL database"""

    try:
        my_db = mysql.connector.connect(
            hostname = credentials["hostname"],
            port = credentials["port"],
            user = credentials["username"],
            passwd = credentials["password"],
        )

        print("Connected Successfully.")

        return my_db


    except:
        sys.exit("Could not login to host with user/password provided.")


if __name__ == "__main__":
    credentials = launch()


    my_db = login_db(credentials)


    while my_db:
        my_cursor = my_db.cursor()


        my_cursor.execute("SHOW VARIABLES like 'version'")


        print(my_db)


        my_result = my_cursor.fetchall()


        for row in my_result:
            print(row)

