import sqlite3, records
from splinter import Browser
from util.encryption import CryptoFernet
from util.passwordGenerator import password_generator
from environment.bot_credential import *
import time

class User:

    def __init__(self, username):
        self.db = records.Database('sqlite:///history.db')

        self.bot_username = bot_username
        self.bot_password = bot_password

        self.username = username
        self.cf = CryptoFernet()

        if not self.registered():
            self.addRecord()
        else:
            self.password = self.getPassword()

    def validate(self, password):
        user_id = 0

        if password == self.password:
            user_id = self.getUserId()

        return user_id

    def sendCode(self):

        with Browser('firefox', headless=True) as self.browser:
            self.login()
            self.sendMsg()
            self.logout()
        
    def sendMsg(self):
            b = self.browser
        
            b.visit("https://forum.lowyat.net/index.php?act=Msg&CODE=04")
            b.fill('entered_name', self.username)
            b.fill('msg_title', 'bump bot verification')
            b.fill('Post', 'Your verification code is {}'.format(self.password))

            submitbtn = b.find_by_name("submit")
            submitbtn.click()

    def login(self):
        b = self.browser
        
        b.visit("https://forum.lowyat.net/")
        b.fill('UserName', self.bot_username)
        b.fill('PassWord', self.bot_password)

        print("Login with username {} and password *****".format(self.bot_username))

        button = b.find_by_css('.button')
        button.click()
        print("We in!")


    def addRecord(self):
        self.password = password_generator()

        print(self.password)

        if not self.registered():
            encrypted_password = self.cf.encrypt(self.password)
            self.db.query('INSERT INTO user (username, password) VALUES ("{un}", "{ps}")'.format(un=self.username.lower(), ps=encrypted_password))        

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
        print("Logout!")

if __name__ == "__main__":
    u = User("kktxyz")
    u.sendCode()