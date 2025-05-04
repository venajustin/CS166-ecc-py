import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np

from utility.eccMath import Domain, CurvePoint


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


    def draw(self, obj):
        if isinstance(obj, Domain):
            if obj.p is None:

                y, x = np.ogrid[-5:5:100j, -5:5:100j]
                self.plt.contour(y.ravel(), x.ravel(),
                                 (pow(y, 2) - pow(x, 3) - x * obj.curve.a - obj.curve.b), [0])

            # else:
            #     #  we can't plot the graph in this state, but we can graph integer points in this way
            #     a = self.g
            #     while a is not None:
            #         a.draw(ctx)
            #         a = a.add(self.g, self)

            self.plt.title('$y^{2} = x^{3}$ + ' + str(obj.curve.a) + " * x + " + str(obj.curve.b))
        if isinstance(obj, CurvePoint):
            self.plt.plot(obj.x, obj.y, 'bo')
            self.plt.annotate('(' + str(obj.x) + ',' + str(obj.y) + ')', (obj.x, obj.y),
                                 textcoords="offset points", xytext=(10, 0), ha='left')
