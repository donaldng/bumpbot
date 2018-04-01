from flask import Flask, render_template, request, flash, redirect, session, url_for
from model.user import User
from model.post import Post
import multiprocessing
import sqlite3, records
import datetime
from environment.config import *
from util.encryption import CryptoFernet
from util.misc import log
import os

app = Flask(__name__)
app.secret_key = "1234567890password0987654321"

os.chdir(app_src_path)

@app.route('/')
def index():
    page = 'index.html'
    msg = request.args.get("msg")
    
    try:
        if session['logged_in']:
            page = 'manage.html'
            db = records.Database('sqlite:///{}'.format(dbname))
            
            post = Post(session["username"])
            limit = post.limit

            posts = post.get(user_id=session['user_id'])

            disableAddBtn = False
            if len(posts.all()) >= limit:
                disableAddBtn = True

            return render_template(page, posts=posts, disableAddBtn=disableAddBtn)
    except:
        pass

    return render_template(page)

@app.route('/register', methods=['POST'])
def register():
    msg = ""

    if request.method == 'POST':
        username = request.form['register_username']
        u = User(username)

        if u.newUser:
            u.add()
            log("Adding new user {}".format(username))
            
            url_root = request.url_root
            log("baseURL is {}".format(url_root))
            t = multiprocessing.Process(target=u.sendCode, args=(url_root,))
            t.start()

            msg = 'We have successfully sent you a code. Please check your LYN inbox!'
            category = "primary"
        else:
            msg = '{} is already a registered user.'.format(username)
            category = "warning"

    flash(msg, category)
    return redirect(url_for("index"))

@app.route("/login", methods=['POST'])
def login():
    msg = "Successfully logged in!"
    category = "primary"
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
            category = "danger"

    flash(msg, category)
    return redirect(url_for("index"))

@app.route("/update-password")
def updatePassword():
    oldpassword = ""

    if session["logged_in"]:
        u = User(session["username"])
        isFirstTime = u.firstTime()
        
        if isFirstTime:
            oldpassword = u.getPassword()
            flash("Please update your password.", "warning")
            
        page = render_template("updatePassword.html", oldpassword=oldpassword)
    else:
        flash("You need to login first!", "warning")
        page = redirect(url_for("index"))
    return page

@app.route("/add-url", methods=["POST"])
def addURL():
    if not session["logged_in"]:
        return redirect(url_for("index"))
        
    if request.method == 'POST':
        url = request.form['url']
        post = Post(session["username"])
        count = len(post.get(user_id=session["user_id"]).all())

        if count < post.limit:
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
        flash("You need to login first!", "warning")
        page = redirect(url_for("index"))    

    old_password = request.form['old_password']
    new_password = request.form['password']
    password_again = request.form['password_again']

    u = User(session["username"])

    valid = (u.getPassword() == old_password and new_password == password_again)
    old_new_not_same = old_password != new_password

    if valid and old_new_not_same:
        u.updatePassword(session["username"], new_password)
        u.notFirstTime()

        flash("Password sucessfully updated!", "primary")
        page = redirect(url_for("index"))            
    else:
        msg = "Password not matched. Please try again!"

        if not old_new_not_same:
            msg = "Failed to change password. Please use a new password!"

        flash(msg, "warning")
        page = render_template("updatePassword.html")
    
    return page

@app.route("/login/<username>/<token>")
def linkLogin(username=None, token=None):    

    page = redirect(url_for("index"))

    if username and token:

        u = User(username)
        firsttime = u.firstTime()   

        if firsttime:
            c = CryptoFernet()

            password = c.decrypt(token)
            log("password is {}".format(password))

            user_id = u.validate(password)
            session['logged_in'] = user_id
            log("user_id is {}".format(user_id))
            if user_id:
                session["username"] = username
                session["user_id"] = user_id
                flash("Please update your password.", "warning")
                page = render_template("updatePassword.html", oldpassword=password)
            else:
                msg = "Wrong username and/or password!"
    
    return page

@app.route("/logout")
def logout():
    msg = ""
    
    if session['logged_in']:
        session['logged_in'] = False
        session['username'] = None
        session['user_id'] = 0
        msg = "Successfully logged out!"

    flash(msg, "primary")
    return redirect(url_for("index"))

@app.template_filter('time2date')
def time2date(timestampp):

    try:
        result = datetime.datetime.fromtimestamp(int(timestampp)).strftime('%Y-%m-%d %H:%M:%S')
    except:
        log("Unable to convert {}".format(timestampp))

    return result

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)