from timeit import default_timer as timer


class Timer(object):
    def __init__(self, msg, fmt="%0.3g"):
        self.msg = msg
        self.fmt = fmt

    def __enter__(self):
        print(self.msg)
        self.start = timer()
        return self

    def __exit__(self, *args):
        t = timer() - self.start
        print(("%s took " + self.fmt + " seconds") % (self.msg, t))
        self.time = t
