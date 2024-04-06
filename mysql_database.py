import mysql.connector

def connect_to_sql_server():
    database = mysql.connector.connect(
        host = "localhost",
        user = "root"
    )

    print(database)
    database.close()

connect_to_sql_server()