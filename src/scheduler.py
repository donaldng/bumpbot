from model.bump import Bump
from model.post import Post
from random import randint
import datetime, time
from util.misc import time2date, log
from environment.config import *
import os

def randomNextExecution():
    # set next run time within 0900~1800
    now = datetime.datetime.now()

    start = int(datetime.datetime(now.year, now.month, now.day, 9, 0).timestamp())
    end = int(datetime.datetime(now.year, now.month, now.day, 18, 0).timestamp())
    return randint(start, end)

def scheduler(post_id=None):
    log("start scheduler")

    cond = ""

    if post_id:
        cond = "AND post_id = {}".format(post_id)
    
    scheduler = Post()
    posts = scheduler.db.query("SELECT * FROM post WHERE status=1 {extra}".format(extra=cond))

    for post in posts:
        next_execution = randomNextExecution()
        log("update post_id {}".format(post.post_id))
        scheduler.db.query("UPDATE post SET next_execution=:next_execution WHERE user_id=:user_id and post_id=:post_id AND status=1;", False, next_execution=next_execution, user_id=post.user_id, post_id=post.post_id)
    
    log("end scheduler")


if __name__ == "__main__":
    chdir(app_src_path)
    scheduler()