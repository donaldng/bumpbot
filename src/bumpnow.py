from model.bump import Bump
from util.misc import log
from environment.config import *
import os

def start():
    b = Bump()
    b.start()

if __name__ == "__main__":
    os.chdir(app_src_path)
    start()
