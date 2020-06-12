class JsonException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return 'Json Exception msg is: {}'.format(self.msg)
