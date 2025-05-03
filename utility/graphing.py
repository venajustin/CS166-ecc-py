import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np

class GraphContext:
    def __init__(self):
        # y, x = np.ogrid[-5:5:100j, -5:5:100j]
        #
        # self.x = x
        # self.y = y

        self.plt = plt



    def flush(self):
        self.plt.grid()
        self.plt.show()
