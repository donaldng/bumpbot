def maskPassword(password):
    return "".join(["*" for i in range(len(password))])

def time2date(ts):
    import time
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))

def log(msg):
    print(msg)
    fh = open("error.log", "a")
    fh.write("{}\n".format(msg))
    fh.close