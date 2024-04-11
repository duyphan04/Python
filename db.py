import mysql.connector

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",  # Or your database host
        user="root",
        password="puppyduylun365",# Your database password
        database="quiz_app" # Your database name
    )