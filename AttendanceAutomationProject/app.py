#from flask import Flask, request, render_template
from flask import Flask,render_template,request,flash,redirect,url_for
import sqlite3
from flask import g
import os
import sqlite3
import pandas as pd
 
app = Flask(__name__)
   
DATABASE = 'users1.db' 
 
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
 
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def valid_login2(username, password):
    user = query_db('select * from User1 where username = ? and password = ?', [username, password], one=True)
    if user is None:
        return False
    else:
        return True
def valid_login1(username, password):
    user = query_db('select * from Faculty1 where username = ? and password = ?', [username, password], one=True)
    if user is None:
        return False
    else:
        return True

def log_the_user_in():
    return render_template('selectaction.html')

def log_the_student_in():
    return render_template('display_template.html')

def uploadfile():
    return render_template('profile.html')
def studentlog():
    return render_template('student_login.html')
def facultylog():
    return render_template('faculty_login.html')
def date_enter():
    return render_template('date_entry.html')

def startpage():
    return render_template('home.html')
@app.route("/", methods=['POST', 'GET'])
def start():
    error=None
    if request.method == 'POST':
        if request.form['submit_button'] == 'ENTER_PORTAL':
                return startpage()
    return render_template('homepage.html',error=error)
            
@app.route('/home', methods=['POST', 'GET'])
def homelog():
    error = None
    if request.method == 'POST':
        if request.form['submit_button'] == 'STUDENT':
            return studentlog()
        elif request.form['submit_button'] == 'FACULTY':
           return facultylog()

    return render_template('home.html', error=error)

@app.route("/")
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login1(request.form['username'], request.form['password']):
            return log_the_user_in()
        else:
            error = 'Invalid username/password'

    return render_template('faculty_login.html', error=error)
@app.route("/")
@app.route('/display', methods=['POST', 'GET'])
def login2():
    error = None
    if request.method == 'POST':
        if valid_login2(request.form['username'], request.form['password']):
            return display2()
        else:
            error = 'Invalid username/password'

    return render_template('student_login.html', error=error)

def query_attendence_details():
    connie=sqlite3.connect('users1.db')

    c = connie.cursor()
    c.execute("""
    SELECT *,Total_present_days*100/total_days as percentage from Attendence1
    """
    )
    student_data = c.fetchall()
    return student_data
def single_student_details(user_name):
    connie=sqlite3.connect(DATABASE)   
    c= connie.cursor()
    sql_print="""
    select *,Total_present_days*100/total_days as percentage from Attendence1 where digital_ID = ?
    """
    c.execute(sql_print,(user_name,))
    records = c.fetchall()
    return records
    
def display1():
    student_data = query_attendence_details()
    return render_template('display_template.html' , student_data = student_data)
#@app.route("/")
@app.route('/action', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        if request.form['submit_button'] == 'UPLOAD ATTENDANCE':
            return uploadfile()
        elif request.form['submit_button'] == 'CHECK BY DATE':
            return date_enter()
        elif request.form['submit_button'] == 'OVERALL ATTENDANCE':
            return display1()



def display2():
    
        name = request.form['username']
        student_data = single_student_details(name)
        return render_template('display_template.html',student_data=student_data,digital_ID=name)


app.config['UPLOAD_FOLDER']="static\Excel"
app.secret_key="123"

con=sqlite3.connect("users1.db")
con.execute("create table if not exists data(pid integer primary key,exceldata TEXT)")
con.close()

@app.route("/upload",methods=['GET','POST'])
def index():

    con = sqlite3.connect("users1.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from data")
    data = cur.fetchall()
    con.close()


    if request.method == 'POST':
        uploadExcel = request.files['uploadExcel']
        if uploadExcel.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], uploadExcel.filename)
            uploadExcel.save(filepath)
            con = sqlite3.connect("users1.db")
            cur = con.cursor()
            cur.execute("insert into data(exceldata)values(?)", (uploadExcel.filename,))
            con.commit()
            flash("Excel Sheet Upload Successfully", "success")

            con = sqlite3.connect("users1.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("select * from data")
            data = cur.fetchall()
            con.close()
            return render_template("profile.html", data=data)

    return render_template("profile.html",data=data)

  
@app.route('/view_excel/<string:id>')
def view_excel(id):
    con = sqlite3.connect("users1.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from data where pid=?",(id))
    data = cur.fetchall()
    print(data)
    for val in data:
        path = os.path.join("static/Excel/",val[1])
        #print(val[1])
        data=pd.read_csv(path)
        df= pd.DataFrame(data)
        for row in df.itertuples():
            cur.execute(
                '''
                INSERT INTO details(reg_no, name) VALUES(?, ? )
                ''',
                (row.reg_no, 
                row.name
                ))
            
        cur.execute(''' update Attendence1 as a set Total_present_days=Total_present_days+1 where reg_no=(select reg_no from details as b where a.reg_no=b.reg_no) ''')
        cur.execute(''' update Attendence1 set total_days=total_days+1''') 
        
       
     
        
        cur.execute('''delete from details''')
        cur.execute('''delete from data''')
    con.commit()
    con.close()
    return render_template("view_excel.html",data=data.to_html(index=False,classes="table table-bordered").replace('<th>','<th style="text-align:center">'))
 
@app.route('/delete_record/<string:id>')
def delete_record(id):
    try:
        con=sqlite3.connect("users1.db")
        cur=con.cursor()
        cur.execute("delete from data where pid=?",[id])
        con.commit()
        flash("Record Deleted Successfully","success")
    except:
        flash("Record Deleted Failed", "danger")
    finally:
        return redirect(url_for("index"))
con.close()	
    

if __name__ == "__main__":
    app.debug = True
    app.run()