import io
import matplotlib
import numpy as np
# matplotlib.use('agg')
import matplotlib.pyplot as plt

class Canvas:
    
    def __init__(self, width, height,  dpi, dpr, offscreen):
        self.width = width
        self.height = height
        self.dpi = dpi
        self.dpr = dpr
        self.offscreen = offscreen
        self.figure = plt.figure(frameon=False,
                                 dpi=self.dpi)
        self.figure.set_size_inches(self.width / self.dpi,
                                    self.height /self.dpi)
        
    def render(self, format):
        self.figure.canvas.draw()
        with io.BytesIO() as output:
            self.figure.savefig(output, format='raw')
            output.seek(0)
            data = np.frombuffer(output.getvalue(), dtype=np.uint8)
        return data.reshape(self.ratio * self.height,
                            self.ratio * self.width,
                            -1)

