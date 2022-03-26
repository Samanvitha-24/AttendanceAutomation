import sqlite3

db_locale='users1.db'

connie= sqlite3.connect(db_locale)
c= connie.cursor()
c.execute("""
CREATE TABLE User1
(
    username TEXT,
    password TEXT
)
""")

c.execute("""
CREATE TABLE Faculty1
(
    username TEXT,
    password TEXT
)
""")

c.execute("""
CREATE TABLE Attendence1
(
    reg_no NUMBER PRIMARY KEY,
    name TEXT,
    digital_ID TEXT,
    Total_present_days NUMBER,
    total_days NUMBER
)
""")


c.execute("""
CREATE TABLE details
(
    reg_no Number,
    name TEXT,
    _date DATE
)
""")

connie.commit()
connie.close()