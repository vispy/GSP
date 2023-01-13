from .app import default_app


class Viewport:
    def __init__(self, canvas, x, y, width, height):
        self.canvas = canvas
        self.extent = x, y, width, height

    def set_position(self, x, y):
        raise NotImplementedError

    def set_size(self, width, height):
        raise NotImplementedError
