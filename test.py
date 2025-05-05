from utility.eccMath import EllipticCurve, Domain, CurvePoint
from utility.ecc_func import eccGenShared, eccGenPublic
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
domain = Domain( # secp192k1
    0xfffffffffffffffffffffffffffffffffffffffeffffee37,
    EllipticCurve(0, 3),
    CurvePoint(0xdb4ff10ec057e9ae26b07d0280b7f4341da5d1b1eae06c7d, 0x9b2f2f6d9c5628a7844163d015be86344082aa88d95e2f9d),
    6,
    1
)


ctx = GraphContext()
ctx.draw(domain)

print(domain.g)
a = domain.g
for i in range(10):
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

domain = Domain(
    None,
    EllipticCurve(0, 1),
    CurvePoint(2, 3),
    6,
    1
)
ctx.draw(domain)
sec1 = 2
sec2 = 1
print("domain: " + str(domain))
print("secret1: " +  str(sec1))
print("secret2: " +  str(sec2))
pub1 = eccGenPublic(sec1, domain)
ctx.draw(domain.g)
ctx.draw(pub1)
print("public: ", pub1)

pub2 = eccGenPublic(sec2, domain)
ctx.draw(pub2)
print("public2: ", pub2)

shared1 = eccGenShared(sec2, pub1, domain)
print("shared1: ", shared1)
ctx.draw(shared1)

shared2 = eccGenShared(sec1, pub2, domain)
print("shared2: ", shared2)
ctx.draw(shared2)

ctx.flush()





