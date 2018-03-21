from flask import Flask, render_template, request, flash, redirect, session, url_for
from user import User
from post import Post
import multiprocessing
import sqlite3, records
import datetime
from environment.config import *


app = Flask(__name__)
app.secret_key = "1234567890password0987654321"

@app.route('/')
def index():
    page = 'index.html'
    msg = request.args.get("msg")
    
    try:
        if session['logged_in']:
            page = 'manage.html'
            db = records.Database('sqlite:///{}'.format(dbname))
            posts = db.query('SELECT * FROM post WHERE user_id={}'.format(session['user_id']))
            return render_template(page, posts=posts)
    except:
        pass

    return render_template(page)

@app.route('/register', methods=['POST'])
def register():
    msg = ""

    if request.method == 'POST':
        username = request.form['register_username']
        u = User(username)

        t = multiprocessing.Process(target=u.sendCode)
        t.start()

        msg = 'We have successfully sent you a code. Please check your LYN inbox!'

    flash(msg)
    return redirect(url_for("index"))

@app.route("/login", methods=['POST'])
def login():
    msg = "Successfully logged in!"
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        u = User(username)
        result = u.validate(password)
        session['logged_in'] = result

        if result:
            session["username"] = username
            session["user_id"] = result
        else:
            msg = "Wrong username and/or password!"

    flash(msg)
    return redirect(url_for("index"))

@app.route("/update-password")
def updatePassword():
    if session["logged_in"]:
        page = render_template("updatePassword.html")
    else:
        flash("You need to login first!")
        page = redirect(url_for("index"))
    return page

@app.route("/add-url", methods=["POST"])
def addURL():
    if not session["logged_in"]:
        return redirect(url_for("index"))
        
    if request.method == 'POST':
        url = request.form['url']
        post = Post(session["username"])
        status = post.add(url)
    
    return status

@app.route("/delete-url", methods=["POST"])
def deleteURL():
    if not session["logged_in"]:
        return redirect(url_for("index"))
        
    if request.method == 'POST':
        id = request.form['id']
        post = Post(session["username"])
        post.delete(id)
    
    return "Success"

@app.route("/update-url", methods=["POST"])
def updateURL():
    if not session["logged_in"]:
        return redirect(url_for("index"))
        
    if request.method == 'POST':
        id = request.form['id']
        status = request.form['status']

        post = Post(session["username"])
        post.updateStatus(id, status)
    
    return "Success"
    
@app.route("/update-db-password", methods=['POST'])
def updateDBPassword():

    if not session["logged_in"]:
        flash("You need to login first!")
        page = redirect(url_for("index"))    

    old_password = request.form['old_password']
    new_password = request.form['password']
    password_again = request.form['password_again']

    u = User(session["username"])

    valid = (u.getPassword() == old_password and new_password == password_again)
    old_new_not_same = old_password != new_password

    if valid and old_new_not_same:
        u.updatePassword(session["username"], new_password)

        flash("Password sucessfully updated!")
        page = redirect(url_for("index"))            
    else:
        msg = "Password not matched. Please try again!"

        if not old_new_not_same:
            msg = "Failed to change password. Please use a new password!"

        flash(msg)
        page = render_template("updatePassword.html")
    
    return page


@app.route("/logout")
def logout():
    msg = ""
    
    if session['logged_in']:
        session['logged_in'] = False
        session['username'] = None
        session['user_id'] = 0
        msg = "Successfully logged out!"

    flash(msg)
    return redirect(url_for("index"))

@app.template_filter('time2date')
def time2date(ts):
    print(ts)
    result = datetime.datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')
    print(result)
    return result

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)