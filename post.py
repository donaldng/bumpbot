from environment.config import *
from splinter import Browser
import sqlite3, records
import time

class Post:
    def __init__(self, user):
        self.db = records.Database('sqlite:///{}'.format(dbname))
        self.topic_url = "https://forum.lowyat.net/topic/"
        self.requestor = user
        self.limit = 1

    def add(self, url):
        post_id = self.process_id(url)
        
        print("post_id is {}".format(post_id))

        post_title, post_owner =  self.getPostInfo(post_id)
        is_owner = post_owner.lower() == self.requestor.lower()

        if post_id and is_owner:
            status = "Verified success, will bump {}{} for {}!".format(self.topic_url, post_id, self.requestor)
            try:
                self.db.query("INSERT INTO post (post_id, title, url, count, status, user_id, created_at, updated_at) VALUES ({pid}, '{title}', '{base}{pid}', 0, 1, (SELECT user_id FROM user WHERE LOWER(username)='{uname}'), {t}, {t})".format(pid=post_id, base=self.topic_url, uname=self.requestor.lower(), t=time.time(), title=post_title))
            except:
                status = "Error inserting post"
                print(status)
                pass

        elif not is_owner:
            status = "post owner is {}, not you, {}".format(post_owner, self.requestor)
            print(status)
        else:
            status = "unable to process url {}".format(url)
            print(status)
        
        return status
    
    def delete(self, post_id):
        print("delete post_id {}".format(post_id))

        post_owner = self.db.query("SELECT u.username FROM post p, user u WHERE u.user_id=p.user_id AND post_id=:post_id", False, post_id=post_id)[0].username
        print("post_owner is {}".format(post_owner))

        if post_owner.lower() == self.requestor.lower():
            self.db.query("DELETE FROM post WHERE post_id=:post_id", False, post_id=post_id)
            print("deleted")

    def updateStatus(self, post_id, status):
        print("stop post_id {}".format(post_id))

        post_owner = self.db.query("SELECT u.username FROM post p, user u WHERE u.user_id=p.user_id AND post_id=:post_id", False, post_id=post_id)[0].username

        if post_owner.lower() == self.requestor.lower():
            self.db.query("UPDATE post SET status=:status WHERE post_id=:post_id", False, status=status, post_id=post_id)           

    def process_id(self, url):
        post_id = 0

        if "lowyat.net/topic" in url:
            post_id = url.split(".lowyat.net/topic/")[1].split("/")[0]

        # https://forum.lowyat.net/index.php?showtopic=873687&hl=
        if not post_id:
            post_id = url.split("showtopic=")[1].split("&")[0]

        return post_id

    def get(self, user_id=0, username=None):

        condition = []
        where_statement = ""
        
        if user_id:
            condition.append("user_id='{}'".format(user_id))
        
        if username:
            condition.append("username='{}'".format(username))

        if len(condition) > 0:
            where_statement = "WHERE {}".format(" AND ".join(condition))

        return self.db.query('SELECT * FROM post {};'.format(where_statement))


    def getPostInfo(self, post_id):
        with Browser('firefox', headless=True) as browser:
            url = "{}{}".format(self.topic_url, post_id)
            print("visit {}".format(url))
            browser.visit(url)

            topicTitle = browser.title
            topicOwner = browser.find_by_css(".normalname a").first["text"]

            return topicTitle, topicOwner


if __name__ == "__main__":
    post = Post("ACHARR")
    status = post.add("https://forum.lowyat.net/topic/4503006/+20")


