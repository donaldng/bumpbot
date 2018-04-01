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
        
        print("SELECT post_id FROM post WHERE status=1 AND {now_time} > next_execution AND next_execution != 0;".format(now_time=now_time))
        print(self.posts.all())

        if len(self.posts.all()) > 0:
            with Browser('firefox', headless=True) as self.browser:
                
                self.visit(self.base_url)
                self.login()
                
                if self.logged_in():
                    self.bumps()
                
                self.logout()

    def logged_in(self):
        log("Logged in!")
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

    def updateBumpCount(self, post_id):
        self.db.query("UPDATE post SET count = count + 1, last_bump={t}, updated_at={t}, next_execution=0 WHERE post_id={post_id}".format(t=int(time.time()), post_id=, post_id))

    def bumpSchedule2Zero(self, post_id):
        self.db.query("UPDATE post SET updated_at={t}, next_execution=0 WHERE post_id={post_id}".format(t=int(time.time()), post_id=, post_id))

    def bumps(self):
        for row in self.posts:
            success = False
            try:
                self.visit("{}{}".format(self.topic_url, row.post_id))
                
                links = self.browser.find_by_tag('img')

                print("{} links found.".format(len(links)))

                for bump_link in links:
                    if bump_link['alt'] == "Bump Topic":
                        log("Found bump link.")
                        bump_link.click()

                        if not self.browser.is_text_present("You can only bump this thread tomorrow.") and not self.browser.is_text_present("Sorry, an error occurred."):
                            self.updateBumpCount(row.post_id)
                            log("Successfully bumped for post {post}!".format(post=row.post_id))
                            success = True

                        if self.browser.is_text_present("You can only bump this thread tomorrow.") and self.browser.is_text_present("Sorry, an error occurred."):
                            log("Error: Already bumped today.")
                            self.bumpSchedule2Zero(row.post_id)
                            success = True

                        break

            except:
                log("Failed to bump post {post}".format(post=row.post_id))
            
            if not success:
                log("Failed to bump post {post}".format(post=row.post_id))
            
            try:
                self.browser.driver.save_screenshot('{}{}.png'.format(app_src_path, row.post_id))
                log("screenshoted post {} bump result".format(row.post_id))
            except:
                log("Failed to capture screenshot for post {}".format(row.post_id))
                
    def comment(self, msg):
        self.browser.fill('Post', 'bump!')
        submit_button = self.browser.find_by_name('submit')
        submit_button.click()


if __name__ == "__main__":
    bump = Bump()
    bump.start()