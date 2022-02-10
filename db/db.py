import sqlite3

from classes.Database import dbopen, Database

database = dbopen("question_data.db")


def init_db():
    with database as cursor:
        with open("schema.sql") as schema:
            cursor.executescript(schema.read())


if __name__ == '__main__':
    db = Database()
    import datetime

    with database as cursor:
        for row in cursor.execute("PRAGMA table_info('question_data')"):
            print(row)
        for row in cursor.execute("SELECT * FROM question_data"):
            print(row)

    with database as cursor:
        # cursor.execute("INSERT INTO question_data VALUES (?, ?, ?, ?, ?, ?);", ("class", datetime.datetime.now(), "a",
        #                "b", "e", "f"))
        print("===")
        cursor.execute("SELECT * FROM question_data WHERE due_date > ?",
                       (datetime.datetime(year=2023, day=10, month=3),))
        data = cursor.fetchall()
        for row in data:
            print(row)
            for i in row:
                print(type(i), end=" ")
            print()
