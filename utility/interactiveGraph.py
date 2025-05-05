import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np

from utility.eccMath import Domain, CurvePoint
#
# class DemoLine:
#     def __init__(self, p1, p2, p3):
#         self.points = [p1, p2, p3]

class InteractiveContext:
    def __init__(self):

        self.plt = plt

        self.fig, self.ax = plt.subplots()
        self.fig.subplots_adjust(bottom=0.2)

        self.element_list = []
        self.element_pos = 0

    def start(self):
        axstep = self.fig.add_axes([0.81, 0.05, 0.1, 0.075])
        bstep = Button(axstep, 'Step')
        bstep.on_clicked(self.step)
        axstepback = self.fig.add_axes([0.7, 0.05, 0.1, 0.075])
        bstepback = Button(axstepback, 'Back')
        bstepback.on_clicked(self.step_back)

        axreset = self.fig.add_axes([0.1, 0.05, 0.2, 0.075])
        breset = Button(axreset, 'Hide Intermediate')
        breset.on_clicked(self.hide_points)

        self.ax.grid()
        self.plt.show()


    def draw(self, obj):
        if isinstance(obj, Domain):
            if obj.p is None:

                y, x = np.ogrid[-5:5:100j, -5:5:100j]
                contour = self.ax.contour(y.ravel(), x.ravel(),
                                 (pow(y, 2) - pow(x, 3) - x * obj.curve.a - obj.curve.b), [0])
                contour.set_alpha(0)
                self.element_list.append((contour, None))

            # else:
            #     #  we can't plot the graph in this state, but we can graph integer points in this way
            #     a = self.g
            #     while a is not None:
            #         a.draw(ctx)
            #         a = a.add(self.g, self)

            self.plt.title('$y^{2} = x^{3}$ + ' + str(obj.curve.a) + " * x + " + str(obj.curve.b))
        if isinstance(obj, CurvePoint):
            point, = self.ax.plot(obj.x, obj.y, 'bo')
            annotation = self.ax.annotate('(' + str(obj.x) + ',' + str(obj.y) + ')', (obj.x, obj.y),
                                 textcoords="offset points", xytext=(10, 0), ha='left')
            point.set_alpha(0)
            annotation.set_alpha(0)

            self.element_list.append((point, annotation))
        return obj

    def draw_add(self, point1, point2, domain):
        output = domain.add(point1, point2)
        inverse = domain.inverse(output)
        if point1 is None or point2 is None or domain is None:
            return
        x = [point1.x, point2.x, inverse.x]
        y = [point1.y, point2.y, inverse.y]
        line,  = self.ax.plot(x, y, 'r')
        line.set_alpha(0)
        self.element_list.append((line, None))
        line2, = self.ax.plot([inverse.x, output.x], [inverse.y, output.y])
        line2.set_alpha(0)
        self.element_list.append((line2, None))
        return output

    def step(self, event):
        # steps through the animation by revealing the next item in the element list
        if self.element_pos < len(self.element_list):
            curr = self.element_list[self.element_pos]

            curr[0].set_alpha(1.0)
            if curr[1] is not None:
                curr[1].set_alpha(1.0)
            self.element_pos += 1
        self.plt.draw()

    def step_back(self, event):
        # steps through the animation by revealing the next item in the element list
        if self.element_pos > 0:
            self.element_pos -= 1

            curr = self.element_list[self.element_pos]

            curr[0].set_alpha(0)
            if curr[1] is not None:
                curr[1].set_alpha(0)
        self.plt.draw()

    def hide_points(self, event):
        for element in self.element_list:
            element[0].set_alpha(0.0)
            if element[1] is not None:
                element[1].set_alpha(0.0)
        try:
            self.element_list[0][0].set_alpha(1.0)
            self.element_list[1][0].set_alpha(1.0)
            self.element_list[1][1].set_alpha(1.0)
        finally:
            pass
        self.plt.draw()