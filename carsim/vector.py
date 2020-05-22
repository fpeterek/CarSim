class Vector:

    def __init__(self, x: int = None, y: int = None):
        if x is None:
            self.x = 0
            self.y = 0
        elif y is None:
            self.x = x
            self.y = x
        else:
            self.x = x
            self.y = y
