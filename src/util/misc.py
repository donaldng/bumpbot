def maskPassword(password):
    return "".join(["*" for i in range(len(password))])

def time2date(ts):
    import time
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))