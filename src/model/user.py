import sqlite3, records
from splinter import Browser
from util.encryption import CryptoFernet
from util.passwordGenerator import password_generator
from environment.config import *
from util.misc import maskPassword, log
import time

class User:

    def __init__(self, username):
        self.db = records.Database('sqlite:///{}'.format(dbname))

        self.bot_username = bot_username
        self.bot_password = bot_password

        self.username = username
        self.cf = CryptoFernet()
        self.newUser = False

        if not self.registered():
            self.newUser = True
            self.password = password_generator()
        else:
            self.password = self.getPassword()

    def validate(self, password):
        user_id = 0

        if self.registered() and password == self.password:
            user_id = self.getUserId()

        return user_id

    def firstTime(self):
        status = self.db.query("SELECT firsttime FROM user WHERE username=:username", False, username=self.username)[0].firsttime
        return status

    def notFirstTime(self):
        self.db.query("UPDATE user SET firsttime=0 WHERE username=:username", False, username=self.username)

    def sendCode(self, url):

        with Browser('firefox', headless=True) as self.browser:
            self.login()
            self.sendMsg(url)
            self.logout()
        
    def sendMsg(self, root_url):
        password = self.getPassword()
        token = self.cf.encrypt(password)
        
        loginPath = "/login"
        if root_url[-1] == "/":
            loginPath = "login"

        url = "{}{}".format(root_url, loginPath)

        log("Sending code to {username} with url: {url}/{username}/{token}".format(username=self.username, url=url, token=token))
        
        body = """Dear {username},

        Your login password is {password}.
        
        Click here to login: {url}/{username}/{token}

        Please change your password after you login.
        
        Thank you.

        WeBump!
        """.format(url=url, username=self.username, password=password, token=token)

        b = self.browser
        
        b.visit("https://forum.lowyat.net/index.php?act=Msg&CODE=04")
        b.fill('entered_name', self.username)
        b.fill('msg_title', 'WeBump! credentials')
        b.fill('Post', body)

        submitbtn = b.find_by_name("submit")
        submitbtn.click()

        log("Successfully sent code to {}".format(self.username))

    def login(self):
        b = self.browser
        
        b.visit("https://forum.lowyat.net/")
        b.fill('UserName', self.bot_username)
        b.fill('PassWord', self.bot_password)

        log("Login with username {} and password {}".format(self.bot_username, maskPassword(self.bot_password)))

        button = b.find_by_css('.button')
        button.click()
        log("We in!")


    def add(self):
        if not self.registered():
            encrypted_password = self.cf.encrypt(self.password)
            self.db.query('INSERT INTO user (username, password, created_at) VALUES ("{un}", "{ps}", datetime("now"))'.format(un=self.username.lower(), ps=encrypted_password))        

    def getPassword(self):
        password = self.db.query("SELECT password FROM user WHERE LOWER(username) = '{}'".format(self.username.lower()))[0].password
        decryptedPassword = self.cf.decrypt(password)

        return decryptedPassword

    def getUserId(self):
        user_id = self.db.query("SELECT user_id FROM user WHERE LOWER(username) = '{}'".format(self.username.lower()))[0].user_id

        return user_id

    def registered(self):
        return self.db.query("SELECT COUNT(*) count FROM user WHERE LOWER(username) = '{}'".format(self.username.lower()))[0].count > 0

    def updatePassword(self, username, password):
        enc_password = self.cf.encrypt(password)
        self.db.query("UPDATE user SET password='{}' WHERE LOWER(username)='{}'".format(enc_password, username.lower()))

    def logout(self):
        logout_link = self.browser.find_by_text('Log out')
        logout_link.click()
        log("Logout!")

if __name__ == "__main__":
    u = User("kktxyz")
    u.sendCode()