from model.bump import Bump
from util.misc import log

def start():
    log("start bump")
    b = Bump()
    b.start()
    log("end bump")

if __name__ == "__main__":
    start()