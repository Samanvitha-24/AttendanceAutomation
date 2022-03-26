import sqlite3

db_locale='users1.db'
connie= sqlite3.connect(db_locale)
c= connie.cursor()

c.execute("""
SELECT * from Faculty1
""")

student_info=c.fetchall()
for student in student_info:
    print(student)


connie.commit()
connie.close()