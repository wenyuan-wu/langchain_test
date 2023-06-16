import sqlite3
from util import SQLiteUtility

def create_table(db_path, table, cols):
    #TODO: need update
    con = sqlite3.connect("database/prompts.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE prompt(type, language, text)")


def check_table():
    pass


# def insert_val():
#     cur.execute("""
#         INSERT INTO prompt VALUES
#             ('full', 'de', '{prompt}'),
#     """)


if __name__ == '__main__':
    # # create_table("database/prompts.db", "prompt", ["type", "content", "language"])
    # con = sqlite3.connect("database/prompts.db")
    # cur = con.cursor()
    # res = cur.execute("SELECT name FROM sqlite_master")
    # print(res.fetchone())

    # Example Usage:
    prompt_db_path = "database/prompts.db"
    db = SQLiteUtility('my_database.db')

    create_table_query = """
    CREATE TABLE IF NOT EXISTS employees (
        id integer PRIMARY KEY,
        name text NOT NULL,
        department text NOT NULL,
        birthdate text
    );"""

    db.create_table(create_table_query)

    data = {
        "id": 1,
        "name": "John Doe",
        "department": "HR",
        "birthdate": "1980-01-01"
    }

    db.insert_rows('employees', data)

    select_query = "SELECT * from employees"
    db.select_rows(select_query)

    db.close_connection()

