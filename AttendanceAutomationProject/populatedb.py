import sqlite3

db_locale='users1.db'


connie= sqlite3.connect(db_locale)
c= connie.cursor()

c.execute("""
INSERT into User1(username,password) VALUES

('user1student@gmail.com','222'),
('user2student@gmail.com','023'),
('user3student@gmail.com','123'),
('user4student@gmail.com','234')

""")

c.execute("""INSERT into Faculty1(username,password) VALUES ('AttendanceAutomation','111') """)

c.execute("""
INSERT into Attendence1(reg_no,name,digital_ID,Total_present_days,total_days) VALUES

(2018,'samanvitha','user1student@gmail.com',0,0),
(2023,'sree','user2student@gmail.com',0,0),
(2020,'satvik','user3student@gmail.com',0,0),
(2019,'gopal','user4student@gmail.com',0,0)


""")

connie.commit()
connie.close()