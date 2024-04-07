import mysql.connector

class Database:
    def __init__(self):
        self.file_wikipedia_20160701_0 = "Filtered_wikipedia_dataset.txt"
    
    def connect_to_sql_server(self):
        self.database_connection = mysql.connector.connect(
            host = "localhost",
            user = "root"
        )
        print(self.database_connection)
        self.cursor = self.database_connection.cursor()
    
    def create_database(self):
        self.cursor.execute("DROP DATABASE IF EXISTS sieve")
        self.cursor.execute("CREATE DATABASE sieve")
        self.cursor.execute("USE sieve")

    def close(self):
        self.database_connection.close()


def set_up():
    database = Database()
    database.connect_to_sql_server()
    database.create_database()
    database.close()

set_up()