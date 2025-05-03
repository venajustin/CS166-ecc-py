from utility.eccMath import EllipticCurve, Domain, CurvePoint
from utility.graphing import GraphContext

#
# y^2 = x^3 + 1
# generator  = ( 2, 3 )
# order = 6
# cofactor = 6 / 6 = 1
#
domain = Domain(
    None,
    EllipticCurve(0, 1),
    CurvePoint(2, 3),
    6,
    1
)


ctx = GraphContext()
domain.draw(ctx)

print(domain.g)
a = domain.g
for i in range(6):
    if a is None:
        break
    print(a)
    a.draw(ctx)

    a = a.add(domain.g, domain)

ctx.flush()
