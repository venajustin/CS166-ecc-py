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
ctx.draw(domain)

print(domain.g)
a = domain.g
for i in range(6):
    if a is None:
        break
    print(a)
    ctx.draw(a)

    a = domain.add(a, domain.g)

ctx.flush()



domain = Domain(
    4,
    EllipticCurve(0, 1),
    CurvePoint(2, 3),
    6,
    1
)


ctx = GraphContext()
ctx.draw(domain)

print(domain.g)
a = domain.g
for i in range(6):
    if a is None:
        break
    print(a)
    ctx.draw(a)

    print("verify: ", domain.verifyPoint(a))

    a = domain.add(a, domain.g)

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
ctx.draw(P)

Q = CurvePoint(8, 1267)
ctx.draw(Q)

R = CurvePoint(2, 3103)
ctx.draw(R)

TwoP = domain.add( P, P)
ctx.draw(TwoP)

ThreeP = domain.add(TwoP, P)
ctx.draw(ThreeP)

ctx.flush()

FourP1 = domain.add(P,ThreeP)
FourP2 = domain.add(TwoP, TwoP)
assoc1 = domain.add(P, domain.add(Q, R))
assoc2 = domain.add(domain.add(P, Q), R)

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
ctx.draw(domain)

print(domain.g)
a = domain.g
for i in range(6):
    if a is None:
        break
    print(a)
    ctx.draw(a)

    print("verify: ", domain.verifyPoint(a))

    a = domain.add(a, domain.g)

ctx.flush()


domain = Domain(
    None,
    EllipticCurve(0, 1),
    CurvePoint(2, 3),
    6,
    0
)

a = 2
b = domain.multiply(domain.g, a)
print(b)
print("veryify: ", domain.verifyPoint(b))

ctx.draw(domain)
ctx.draw(domain.g)
ctx.draw(b)
ctx.flush()

