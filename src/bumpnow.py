from model.bump import Bump
from util.misc import log
from environment.config import *

def start():
    log("start bump")
    b = Bump()
    b.start()
    log("end bump")

if __name__ == "__main__":
    chdir(app_src_path)
    start()