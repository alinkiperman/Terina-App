import mysql.connector
from mysql.connector import Error


def connect_to_database(database="terina_app"):
    config = {
        "host": "localhost",
        "user": "root",
        "password": "020299Sri",
    }

    if database:
        config["database"] = database

    connection = mysql.connector.connect(
        **config
    )
    print("Connected to MySQL server")
    return connection


def execute_sql_file(file_path):

    connection = connect_to_database(database=None)
    cursor = connection.cursor()

    with open(file_path, "r", encoding="utf-8") as sql_file:
        sql_script = sql_file.read()

    commands = sql_script.split(";")

    for command in commands:
        command = command.strip()

        if command:
            try:
                cursor.execute(command)

            except Error as err:
                if err.errno in [1007, 1050, 1826]: #SQL common errors
                    pass
                else:
                    raise err


    connection.commit()
    cursor.close()
    connection.close()

    print("SQL file executed")
