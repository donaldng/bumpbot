import sqlite3, records
from util.encryption import *
from util.passwordGenerator import password_generator

class Register:

    def __init__(self, username):
        self.db = records.Database('sqlite:///history.db')
        
        self.username = username

        if not self.validUsername(username):
            print("user not found in LYN")

    def validUsername(self, username):
        

    def addRecord(self):
        self.password = password_generator()

        print(self.password)

        if not self.registered():
            encrypted_password = encrypt(self.password)
            self.db.query('INSERT INTO user (username, password) VALUES ("{un}", "{ps}")'.format(un=self.username, ps=encrypted_password))        

    def registered(self):
        return self.db.query("SELECT COUNT(*) count FROM user WHERE username = '{}'".format(self.username))[0].count > 0

if __name__ == "__main__":
    Register("donaldyann")