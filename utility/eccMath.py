import numpy as np


class Domain:
    # field: int, curve: EllipticCurve, generator: point, n: integer, h: integer
    def __init__(self, field, curve, generator, n, h):
        self.p = field  # field parameter (everything is mod p )
        self.curve = curve
        self.g = generator  # g is a generator point
        self.n = n  # is ord(g)
        self.h = h  # cofactor


    def draw(self, ctx):

        sections = []
        if self.p is None:

            y, x = np.ogrid[-5:5:100j, -5:5:100j]
            sections.append([x, y])
        else:

            for i in range(5):
                y, x = np.ogrid[-self.p + 1 + (self.p * i):self.p * i - 2:200j, -self.p + 1 + (self.p * i):self.p * i - 2:200j]
                sections.append([x,y])

        for [x, y] in sections:
            if self.p is not None:
                xmod = x % self.p
                ymod = y % self.p
            else:
                xmod = x
                ymod = y
            ctx.plt.contour(xmod.ravel(), ymod.ravel(), pow(y, 2) - pow(x, 3) - x * self.curve.a - self.curve.b, [0])
        ctx.plt.title('$y^{2} = x^{3}$ + ' + str(self.curve.a) + " * x + " + str(self.curve.b))




class EllipticCurve:
    def __init__(self, a, b):
        # curve is defined by y^2 = x^3 + a * x + b
        self.a = a
        self.b = b

    def verifyPoint(self, point):
        if point == None:
            return False
        difference = point.y ** 2 - (point.x ** 3 + (self.a * point.x) + self.b)
        if difference < .0001 and difference > -0.0001:
            return True
        else:
            return False

    def __str__(self):
        return "Curve: a " + str(self.a) + " b " + str(self.b)




class CurvePoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point x " + str(self.x) + " y " + str(self.y)

    def multiply(self, coefficient, domain):

        output = self
        if coefficient == 1:
            return output

        output = output.double(domain)
        if output == None:
            return None
        # print("Multiply: ", self," x ", coefficient)
        # print(output)
        for i in range(coefficient - 2):
            output = output.add(self, domain)
            if output == None:
                return None
            # print(output)

        return output

    def double(self, domain):

        if self.y == 0:
            return None

        # the slope of the curve at this point
        slope = ((3 * (self.x ** 2)) + domain.curve.a) / (2 * self.y)

        newx = slope ** 2 - (2 * self.x)
        newy = (slope * (self.x - newx)) - self.y

        # mod within the bounds of domain
        if domain.p is not None:
            newx = newx % domain.p
            newy = newy % domain.p

        return CurvePoint(newx, newy)

    def add(self, other, domain):
        if other.x == self.x and other.y == self.y:
            return self.double(domain)

        slope = self.slopeTo(other)
        if slope is None:
            return None
        if slope == 0:
            return CurvePoint(self.x, -self.y)
        newx = (slope ** 2) - (self.x + other.x)
        newy = (slope * (self.x - newx)) - self.y

        # mod within the bounds of domain
        if domain.p is not None:
            newx = newx % domain.p
            newy = newy % domain.p

        return CurvePoint(newx, newy)

    def slopeTo(self, other):
        num = (self.y - other.y)
        den = (self.x - other.x)
        if den == 0:
            return None
        return num / den

    def draw(self, ctx):
        ctx.plt.plot(self.x, self.y, 'bo')
        ctx.plt.annotate('(' + str(self.x) + ',' + str(self.y) + ')', (self.x, self.y), textcoords="offset points", xytext=(10, 0), ha='left')

