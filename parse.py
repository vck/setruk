#!/usr/bin/env python
# coding=utf-8

import sqlite3 as sqlite

CREATE_TABLE = "CREATE TABLE dist_name(id INTEGER PRIMARY KEY AUTOINCREMENT, token VARCHAR(20), sum INTEGER, gender INTEGER)"
QUERY = "SELECT * FROM names WHERE name LIKE '%{}%' AND gender={}"
INSERT_QUERY = "INSERT INTO dist_name(token, sum, gender) VALUES ('{}', '{}', '{}')"

db = sqlite.connect("setruk-2.db")
cur = db.cursor()

cur.execute("DROP TABLE IF EXISTS dist_name")
cur.execute(CREATE_TABLE)
db.commit()

stored_token = []
names = cur.execute("SELECT name FROM names").fetchall()
parsed_names = [name[0] for name in names]
genders = ["0", "1"]

def parse_name(name, jump=2):
    """
    parse name to it's morfologi
    """

    tokens = []

    start, stop = 0, jump


    print "scanning name: %s"%name
    for i in range(len(name)):
        tokens.append(name[start:stop].strip(" "))
        start, stop = stop, stop+jump

    return tokens

if __name__ == "__main__":
    for name in parsed_names:
        for i in range(2,6):
            tokens = parse_name(name, jump=i)
            for token in tokens:
                if token not in stored_token:
                    print "[perform] token: {}".format(token)
                    try:
                        male = cur.execute(QUERY.format(token, "0")).fetchall()
                        female = cur.execute(QUERY.format(token, "1")).fetchall()
                        cur.execute(INSERT_QUERY.format(token, str(len(male)), 0))
                        cur.execute(INSERT_QUERY.format(token, str(len(female)), 1))
                        stored_token.append(token)
                    except Exception as err:
                        print "unable to perform operation, reason: %s"%err

    db.commit()

