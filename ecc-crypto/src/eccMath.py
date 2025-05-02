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
        
        num = (3 * (self.x ** 2) + a) % p
        den = (2 * self.y) % p
        if den == 0:                # division by zero check
            return None
        multinv_den = pow(den, -1, p)
        slope = (num * multinv_den) % p

        newx = ((slope ** 2) - (2 * self.x)) % p
        newy = ((slope * (self.x - newx)) - self.y) % p

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
            if (2 * self.y) % p == 0:
                return None
            return self.double(domain)

        slope = self.slopeTo(other, domain)  
        newx = ((slope ** 2) - (self.x + other.x)) % p
        newy = ((slope * (self.x - newx)) - self.y) % p

        return CurvePoint(newx, newy)

    def slopeTo(self, other, domain):
        if not isinstance(other, CurvePoint) or not isinstance(domain, Domain):
            raise TypeError("Slope calculation must be performed on given two curve points and a domain")
        p = domain.field

        num = (self.y - other.y) % p
        den = (self.x - other.x) % p
        if den == 0:                # division by zero check
                return None
        multinv_den = pow(den, -1, p)
        slope = (num * multinv_den) % p

        return slope

    def draw(self, ctx):
        if not hasattr(ctx, 'ax'):
            raise TypeError("The graphing context must have an 'ax' attribute.")
        if not callable(getattr(ctx.ax, 'plot', None)):
            raise TypeError("ctx.ax must have a callable 'plot' method.")
        if not callable(getattr(ctx.ax, 'annotate', None)):
            raise TypeError("ctx.ax must have a callable 'annotate' method.")
        
        # draw the plot using blue and annotate the points
        ctx.ax.plot(self.x, self.y, 'bo')
        ctx.ax.annotate(f'({self.x}, {self.y})', (self.x, self.y), textcoords="offset points", xytext=(0,10), ha='center')

class EllipticCurve:
    def __init__(self, a: int, b: int) -> None:
        # curve is defined by y^2 = x^3 + a * x + b
        self.a = a
        self.b = b

    def verifyPoint(self, point: CurvePoint, domain) -> bool:
        if not isinstance(point, CurvePoint) or not isinstance(domain, Domain):
            raise TypeError("Point verification can only be performed between a CurvePoint and a Domain")
        
        p = domain.field

        lhs = pow(point.y, 2, p)
        rhs = (pow(point.x, 3, p) + self.a * point.x + self.b) % p
        return lhs == rhs

    def __str__(self):
        return "Curve: a " + str(self.a) + " b " + str(self.b)
    

class Domain:
    #  curve: EllipticCurve, generator: CurvePoint, n: integer, h: integer
    def __init__(self, field: int, curve: EllipticCurve, generator: CurvePoint, n: int, h: int) -> None:
        self.field = field      # system modulus
        self.curve = curve      # contains a, b
        self.g = generator      # g is a generator point
        self.n = n              # is ord(g)
        self.h = h              # cofactor


    def draw(self, ctx):
        if not hasattr(ctx, 'plt'):
            raise TypeError("The drawing context must have a 'plt' attribute.")
        if not hasattr(ctx, 'ax'):
            raise TypeError("The drawing context must have an 'ax' attribute.")
        if not callable(getattr(ctx.ax, 'contour', None)):
            raise TypeError("ctx.ax must have a callable 'contour' method.")
        if not callable(getattr(ctx.plt, 'title', None)):
            raise TypeError("ctx.plt must have a callable 'title' method.")

        sections = []
        p = self.field

        for i in range(5):
            start = -p + 1 + (p * i)
            stop = p * i -2
            y, x = np.ogrid[start:stop:200j, start:stop:200j]
            sections.append([x,y])

        for [x, y] in sections:
            xmod = x % p
            ymod = y % p

        # plot the curve
        ctx.plt.contour(xmod.ravel(), ymod.ravel(), pow(y, 2) - pow(x, 3) - x * self.curve.a - self.curve.b, [0])
        ctx.plt.title('$y^{2} = x^{3}$ + ' + str(self.curve.a) + " * x + " + str(self.curve.b))
