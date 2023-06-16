import sqlite3


def create_table(db_path, table, cols):
    #TODO: need update
    con = sqlite3.connect("database/prompts.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE prompt(type, content, language)")


def check_table():
    pass


if __name__ == '__main__':
    # create_table("database/prompts.db", "prompt", ["type", "content", "language"])
    con = sqlite3.connect("database/prompts.db")
    cur = con.cursor()
    res = cur.execute("SELECT name FROM sqlite_master")
    print(res.fetchone())

