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
            host = credentials["hostname"],
            port = credentials["port"],
            user = credentials["username"],
            passwd = credentials["password"],
        )

        print("Connected Successfully.")

        return my_db


    except Exception as e:
        print(e)
        sys.exit("Could not login to host with user/password provided.")


def show_version(my_cursor):
    """Simply show the version of MySQL after logging in"""
    my_cursor.execute("SHOW VARIABLES LIKE 'version'")
    print(my_cursor.fetchone())


def prompt_word(my_cursor, my_db):
    """Add word to database if it doesn't exist. Change word in database if it does exist."""
    first_word = input("What word would you like to add/change >> ")

    # See if word is in database already!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    my_cursor.execute(f"SELECT word FROM dictionary.word WHERE word = '{first_word}'")
    check = my_cursor.fetchone()


    if check:
        print(f"Found '{first_word}' in the database.")
        print(check)

        second_word = input(f"Change {first_word} to >> ")
        my_cursor.execute(f"UPDATE dictionary.word SET word = '{second_word}' WHERE word = '{first_word}'")

        print(f"Changed '{first_word}' to '{second_word}' in the database")
    

    else:
        print(f"The word '{first_word}' was not found... adding")
        my_cursor.execute(f"INSERT INTO dictionary.word (word) VALUES ('{first_word}')")

    my_db.commit()

def main():
    # Get the user login details
    credentials = launch()

    # boring init
    my_db = login_db(credentials)
    my_cursor = my_db.cursor()

    # display mysql version
    show_version(my_cursor)

    # main word prompt stuff
    prompt_word(my_cursor, my_db)

    # exit when finished
    sys.exit("Goodbye")



if __name__ == "__main__":
    main()