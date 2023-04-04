from typing import Union

import psycopg2


def execute_get_last_date_read_score(conn, email:str) -> str:
    """
    Retrieve the date of the latest score record for a given user ID.

    Parameters:
        conn (psycopg2.extensions.connection): A connection object to the database.
        user_id (str): The ID of the user.

    Returns:
        str or None: The date of the latest score record, or None if there are no records.
    """
    query = """SELECT id
    FROM emailname 
    WHERE stripped_email='{}'""".format(email)

    cursor = conn.cursor()
    try:
        cursor.execute(query)
        record = cursor.fetchall()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1

    cursor.close()
    return record[0][0]


def execute_get_tz_offset_biometrics(conn, date:str) -> Union[str, None]:
    """
    Retrieve the latest recorded date of sleep data for a given user from the 'sleep' table in the database.

    Args:
    - conn (psycopg2.extensions.connection): a connection to the PostgreSQL database
    - user_id (str): the ID of the user whose sleep data will be queried

    Returns:
    - datetime.date: the latest recorded date of sleep data for the given user
    """
    #query = f"SELECT tz_offset_mins FROM biometrics WHERE id='{user_id}'"
    query = """SELECT tz_offset_mins 
    FROM biometrics 
    WHERE id='{}'""".format(date)

    cursor = conn.cursor()
    try:
        cursor.execute(query)
        record = cursor.fetchall()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1

    cursor.close()
    return record[0][0]


def execute_get_tz_offset_sleep(conn, date:str) -> Union[str, None]:
    """
    Retrieve the latest recorded date of sleep data for a given user from the 'sleep' table in the database.

    Args:
    - conn (psycopg2.extensions.connection): a connection to the PostgreSQL database
    - user_id (str): the ID of the user whose sleep data will be queried

    Returns:
    - datetime.date: the latest recorded date of sleep data for the given user
    """
    query = """SELECT tz_offset FROM sleep WHERE date_wake_up='{}'""".format(date)
    # query = """SELECT MAX(date_wake_up) 
    # FROM sleep 
    # WHERE id='{}'""".format(user_id)

    cursor = conn.cursor()
    try:
        cursor.execute(query)
        record = cursor.fetchall()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1

    cursor.close()
    return record[0][0]

# Path: crud\update.py