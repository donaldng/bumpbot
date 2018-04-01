from requests_html import HTMLSession
from environment.config import *
from util.misc import log
from splinter import Browser
import sqlite3, records
import time

class Post:
    def __init__(self, user=None):
        self.db = records.Database('sqlite:///{}'.format(dbname))
        self.topic_url = "https://forum.lowyat.net/topic/"
        self.requestor = user
        self.limit = 1

    def add(self, url):
        post_id = self.process_id(url)
        
        log("post_id is {}".format(post_id))

        post_title, post_owner =  self.getPostInfo(post_id)
        is_owner = post_owner.lower() == self.requestor.lower()

        if post_id and is_owner:
            status = "Verified success, will bump {}{} for {}!".format(self.topic_url, post_id, self.requestor)
            try:
                self.db.query("INSERT OR IGNORE INTO post (post_id, title, url, count, status, user_id, created_at, updated_at) VALUES ({pid}, '{title}', '{base}{pid}', 0, 1, (SELECT user_id FROM user WHERE LOWER(username)='{uname}'), {t}, {t})".format(pid=post_id, base=self.topic_url, uname=self.requestor.lower(), t=int(time.time()), title=post_title))
                self.db.query("UPDATE post SET deleted=0, updated_at={t} WHERE post_id={pid} AND user_id=(SELECT user_id FROM user WHERE LOWER(username)='{uname}')".format(pid=post_id, uname=self.requestor.lower(), t=int(time.time())))
            except:
                status = "Error inserting post"
                log(status)
                pass

        elif not is_owner:
            status = "post owner is {}, not you, {}".format(post_owner, self.requestor)
            log(status)
        else:
            status = "unable to process url {}".format(url)
            log(status)
        
        return status
    
    def delete(self, post_id):
        log("delete post_id {}".format(post_id))

        post_owner = self.db.query("SELECT u.username FROM post p, user u WHERE u.user_id=p.user_id AND post_id=:post_id", False, post_id=post_id)[0].username
        log("post_owner is {}".format(post_owner))

        if post_owner.lower() == self.requestor.lower():
            self.db.query("UPDATE post SET deleted=1, status=0 WHERE post_id=:post_id", False, post_id=post_id)
            log("deleted")

    def updateStatus(self, post_id, status):
        log("stop post_id {}".format(post_id))

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
            where_statement = " AND {}".format(" AND ".join(condition))

        return self.db.query('SELECT * FROM post WHERE deleted=0 {};'.format(where_statement))


    def getPostInfo(self, post_id):
        log("get post info of post_id {}".format(post_id))
        session = HTMLSession()

        url = "{}{}".format(self.topic_url, post_id)
        r = session.get(url)

        body = r.html

        topic_owner = body.find("span.normalname", first=True).text
        title = body.find("title", first=True).text

        log("topic owner={};title={}".format(topic_owner, title))

        return title, topic_owner


if __name__ == "__main__":
    post = Post("ACHARR")
    status = post.add("https://forum.lowyat.net/topic/4503006/+20")


