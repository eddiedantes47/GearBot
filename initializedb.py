import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
HOST = os.getenv('host')
USER = os.getenv('user')
PASSWORD = os.getenv('password')
DATABASE = os.getenv('database')

def create_table():
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        if connection.is_connected():
            cursor = connection.cursor()
            # Define the SQL statement to create the table
            create_table_query = """
            CREATE TABLE IF NOT EXISTS member_gear (
                user_id BIGINT NOT NULL, 
                gear_photo TEXT NOT NULL,
                ap INT NOT NULL,
                aap INT NOT NULL,
                dp INT NOT NULL,
                gs INT NOT NULL,
                family_name TEXT NOT NULL,
                server_id BIGINT NOT NULL,
                datestamp DATE NOT NULL,
                PRIMARY KEY(user_id)
            )
            """
            # Execute the SQL statement
            cursor.execute(create_table_query)
            print("Table 'member_gear' created successfully")
    except Error as e:
        print("Error creating table:", e)
    finally:
        # Close the connection
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

# Call the function to create the table
create_table()
