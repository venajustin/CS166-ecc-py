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



domain = Domain(
    4,
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

    print("verify: ", domain.verifyPoint(a))

    a = a.add(domain.g, domain)

ctx.flush()



# test 3
domain = Domain(
    15733,
    EllipticCurve(1, 3),
    CurvePoint(0,0), # unknown
    0, # not needed
    0 # not needed
)
P = CurvePoint(6, 15)
P.draw(ctx)
Q = CurvePoint(8, 1267)
Q.draw(ctx)
R = CurvePoint(2, 3103)
R.draw(ctx)
TwoP = P.add(P, domain)
TwoP.draw(ctx)
ThreeP = TwoP.add(P, domain)
ThreeP.draw(ctx)
ctx.flush()
FourP1 = P.add(ThreeP, domain)
FourP2 = TwoP.add(TwoP, domain)
assoc1 = P.add(Q.add(R, domain), domain)
assoc2 = P.add(Q, domain).add(R, domain)
print("FourP2: ", FourP2)
print("FourP2: ", FourP2)

print("Associative point 1: ", assoc1)
print("Associative point 2: ", assoc2)

print("validity checks: ")
print(domain.verifyPoint(P))
print(domain.verifyPoint(Q))
print(domain.verifyPoint(R))
print(domain.verifyPoint(TwoP))
print(domain.verifyPoint(ThreeP))
print(domain.verifyPoint(FourP1))
print(domain.verifyPoint(assoc1))

#test 4
domain = Domain(
    4,
    EllipticCurve(0, 7),
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

    print("verify: ", domain.verifyPoint(a))

    a = a.add(domain.g, domain)

ctx.flush()
