
class Domain:
    # field: int, curve: EllipticCurve, generator: point, n: integer, h: integer
    def __init__(self, field, curve, generator, n, h):
       self.p = field # field parameter (everything is mod p )
       self.curve = curve
       self.g = generator # g is a generator point
       self.n = n # is ord(g)
       self.h = h # cofactor

class EllipticCurve:
    def __init__(self, a, b):
        # curve is defined by y^2 = x^3 + a * x + b
        self.a = a
        self.b = b

    def verifyPoint(self, point):
        difference = point.y**2 - (point.x**3 + (self.a * point.x) + self.b)
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


    def add(self, other, domain):
        slope = self.slopeTo(other)
        if slope == None:
            return None
        newx = ( slope ** 2 ) - (self.x + other.x)
        newy = ( slope * (self.x - newx) ) - self.y
        
        return CurvePoint(newx, newy)

    def slopeTo(self, other):
        num = ( self.y - other.y )
        den = ( self.x - other.x )
        if den == 0:
            return None
        return num / den
