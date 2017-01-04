#!/usr/bin/env python
# coding=utf-8

import sqlite3 as sqlite

QUERY = "SELECT * FROM names WHERE name LIKE '%{}%' AND gender={}"
INSERT_QUERY = "INSERT INTO dist_name(token, sum, gender) VALUES ('{}', '{}', '{}')"

db = sqlite.connect("setruk-2.db")
cur = db.cursor()

stored_token = []
names = cur.execute("SELECT name FROM names").fetchall()
parsed_names = [name[0] for name in names]


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
            for gender in ["0", "1"]:
                for token in tokens:
                    if token not in stored_token:
                        try:
                            names = cur.execute(QUERY.format(token, gender)).fetchall()
                            cur.execute(INSERT_QUERY.format(token, str(len(names)), gender))
                            stored_token.append(token)
                        except Exception as err:
                            print "unable to perform operation, reason: %s"%err

    db.commit()

