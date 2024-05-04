import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from random import choice
from bin.models import GearData

# Load environment variables
load_dotenv()
HOST = os.getenv('host')
USER = os.getenv('user')
PASSWORD = os.getenv('password')
DATABASE = os.getenv('database')

def create_connection():
    """Create a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        if connection.is_connected():
            print('Connected to MySQL database')
            return connection
    except Error as e:
        print("Error connecting to MySQL database:", e)
        return None

def close_connection(connection):
    """Close the connection."""
    if connection:
        connection.close()

def execute_query(sql, values=None):
    """Execute a query."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            if values:
                cursor.execute(sql, values)  # Use parameterization
            else:
                cursor.execute(sql)
            connection.commit()
        except Error as e:
            print("Error executing query:", e)
        finally:
            close_connection(connection)

def fetch_data(sql, values=None):
    """Fetch data from the database."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            if values:
                cursor.execute(sql, values)  # Use parameterization
            else:
                cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print("Error fetching data:", e)
        finally:
            close_connection(connection)

def table_check():
    """Check if member_gear table exists and create if necessary."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('''
            SELECT table_name FROM information_schema.tables WHERE table_name='member_gear';
            ''')
            row = cursor.fetchall()
            if len(row) == 0:
                print('Creating member table')
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS member_gear (
                    user_id INT NOT NULL, 
                    gear_photo TEXT NOT NULL,
                    ap INT NOT NULL,
                    aap INT NOT NULL,
                    dp INT NOT NULL,
                    gs INT NOT NULL,
                    family_name TEXT NOT NULL,
                    server_id BIGINT NOT NULL,
                    datestamp DATE NOT NULL,
                    PRIMARY KEY(user_id)
                );''')
                connection.commit()
        except Error as e:
            print("Error checking or creating table:", e)
        finally:
            close_connection(connection)

def update_gear(gear_data: GearData):
    sql = '''INSERT INTO member_gear(user_id, gear_photo, ap, aap, dp, gs, family_name, server_id, datestamp)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
             ON DUPLICATE KEY UPDATE 
             gear_photo = VALUES(gear_photo), 
             ap = VALUES(ap),
             aap = VALUES(aap), 
             dp = VALUES(dp), 
             gs = VALUES(gs),  -- Use VALUES() for the gs column
             family_name = VALUES(family_name), 
             datestamp = VALUES(datestamp)'''
    payload = (gear_data.user_id, gear_data.gear_photo, gear_data.ap, gear_data.aap, gear_data.dp, gear_data.gs, gear_data.family_name, gear_data.server_id, gear_data.datestamp)
    execute_query(sql, payload)
    return gear_data

def update_ap(user_id, ap):
    """Update the AP of a user."""
    sql = '''UPDATE member_gear SET ap = %s WHERE user_id = %s'''
    payload = (ap, user_id)
    execute_query(sql, payload)
    
    # Recalculate gs
    update_gs(user_id)
    return True

def update_aap(user_id, aap):
    """Update the Awakening AP of a user."""
    sql = '''UPDATE member_gear SET aap = %s WHERE user_id = %s'''
    payload = (aap, user_id)
    execute_query(sql, payload)
    
    # Recalculate gs
    update_gs(user_id)
    return True

def update_dp(user_id, dp):
    """Update the DP of a user."""
    sql = '''UPDATE member_gear SET dp = %s WHERE user_id = %s'''
    payload = (dp, user_id)
    execute_query(sql, payload)
    
    # Recalculate gs
    update_gs(user_id)
    return True

def update_gs(user_id):
    """Recalculate the gear score of a user."""
    sql = '''UPDATE member_gear SET gs = ((ap + aap) / 2) + dp WHERE user_id = %s'''
    execute_query(sql, (user_id,))
    return True

def update_gear_photo(user_id, gear_photo):
    """Update the gear photo of a user."""
    sql = '''UPDATE member_gear SET gear_photo = %s WHERE user_id = %s'''
    payload = (gear_photo, user_id)
    execute_query(sql, payload)
    return True

def find_gear(user_id):
    sql = 'SELECT * FROM member_gear WHERE user_id=%s'
    rows = fetch_data(sql, (user_id,))  # Pass user_id as a tuple
    return rows

def del_gear(user_id):
    sql_del = 'DELETE FROM member_gear WHERE user_id=%s'
    sql_find = 'SELECT gear_photo FROM member_gear WHERE user_id=%s'
    rows = fetch_data(sql_find, (user_id,))  # Pass user_id as a tuple
    execute_query(sql_del, (user_id,))  # Pass user_id as a tuple
    return rows


def find_average(server_id):
    sql = 'SELECT gs FROM member_gear WHERE server_id=%s'
    rows = fetch_data(sql, server_id)
    return rows

def find_all(server_id, page):
    sql = 'FROM member_gear WHERE server_id=%s'
    sql_count = f'SELECT COUNT(*) {sql}'
    sql_select = f'SELECT * {sql} ORDER BY gs DESC LIMIT {page*10}, 10'
    count_rows = fetch_data(sql_count, server_id)
    pages = count_rows[0][0]
    rows = fetch_data(sql_select, server_id)
    return [rows, pages]

def find_id(guild_id, page):
    sql = 'FROM member_gear WHERE server_id=%s'
    sql_count = f'SELECT COUNT(*) {sql}'
    sql_select = f'SELECT user_id, family_name {sql} ORDER BY gs DESC LIMIT {page*20}, 20'
    count_rows = fetch_data(sql_count, guild_id)
    pages = count_rows[0][0]
    rows = fetch_data(sql_select, guild_id)
    return [rows, pages]