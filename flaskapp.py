import sqlite3
from flask import *  
app = Flask(__name__)  

app.secret_key = "abc" 
import csv
import sqlite3

from flask import Flask, request, g

DATABASE = '/var/www/html/user.db'

app.config.from_object(__name__)

def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

@app.route("/viewdb")
def viewdb():
    rows = execute_query("""SELECT * FROM user""")
    return '<br>'.join(str(row) for row in rows)

def get_user_info(user_name):
    con = connect_to_database()
    cur = con.cursor()
    cur.execute("SELECT * FROM user where username = (?)" , [user_name])
    data = cur.fetchall() 
    return data



@app.route('/')  
def home():  
    return render_template("signup.html")  

 
@app.route('/login',methods = ["GET","POST"])  
def login():  
    error = None;  
    if request.method == "POST": 
        username = request.form['username']
        pwd = request.form['pwd']
        data = get_user_info(username)
        for item in data:
            username = request.form['username']
            if pwd != item[1]:
                error = "invalid password" 
            elif username != item[0]:
                error = "username don't have account"

            else:
                msg = "you are successfuly logged in"
                session[username] = username 
                return render_template('result.html' , data= data, msg = msg ) 
        return render_template('Login.html',error = error)  
  
 
@app.route("/result")
def result():
    return render_template("result.html" ) 

@app.route('/logout')
def logout():
   session.pop('username', None)
   flash("you successfully logged out")
   return redirect(url_for('home'))  

@app.route("/register" , methods =["GET", "POST"]) 
def register():
        if request.method == 'POST':
            username = request.form['username']
            pwd = request.form['pwd']
            Firstname = request.form['Firstname']
            Lastname = request.form['Lastname']
            email = request.form['email']
            try:
                con = connect_to_database()
                cur = con.cursor()
                cur.execute("INSERT INTO user(username,password,firstname,lastname,email) VALUES (?,?,?,?,?)",(username,pwd,Firstname,Lastname,email) )
                con.commit()
                con.close()
                msg = "successfully registered"
            except:
                error = "You already have account" 
                return render_template('signup.html' , error = error)
            data = get_user_info(username)
        return render_template('result.html' , data= data, msg = msg )      
        
@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/Login")
def Login():
    return render_template("Login.html")

if __name__ == '__main__':  
    app.run(debug = True) 