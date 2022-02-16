class NoFaceFoundError(Exception):
    def __init__(self):
        self.message = "No faces found"
        super().__init__(self.message)
