import numpy as np


class Domain:
    # field: int, curve: EllipticCurve, generator: point, n: integer, h: integer
    def __init__(self, field, curve, generator, n, h):
        self.p = field  # field parameter (everything is mod p )
        self.curve = curve
        self.g = generator  # g is a generator point
        self.n = n  # is ord(g)
        self.h = h  # cofactor



    def verifyPoint(self, point):
        if point is None:
            return True
        if self.p is not None:
            difference = (point.y ** 2 - (point.x ** 3 + self.curve.a * point.x + self.curve.b)) % self.p
            return (
                    .0001 > difference > -0.0001
                    and
                    0 <= point.x < self.p and 0 <= point.y < self.p
            )
        else:
            difference = point.y ** 2 - (point.x ** 3 + (self.curve.a * point.x) + self.curve.b)
            return .0001 > difference > -0.0001

    def inv_mod_p(self, x):
        if self.p is None: # real
            return 1 / x
        if x % self.p == 0: # finite field
            raise ZeroDivisionError("no inverse for " + x + " in field")
        return pow(x, self.p-2, self.p)

    def multiply(self, point, coefficient):

        output = point
        if coefficient == 1:
            return output

        output = self.double(output)
        if output == None:
            return None
        # print("Multiply: ", self," x ", coefficient)
        # print(output)
        for i in range(coefficient - 2):
            output = self.add(output, point)
            if output == None:
                return None
            # print(output)

        return output

    def double(self, point):

        if point.y == 0:
            return None

        # the slope of the curve at this point
        slope = ((3 * (point.x ** 2)) + self.curve.a) * self.inv_mod_p(2 * point.y)

        newx = slope ** 2 - (2 * point.x)
        newy = (slope * (point.x - newx)) - point.y

        # mod within the bounds of domain
        if self.p is not None:
            newx = newx % self.p
            newy = newy % self.p

        return CurvePoint(newx, newy)

    def add(self, point1, point2):
        if point2.x == point1.x and point2.y == point1.y:
            return self.double(point1)

        slope = self.slopeTo(point1, point2)
        if slope is None:
            return None
        if slope == 0:
            return CurvePoint(point1.x, -point1.y % self.p)
        newx = (slope ** 2) - (point1.x + point2.x)
        newy = (slope * (point1.x - newx)) - point1.y

        # mod within the bounds of domain
        if self.p is not None:
            newx = newx % self.p
            newy = newy % self.p

        return CurvePoint(newx, newy)

    def slopeTo(self, point1, point2):
        num = (point1.y - point2.y)
        den = (point1.x - point2.x)
        if den == 0:
            return None
        # in order to do division within this field we use the inverse fn
        # return num / den
        return num * self.inv_mod_p(den)


    def inverse(self, point):
        return CurvePoint(point.x, (-point.y)%self.p)


    def draw(self, ctx):
        ctx.plt.plot(self.x, self.y, 'bo')
        ctx.plt.annotate('(' + str(self.x) + ',' + str(self.y) + ')', (self.x, self.y), textcoords="offset points", xytext=(10, 0), ha='left')

class EllipticCurve:
    def __init__(self, a, b):
        # curve is defined by y^2 = x^3 + a * x + b
        self.a = a
        self.b = b



    def __str__(self):
        return "Curve: a " + str(self.a) + " b " + str(self.b)




class CurvePoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point x " + str(self.x) + " y " + str(self.y)

