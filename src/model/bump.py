from splinter import Browser
from environment.config import *
import sqlite3, records
from util.encryption import CryptoFernet
from util.misc import maskPassword, log
import time


class Bump:

    def __init__(self, username=None):

        self.db = records.Database('sqlite:///{}'.format(dbname))
        self.base_url = "https://forum.lowyat.net"
        self.topic_url = "https://forum.lowyat.net/topic/"
        self.username = username if username else bot_username


    def start(self):
        now_time = int(time.time())
        self.posts = self.db.query("SELECT post_id FROM post WHERE status=1 AND {now_time} > next_execution AND next_execution != 0;".format(now_time=now_time))
        
        if len(self.posts.all()) > 0:
            with Browser('firefox', headless=True) as self.browser:
                
                self.visit(self.base_url)
                self.login()
                
                if self.logged_in():
                    self.bumps()
                    self.logout()

    def logged_in(self):
        return self.browser.is_text_present(self.username)

    def visit(self, url):
        log("visit {}".format(url))
        self.browser.visit(url)

    def login(self):

        password = bot_password

        if self.username != bot_username:
            password = self.retrievePassword(self.username)

        self.browser.fill('UserName', self.username)
        self.browser.fill('PassWord', password)

        masked_password = maskPassword(password)

        log("Login with username {} and password {}".format(self.username, masked_password))

        button = self.browser.find_by_css('.button')
        button.click()
        log("We in!")

    def logout(self):
        logout_link = self.browser.find_by_text('Log out')
        logout_link.click()
        log("Logout!")

    def scrollDown(self):
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    def retrievePassword(self, username):
        cf = CryptoFernet()

        token = self.db.query("SELECT password FROM user WHERE username=:username", False, username=username)[0].password
        password = cf.decrypt(token)

        return password

    def updateBumpCount(self):
        self.db.query("UPDATE post SET count = count + 1, last_bump={t}, updated_at={t}, next_execution=0".format(t=int(time.time())))

    def bumps(self):
        for row in self.posts:
            self.visit("{}{}".format(self.topic_url, row.post_id))
            self.scrollDown()
            self.browser.fill('Post', 'bump!')
            submit_button = self.browser.find_by_name('submit')
            submit_button.click()
            self.updateBumpCount()

if __name__ == "__main__":
    bump = Bump()
    bump.start()