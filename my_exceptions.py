class SetupException(Exception):
    def __init__(self, value, read_write=None, address=None, data=None):
        self.value = value        
    def __str__(self):
        return repr(self.value)

class SendingException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class ConvertionException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

