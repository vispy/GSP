import io
import matplotlib as mpl
import numpy as np
# matplotlib.use('agg')
import matplotlib.pyplot as plt

class Canvas:
    
    def __init__(self, width, height,  dpi):
        self.width = width
        self.height = height
        self.dpi = dpi
        self.figure = plt.figure(frameon=False,
                                 dpi=self.dpi)
        self.figure.patch.set_alpha(0.0)
        self.figure.set_size_inches(self.width / self.dpi,
                                    self.height /self.dpi)

    def run(self):
        plt.show()
        
    def render(self, format):
        self.figure.canvas.draw()
        with io.BytesIO() as output:
            self.figure.savefig(output, format='raw')
            output.seek(0)
            data = np.frombuffer(output.getvalue(), dtype=np.uint8)
        return data.reshape(self.ratio * self.height,
                            self.ratio * self.width,
                            -1)

