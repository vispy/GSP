
class Viewport:
    def __init__(self, canvas, x, y, width, height):
        self.canvas = canvas
        self.extent = x, y, width, height
        self.axes = canvas.figure.add_axes([x / canvas.width,
                                            y / canvas.height,
                                            width / canvas.width,   
                                            height / canvas.height])
        self.axes.autoscale(False)
        self.axes.set_xlim(0, width)
        self.axes.set_ylim(0, height)
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)
        for position in ["top", "bottom", "left", "right"]:
            self.axes.spines[position].set_visible(False)

    def set_position(self, x, y):
        raise NotImplementedError

    def set_size(self, width, height):
        raise NotImplementedError

