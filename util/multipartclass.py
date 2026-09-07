class MultipartPart:
    def __init__(self):
        self.headers = {}
        self.name = ""
        self.content = b""
        pass

class MultipartRequest:
    def __init__(self):
        self.boundary = ""
        self.parts = []
        pass