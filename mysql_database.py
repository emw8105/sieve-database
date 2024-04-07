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

    def load_wikipedia_data(self):
        wikipedia_table = """CREATE TABLE Wikipedia(
                             Project_Type		VARCHAR(15)		NOT NULL,
                             Page_Name			MEDIUMTEXT		NOT NULL,
                             View_Count			INT				NOT NULL,
                             Bytes_Transferred	BIGINT			NOT NULL
                             )"""
        self.cursor.execute(wikipedia_table)
        
        alter_table_query = "ALTER TABLE Wikipedia CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci"
        self.cursor.execute(alter_table_query)
        
        file = open(self.file_wikipedia_20160701_0, "r", encoding="utf8")
        next(file)
        for line in file:   
            line = line.strip()
            values = line.split(' ')
            query = "INSERT INTO Wikipedia (Project_Type, Page_Name, View_Count, Bytes_Transferred) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, values)
        file.close()
        self.database_connection.commit()
        

    def close(self):
        self.cursor.close()
        self.database_connection.close()


def set_up():
    database = Database()
    database.connect_to_sql_server()
    database.create_database()
    database.load_wikipedia_data()
    database.close()

set_up()