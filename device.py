

class oscilloscope(object):
    def __init__(self):
        pass

    def decode(self, cmd, arg):
        print ("osc: {}, {}".format(cmd, arg))
        ret = "osc ok"
        return ret


