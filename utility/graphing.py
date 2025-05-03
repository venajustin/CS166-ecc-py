import matplotlib.pyplot as plt
import numpy as np
from eccMath import CurvePoint

class GraphContext:
    def __init__(self):
        self.plt = plt
        self.fig = plt.subplots()       # figure for further plotting
        self.ax = plt.subplots()        # axes for further plotting

    def draw_curve(self, curve: CurvePoint, x_range=(-10, 10), num_points=400):
        if not (hasattr(curve, 'a') and hasattr(curve, 'b')):
            raise TypeError("The curve parameter must have numeric attributes 'a' and 'b'")
        try:
            a = float(curve.a)
            b = float(curve.b)
        except (ValueError, TypeError):
            raise TypeError("The 'a' and 'b' attributes of curve must be numbers.")
        
        # Generate a set of x values over the given range.
        x = np.linspace(x_range[0], x_range[1], num_points)
        # Calculate f(x) = x^3 + a * x + b.
        f = x**3 + a*x + b
        
        # Only the non-negative f(x) values yield real y; assign NaN where f(x) is negative.
        y_positive = np.where(f >= 0, np.sqrt(f), np.nan)
        y_negative = -y_positive
        
        # Plot both branches of the curve.
        self.ax.plot(x, y_positive, 'r', label='y = +sqrt(x^3 + a*x + b)')
        self.ax.plot(x, y_negative, 'r', label='y = -sqrt(x^3 + a*x + b)')
        
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_title(f'Elliptic Curve: y\u00b2 = x\u00b3 + {a}x + {b}')
        self.ax.grid(True)
    
    # display the graph
    def flush(self):
        self.plt.show()
