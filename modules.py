import psycopg2
from config import host, user, password, db_name

try:
    connectDB = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connectDB.autocommit = True
    cursor = connectDB.cursor()

    # with connectDB.cursor() as cursor:
    #     cursor.execute(
    #         "Select version();"
    #     )

    #     print(f'Server version: {cursor.fetchone()}')
    
    # create new table
    with connectDB.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE users(
            id serial PRIMARY KEY,
            first_name varchar(50) NOT NULL,
            nick_name varchar(50) NOT NULL);"""
        )

        print("Table created!")

    # with connectDB.cursor() as cursor:
    #     cursor.execute(
    #         """INSERT INTO users (first_name, nick_name) VALUES
    #         ('Otabek', 'wextin');"""
    #     )

    #     print("Data was inserted")

    # with connectDB.cursor() as cursor:
    #     cursor.execute(
    #         """SELECT nick_name FROM users WHERE first_name = 'Otabek';"""
    #     )

    #     print(cursor.fetchone())

    # with connectDB.cursor() as cursor:
    #     cursor.execute(
    #         """DROP TABLE users;"""
    #     )

    #     print("Table was dropped")

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connectDB:
        connectDB.close()
        print("Closed")