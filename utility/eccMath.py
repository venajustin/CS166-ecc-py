import numpy as np

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
        slope = ((3 * (self.x ** 2)) + domain.curve.a) * domain.inv_mod_p(2 * self.y)

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

        slope = self.slopeTo(other, domain)
        if slope is None:
            return None
        if slope == 0:
            new_y = (-self.y) % domain.p        # negative y value modded by p to get in-field value
            return CurvePoint(self.x, new_y)
        newx = (slope ** 2) - (self.x + other.x)
        newy = (slope * (self.x - newx)) - self.y

        # mod within the bounds of domain
        if domain.p is not None:
            newx = newx % domain.p
            newy = newy % domain.p

        return CurvePoint(newx, newy)

    def slopeTo(self, other, domain):
        num = (self.y - other.y)
        den = (self.x - other.x)
        if den == 0:
            return None
        # in order to do division within this field we use the inverse fn
        # return num / den
        return num * domain.inv_mod_p(den)

    def draw(self, ctx):
        ctx.plt.plot(self.x, self.y, 'bo')
        ctx.plt.annotate('(' + str(self.x) + ',' + str(self.y) + ')', (self.x, self.y), textcoords="offset points", xytext=(10, 0), ha='left')

    def inverse(self, domain):
        return CurvePoint(self.x, (-self.y)%domain.p)

class Domain:
    # field: int, curve: EllipticCurve, generator: point, n: integer, h: integer
    def __init__(self, field, curve, generator: CurvePoint, n, h):
        self.p = field  # field parameter (everything is mod p )
        self.curve = curve
        self.g = generator  # g is a generator point
        self.n = n  # is ord(g)
        self.h = h  # cofactor


    def draw(self, ctx):

        if self.p is None:

            y, x = np.ogrid[-5:5:100j, -5:5:100j]
            ctx.plt.contour(y.ravel(), x.ravel(), (pow(y, 2) - pow(x, 3) - x * self.curve.a - self.curve.b), [0])

        # else:
        #     #  we can't plot the graph in this state, but we can graph integer points in this way
        #     a = self.g
        #     while a is not None:
        #         a.draw(ctx)
        #         a = a.add(self.g, self)

        ctx.plt.title('$y^{2} = x^{3}$ + ' + str(self.curve.a) + " * x + " + str(self.curve.b))

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



class EllipticCurve:
    def __init__(self, a, b):
        # curve is defined by y^2 = x^3 + a * x + b
        self.a = a
        self.b = b



    def __str__(self):
        return "Curve: a " + str(self.a) + " b " + str(self.b)
