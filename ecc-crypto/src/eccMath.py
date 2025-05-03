import numpy as np

class CurvePoint:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __str__(self):
        return "Point x " + str(self.x) + " y " + str(self.y)

    def multiply(self, coefficient: int, domain):
        if not isinstance(domain, Domain):
            raise TypeError("Scalar multiplication can only performed within a domain.")
        if not isinstance(coefficient, int) or coefficient < 0:
            raise ValueError("Coefficient must be a non-negative integer.")
        
        if coefficient == 0:
            return None

        result = None
        output = self

        while coefficient:
            if coefficient == 1:
                if result is None:
                    result = output
                else:
                    result = result.add(output, domain)
                    if result is None:
                        return None
            output = output.double(domain)
            if output is None and coefficient > 1:
                return None                         # point at infinity
            coefficient //= 2
        return result

    def double(self, domain):
        if not isinstance(domain, Domain):
            raise TypeError("Point doubling can be performed only within a domain.")
        
        p = domain.field
        a = domain.curve.a

        if self.y == 0:
            return None
        
        # finite‐field branch
        if isinstance(p, int):
            num = (3 * (self.x ** 2) + a) % p
            den = (2 * self.y) % p
            if den == 0:
                return None
            inv_den = pow(den, -1, p)
            slope = (num * inv_den) % p
            newx = (slope * slope - 2 * self.x) % p
            newy = (slope * (self.x - newx) - self.y) % p
        # real branch
        else:
            num = 3 * (self.x ** 2) + a
            den = 2 * self.y
            if den == 0:
                return None
            slope = num / den
            newx = slope * slope - 2 * self.x
            newy = slope * (self.x - newx) - self.y

        return CurvePoint(newx, newy)

    def add(self, other, domain):
        if not isinstance(other, CurvePoint) or not isinstance(domain, Domain):
            raise TypeError("Point addition can only be performed on given two curve points and a domain")
        
        p = domain.field

        # case when one of the points is at infinity
        if self is None:        # oo + P = P
            return other
        if other is None:       # P + oo = P
            return self        

        # case when both points are the same
        if other.x == self.x and other.y == self.y:     # P + P = 2P
            # finite-field branch
            if isinstance(p, int):
                if (2 * self.y) % p == 0:
                    return None
            # real branch
            else:
                if (2 * self.y) == 0:
                    return None
            return self.double(domain)

        slope = self.slopeTo(other, domain) 
        if slope is None:
            return None
         
        # finite‐field
        if isinstance(p, int):
            newx = ((slope ** 2) - (self.x + other.x)) % p
            newy = ((slope * (self.x - newx)) - self.y) % p
        # real
        else:
            newx = slope ** 2 - (self.x + other.x)
            newy = slope * (self.x - newx) - self.y

        return CurvePoint(newx, newy)

    def slopeTo(self, other, domain):
        if not isinstance(other, CurvePoint) or not isinstance(domain, Domain):
            raise TypeError("Slope calculation must be performed on given two curve points and a domain")
        p = domain.field

        # finite‐field
        if isinstance(p, int):
            num = (self.y - other.y) % p
            den = (self.x - other.x) % p
            if den == 0:
                return None
            inv_den = pow(den, -1, p)
            return (num * inv_den) % p
        # real
        else:
            num = self.y - other.y
            den = self.x - other.x
            if den == 0:
                return None
            return num / den

        return slope

    def draw(self, ctx):
        ctx.plt.plot(self.x, self.y, 'bo')
        ctx.plt.annotate('(' + str(self.x) + ',' + str(self.y) + ')', (self.x,
                         self.y), textcoords="offset points", xytext=(10, 0), ha='left')

class EllipticCurve:
    def __init__(self, a: int, b: int) -> None:
        # curve is defined by y^2 = x^3 + a * x + b
        self.a = a
        self.b = b

    def verifyPoint(self, point: CurvePoint, domain) -> bool:
        if not isinstance(point, CurvePoint) or not isinstance(domain, Domain):
            raise TypeError("Point verification can only be performed between a CurvePoint and a Domain")
        
        p = domain.field

        # finite‑field
        if isinstance(p, int):
            lhs = pow(point.y, 2, p)
            rhs = (pow(point.x, 3, p) + self.a * point.x + self.b) % p
            return lhs == rhs
        # real
        else:
            return point.y**2 == (point.x**3 + self.a * point.x + self.b)

    def __str__(self) -> str:
        return "Curve: a " + str(self.a) + " b " + str(self.b)
    

class Domain:
    #  curve: EllipticCurve, generator: CurvePoint, n: integer, h: integer
    def __init__(self, field: int, curve: EllipticCurve, generator: CurvePoint, n: int, h: int) -> None:
        self.field = field      # system modulus
        self.curve = curve      # contains a, b
        self.g = generator      # g is a generator point
        self.n = n              # is ord(g)
        self.h = h              # cofactor


    def draw(self, ctx) -> None:
        sections = []
        if self.p is None:

            y, x = np.ogrid[-5:5:100j, -5:5:100j]
            sections.append([x, y])
        else:

            for i in range(5):
                y, x = np.ogrid[-self.p + 1 + (self.p * i):self.p * i - 2:200j,
                                -self.p + 1 + (self.p * i):self.p * i - 2:200j]
                sections.append([x, y])

        for [x, y] in sections:
            if self.p is not None:
                xmod = x % self.p
                ymod = y % self.p
            else:
                xmod = x
                ymod = y
            ctx.plt.contour(xmod.ravel(), ymod.ravel(), pow(
                y, 2) - pow(x, 3) - x * self.curve.a - self.curve.b, [0])
        ctx.plt.title('$y^{2} = x^{3}$ + ' +
                      str(self.curve.a) + " * x + " + str(self.curve.b))