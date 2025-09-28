# reset_db.py
import mysql.connector

# --- CONFIGURE YOUR DB CONNECTION HERE ---
# Use the same credentials you use to run your main app
config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password'
}
DB_NAME = 'dictionary'
TABLE_NAME = 'word'
# The path MUST be this specific, secure directory
DATA_FILE_PATH = '/var/lib/mysql-files/words.txt' 
# -----------------------------------------

# The sequence of commands to execute
# Using triple quotes for multi-line strings
sql_commands = [
    f"DROP DATABASE IF EXISTS {DB_NAME}",
    f"CREATE DATABASE {DB_NAME}",
    f"USE {DB_NAME}", # It's good practice to select the DB
    f"""
    CREATE TABLE {TABLE_NAME} (
      word_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
      word VARCHAR(45) NOT NULL,
      PRIMARY KEY (word_id),
      UNIQUE KEY Unique_Word (word)
    );
    """,
    # NOTE: Remember to check your line endings (\r\n vs \n)
    f"""
    LOAD DATA INFILE '{DATA_FILE_PATH}'
    INTO TABLE {TABLE_NAME}
    LINES TERMINATED BY '\\r\\n'
    (word);
    """
]

db = None # Initialize db to None
try:
    # Connect to the MySQL server (without specifying a database)
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    print("Connected to MySQL server.")

    for command in sql_commands:
        try:
            print(f"Executing: {command[:70]}...") # Print first 70 chars
            cursor.execute(command)
        except mysql.connector.Error as err:
            print(f"Error executing command: {err}")
            # Decide if you want to stop on error
            # For LOAD DATA, you might need to check file permissions
            if err.errno == 1045: # Access denied
                print(">>> HINT: Check your MySQL user/password.")
            elif err.errno == 29: # File not found/permission error
                print(f">>> HINT: Ensure '{DATA_FILE_PATH}' exists and has correct permissions.")
            break

    db.commit() # Not strictly needed for DDL, but good practice
    print("\nDatabase has been reset successfully!")

except mysql.connector.Error as err:
    print(f"Database connection error: {err}")
finally:
    if db and db.is_connected():
        cursor.close()
        db.close()
        print("Connection closed.")