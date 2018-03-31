from model.bump import Bump

def start():
    log("start bump")
    b = Bump()
    b.start()
    log("end bump")

if __name__ == "__main__":
    start()